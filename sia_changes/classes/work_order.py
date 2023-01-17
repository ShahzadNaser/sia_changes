import frappe
from frappe import _
from frappe.utils import cint, cstr, flt, today
from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder
from erpnext.utilities.transaction_base import validate_uom_is_integer

class CustomWorkOrder(WorkOrder):
	def validate(self):
		self.validate_production_item()
		if self.bom_no:
			validate_bom_n(self.production_item, self.bom_no)
		self.validate_sales_order()
		self.set_default_warehouse()
		self.validate_warehouse_belongs_to_company()
		self.calculate_operating_cost()
		self.validate_qty()
		self.validate_transfer_against()
		self.validate_operation_time()
		self.status = self.get_status()

		validate_uom_is_integer(self, "stock_uom", ["qty", "produced_qty"])

		self.set_required_items(reset_only_qty=len(self.get("required_items")))

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
