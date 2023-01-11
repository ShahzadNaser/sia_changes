import frappe
from frappe import scrub
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.utils import nowdate, unique

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def bom(doctype, txt, searchfield, start, page_len, filters):
    doctype = "BOM"
    conditions = []
    fields = get_fields(doctype, ["name", "item"])
    print("=============bom==========")
    return frappe.db.sql(
        """select {fields}
        from `tabBOM`
        where `tabBOM`.is_active=1
            and `tabBOM`.`{key}` like %(txt)s
            {fcond} {mcond}
        order by
            (case when locate(%(_txt)s, name) > 0 then locate(%(_txt)s, name) else 99999 end),
            idx desc, name
        limit %(page_len)s offset %(start)s""".format(
            fields=", ".join(fields),
            fcond=get_filters_cond(doctype, filters, conditions).replace("%", "%%"),
            mcond=get_match_cond(doctype).replace("%", "%%"),
            key=searchfield,
        ),
        {
            "txt": "%" + txt + "%",
            "_txt": txt.replace("%", ""),
            "start": start or 0,
            "page_len": page_len or 20,
        },
    )

def get_fields(doctype, fields=None):
	if fields is None:
		fields = []
	meta = frappe.get_meta(doctype)
	fields.extend(meta.get_search_fields())

	if meta.title_field and not meta.title_field.strip() in fields:
		fields.insert(1, meta.title_field.strip())

	return unique(fields)
