# AlphaX Annual Leave Engine (ERPNext / Frappe)

A small, installable Frappe app that enforces the following **Annual Leave policy**:

- **Annual Leave counts calendar days (weekends included).**
- **Selected public/government holidays (e.g., Eid/Ramadan holiday ranges) are NOT deducted** from Annual Leave.
- HR can control which holidays are excluded using a simple checkbox on Holiday List rows.
- Applies **only to the Leave Types you enable** in **ALE Settings**.

---

## Why this exists

ERPNext’s standard leave-day calculation can either:
- include holidays as leave days, or
- exclude all holidays (including weekends) from leave days.

Many KSA implementations need a hybrid policy:
- weekends are counted in Annual Leave (calendar-days policy),
- but official public holidays (Eid / National Day / Founding Day etc.) should not reduce annual leave entitlement.

This app implements that policy cleanly.

---

## How it works (high level)

For enabled Leave Types (configured in **ALE Settings**):

**Deducted Days = (To Date - From Date + 1) - (Excluded Public Holidays inside range)**

- The date range is **inclusive** (calendar days).
- Weekends are **not excluded** (even if they exist as `weekly_off` rows in Holiday List).
- Only holidays where **Exclude from Annual Leave Deduction** is checked are subtracted.

---

## Installation (Bench / Frappe Cloud)

```bash
bench get-app https://github.com/<YOUR-ORG>/alphax_annual_leave_engine
bench --site <YOUR-SITE> install-app alphax_annual_leave_engine
bench --site <YOUR-SITE> migrate
```

---

## Configuration (HR Operations)

### 1) Maintain Holiday List normally
- HR → Leaves → **Holiday List**
- Add weekly offs using **Add Weekly Holidays**
- Add public holidays (Eid/Ramadan etc.) as Holiday rows

### 2) Mark public holidays to be excluded from Annual Leave deduction
In **Holiday List → Holidays (child rows)**, tick:

✅ **Exclude from Annual Leave Deduction**

**Important:** Do *not* tick this for weekly offs/weekends.

### 3) Enable and scope the rule to your Annual Leave type
Open:

**ALE Settings**
- Enabled = ✅
- Add Leave Type(s): e.g. **Annual Leave**

Only the selected Leave Types will use this engine.

---

## Validation and UI consistency

This app overrides ERPNext’s whitelisted method used to compute leave days for both:
- the Leave Application form (UI days), and
- server-side validation and balance checks.

So you won’t get “UI shows X days, server deducts Y days” mismatches.

---

## KSA Compliance Notes (Practical Guidance)

> **Not legal advice.** This section is operational guidance for HR/ERP configuration in KSA.

### Annual leave entitlement (baseline)
HRSD states an employee is entitled to **annual leave of not less than 21 days**, increasing to **not less than 30 days** after 5 consecutive years with the same employer.  
Source: HRSD knowledge center article “Annual Leave”.  
https://www.hrsd.gov.sa/en/knowledge-centre/articles/321

### Public holidays overlapping annual leave (common KSA HR practice)
Many KSA HR interpretations and guidance treat official public holidays (e.g., Eid holidays) as **not reducing annual leave**, i.e., leave is extended/adjusted when public holidays overlap.  
This app supports that operational outcome by allowing HR to mark those public holidays as excluded from Annual Leave deduction.

For official legal references, always validate against:
- The latest HRSD labor law publication (official PDF) and updates.
https://www.hrsd.gov.sa/sites/default/files/2023-02/Labor.pdf

### Weekends policy is company-specific
Whether weekends are counted as annual leave days can vary by internal policy and contract terms. This app is designed for organizations that explicitly want **calendar-day annual leave** (weekends included) while still excluding official public holidays.

---

## Technical Details

### What is added
- Custom Field on Holiday child rows:
  - `Holiday.custom_exclude_from_annual_leave` (Check)
- New Single Doctype:
  - **ALE Settings** (configure enabled Leave Types)
- Override:
  - `erpnext.hr.doctype.leave_application.leave_application.get_number_of_leave_days`

### Rule applied
- Subtract holidays only when:
  - `custom_exclude_from_annual_leave = 1`
  - `weekly_off = 0`

So weekends remain counted.

---

## Support / Roadmap (Optional)

If you want enhancements:
- Prevent ticking exclusion on Weekly Off rows automatically
- A report: “Excluded Public Holidays Used in Leave”
- Dashboard cards: “Adjusted Days vs Calendar Days”
- Multi-company settings

---

## License
MIT
