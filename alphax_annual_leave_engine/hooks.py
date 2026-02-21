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

# --- Asset hooks (explicit empty) to prevent Frappe v15 esbuild from resolving undefined paths ---
app_include_js = []
app_include_css = []
web_include_js = []
web_include_css = []
doctype_js = {}
doctype_css = {}
