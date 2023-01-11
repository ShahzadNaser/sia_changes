import frappe
from frappe import _

def before_save(doc, method):
    validate_so(doc)
    validate_dn(doc)
def validate_so(doc):
    if doc.get("items") and (doc.items[0].get("sales_order") or doc.items[len(doc.get("items"))-1].get("sales_order")):
        doc_name = doc.items[0].get("sales_order") or doc.items[len(doc.get("items"))-1].get("sales_order")
        if doc_name and frappe.db.get_value("Sales Invoice Item",{"parent":["!=",doc.get("name")],"docstatus":0,"sales_order":doc_name}):
            frappe.throw(_("Not Allowed to create multiple Sales Invoices against Sales Order <b> {} </b>.".format(doc_name)))            
            
def validate_dn(doc):
    if doc.get("items") and (doc.items[0].get("delivery_note") or doc.items[len(doc.get("items"))-1].get("delivery_note")):
        doc_name = doc.items[0].get("delivery_note") or doc.items[len(doc.get("items"))-1].get("delivery_note")
        if doc_name and frappe.db.get_value("Sales Invoice Item",{"parent":["!=",doc.get("name")],"docstatus":0,"delivery_note":doc_name}):
            frappe.throw(_("Not Allowed to create multiple Sales Invoices against Delivery Note <b> {} </b>.".format(doc_name))) 