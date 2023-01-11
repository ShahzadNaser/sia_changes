import frappe
from frappe import _

def before_save(doc, method):
    if doc.get("items") and (doc.items[0].get("against_sales_order") or doc.items[len(doc.get("items"))-1].get("against_sales_order")):
        doc_name = doc.items[0].get("against_sales_order") or doc.items[len(doc.get("items"))-1].get("against_sales_order")
        if doc_name and frappe.db.get_value("Delivery Note Item",{"parent":["!=",doc.get("name")],"docstatus":0,"against_sales_order":doc_name}):
            frappe.throw(_("Not Allowed to create multiple Delivery Notes against Sales Order <b> {} </b>.".format(doc_name)))            