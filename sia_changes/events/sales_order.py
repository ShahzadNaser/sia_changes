import frappe
from frappe import _

def before_save(doc, method):
    if doc.get("items") and (doc.items[0].get("prevdoc_docname") or doc.items[len(doc.get("items"))-1].get("prevdoc_docname")):
        doc_name = doc.items[0].get("prevdoc_docname") or doc.items[len(doc.get("items"))-1].get("prevdoc_docname")
        if doc_name and frappe.db.get_value("Sales Order Item",{"parent":["!=",doc.get("name")],"docstatus":0,"prevdoc_docname":doc_name}):
            frappe.throw(_("Not Allowed to create multiple Sales Order against Quotation <b> {} </b>.".format(doc_name)))            