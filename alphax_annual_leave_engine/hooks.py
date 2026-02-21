app_name = "alphax_annual_leave_engine"
app_title = "AlphaX Annual Leave Engine"
app_publisher = "AlphaX"
app_description = "Annual Leave deduction logic: calendar days (weekends included) minus selected public holidays."
app_email = "support@alphax.com"
app_license = "MIT"

fixtures = [
    {"dt": "Custom Field", "filters": [["name", "in", [
        "Holiday-custom_exclude_from_annual_leave"
    ]]]}
]

override_whitelisted_methods = {
    "erpnext.hr.doctype.leave_application.leave_application.get_number_of_leave_days":
        "alphax_annual_leave_engine.overrides.leave_application.get_number_of_leave_days"
}
