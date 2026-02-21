import frappe
from frappe.utils import getdate, date_diff

from alphax_annual_leave_engine.alphax_annual_leave_engine.doctype.ale_settings.ale_settings import (
    get_enabled_leave_types,
)


def _get_holiday_list(employee: str, company: str | None = None) -> str | None:
    """Priority: Employee.holiday_list > Company.default_holiday_list"""
    holiday_list = frappe.db.get_value("Employee", employee, "holiday_list")
    if holiday_list:
        return holiday_list
    if company:
        return frappe.db.get_value("Company", company, "default_holiday_list")
    return None


def _count_excluded_public_holidays(holiday_list: str, from_date, to_date) -> int:
    """Count holidays inside range that should NOT be deducted from Annual Leave.

    Rule:
      - Subtract ONLY holidays where custom_exclude_from_annual_leave = 1 AND weekly_off = 0
      - Do NOT subtract weekly_off (weekends are still counted as leave days)
    """
    rows = frappe.get_all(
        "Holiday",
        filters={
            "parent": holiday_list,
            "holiday_date": ["between", [from_date, to_date]],
            "custom_exclude_from_annual_leave": 1,
            "weekly_off": 0,
        },
        fields=["holiday_date"],
    )
    return len(rows)


@frappe.whitelist()
def get_number_of_leave_days(
    employee,
    leave_type,
    from_date,
    to_date,
    half_day=0,
    half_day_date=None,
    company=None,
):
    """Calendar (inclusive) days minus selected public holidays for configured leave types.

    - Weekends are counted (even if they exist as weekly_off rows in Holiday List)
    - Only configured Leave Types (ALE Settings) use this logic; others fallback to ERPNext
    """
    if not (employee and leave_type and from_date and to_date):
        return 0

    enabled_leave_types = set(get_enabled_leave_types())

    if leave_type not in enabled_leave_types:
        return _fallback_erpnext(employee, leave_type, from_date, to_date, half_day, half_day_date, company)

    fd = getdate(from_date)
    td = getdate(to_date)
    if td < fd:
        frappe.throw("To Date cannot be before From Date")

    total_days = date_diff(td, fd) + 1  # inclusive calendar days

    holiday_list = _get_holiday_list(employee, company)
    excluded = 0
    if holiday_list:
        excluded = _count_excluded_public_holidays(holiday_list, fd, td)

    # Half-day handling (optional but safe)
    if int(half_day) and half_day_date:
        hd = getdate(half_day_date)
        if holiday_list:
            is_excluded = frappe.db.exists(
                "Holiday",
                {
                    "parent": holiday_list,
                    "holiday_date": hd,
                    "custom_exclude_from_annual_leave": 1,
                    "weekly_off": 0,
                },
            )
            if is_excluded:
                # If half-day is on an excluded public holiday, that day should not be deducted at all.
                return max(total_days - excluded - 1, 0)

        return max(total_days - excluded - 0.5, 0)

    return max(total_days - excluded, 0)


def _fallback_erpnext(employee, leave_type, from_date, to_date, half_day=0, half_day_date=None, company=None):
    """Call ERPNext original implementation."""
    from erpnext.hr.doctype.leave_application.leave_application import get_number_of_leave_days as original

    return original(employee, leave_type, from_date, to_date, half_day, half_day_date, company)
