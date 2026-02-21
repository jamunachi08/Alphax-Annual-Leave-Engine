import frappe
from frappe.model.document import Document

class ALESettings(Document):
    pass


@frappe.whitelist()
def get_enabled_leave_types():
    settings = frappe.get_single("ALE Settings")
    if not getattr(settings, "enabled", 0):
        return []
    return [row.leave_type for row in (settings.leave_types or []) if row.leave_type]
