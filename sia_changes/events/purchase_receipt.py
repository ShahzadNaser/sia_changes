import frappe
from frappe import _

def before_save(doc, method):
    validate_po(doc)
            
def validate_po(doc):
    if doc.get("items") and (doc.items[0].get("purchase_order") or doc.items[len(doc.get("items"))-1].get("purchase_order")):
        doc_name = doc.items[0].get("purchase_order") or doc.items[len(doc.get("items"))-1].get("purchase_order")
        if doc_name and frappe.db.get_value("Purchase Receipt Item",{"parent":["!=",doc.get("name")],"docstatus":0,"purchase_order":doc_name}):
            frappe.throw(_("Not Allowed to create multiple Purchase Receipts against Purchase Order <b> {} </b>.".format(doc_name))) 