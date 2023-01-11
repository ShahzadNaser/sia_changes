import frappe
from frappe import _

def before_save(doc, method):
    validate_so(doc)
    validate_sq(doc)
def validate_sq(doc):
    if doc.get("items") and (doc.items[0].get("supplier_quotation") or doc.items[len(doc.get("items"))-1].get("supplier_quotation")):
        doc_name = doc.items[0].get("supplier_quotation") or doc.items[len(doc.get("items"))-1].get("supplier_quotation")
        if doc_name and frappe.db.get_value("Purchase Order Item",{"parent":["!=",doc.get("name")],"docstatus":0,"supplier_quotation":doc_name}):
            frappe.throw(_("Not Allowed to create multiple Purchase Orders against Supplier Quotation <b> {} </b>.".format(doc_name)))            
            
def validate_so(doc):
    if doc.get("items") and (doc.items[0].get("sales_order") or doc.items[len(doc.get("items"))-1].get("sales_order")):
        doc_name = doc.items[0].get("sales_order") or doc.items[len(doc.get("items"))-1].get("sales_order")
        if doc_name and frappe.db.get_value("Sales Invoice Item",{"parent":["!=",doc.get("name")],"docstatus":0,"sales_order":doc_name}):
            frappe.throw(_("Not Allowed to create multiple Purchase Orders against Sales Order <b> {} </b>.".format(doc_name))) 