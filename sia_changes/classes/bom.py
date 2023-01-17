import frappe
from frappe import _
from frappe.utils import cint, cstr, flt, today
from erpnext.manufacturing.doctype.bom.bom import BOM

class CustomBOM(BOM):
    def validate_materials(self):
        """Validate raw material entries"""

        if not self.get("items"):
            frappe.throw(_("Raw Materials cannot be blank."))
        check_list = []
        for m in self.get("items"):
            if m.bom_no:
                validate_bom_n(m.item_code, m.bom_no)
            if flt(m.qty) <= 0:
                frappe.throw(_("Quantity required for Item {0} in row {1}").format(m.item_code, m.idx))
            check_list.append(m)

def validate_bom_n(item, bom_no):
	"""Validate BOM No of sub-contracted items"""
	bom = frappe.get_doc("BOM", bom_no)
	if not bom.is_active:
		frappe.throw(_("BOM {0} must be active").format(bom_no))
	if False and bom.docstatus != 1:
		if not getattr(frappe.flags, "in_test", False):
			frappe.throw(_("BOM {0} must be submitted").format(bom_no))
	if item:
		rm_item_exists = False
		for d in bom.items:
			if d.item_code.lower() == item.lower():
				rm_item_exists = True
		for d in bom.scrap_items:
			if d.item_code.lower() == item.lower():
				rm_item_exists = True
		if (
			bom.item.lower() == item.lower()
			or bom.item.lower() == cstr(frappe.db.get_value("Item", item, "variant_of")).lower()
		):
			rm_item_exists = True
		if not rm_item_exists:
			frappe.throw(_("BOM {0} does not belong to Item {1}").format(bom_no, item))
