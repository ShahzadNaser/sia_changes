# Copyright (c) 2023, Shahzadnaser and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import random_string, now


class PermissionsMigrator(Document):
	def before_submit(self):
		self.transfer_role_prem()
		self.transfer_page_reports()

	def transfer_role_prem(self):
		frappe.db.sql("""
			INSERT INTO `tabDocPerm` (`name`,`role`,`modified_by`,`owner`,`docstatus`,`parent`,`parentfield`,`parenttype`,`idx`,`permlevel`,`match`,`read`,`write`,`create`,`submit`,`cancel`,`delete`,`amend`,`report`,`export`,`import`,`share`,`print`,`email`,`if_owner`,`select`,`set_user_permissions`) 
			SELECT 
				concat(`tabDocPerm`.`name`,'{}') as name,
				'{}' as role,
				`tabDocPerm`.`modified_by`,
				`tabDocPerm`.`owner`,
				`tabDocPerm`.`docstatus`,
				`tabDocPerm`.`parent`,
				`tabDocPerm`.`parentfield`,
				`tabDocPerm`.`parenttype`,
				`tabDocPerm`.`idx`,
				`tabDocPerm`.`permlevel`,
				`tabDocPerm`.`match`,
				`tabDocPerm`.`read`,
				`tabDocPerm`.`write`,
				`tabDocPerm`.`create`,
				`tabDocPerm`.`submit`,
				`tabDocPerm`.`cancel`,
				`tabDocPerm`.`delete`,
				`tabDocPerm`.`amend`,
				`tabDocPerm`.`report`,
				`tabDocPerm`.`export`,
				`tabDocPerm`.`import`,
				`tabDocPerm`.`share`,
				`tabDocPerm`.`print`,
				`tabDocPerm`.`email`,
				`tabDocPerm`.`if_owner`,
				`tabDocPerm`.`select`,
				`tabDocPerm`.`set_user_permissions`
			FROM 
				`tabDocPerm`
			WHERE `tabDocPerm`.role='{}';
        """.format(random_string(2), self.get("to_role"),self.get("from_role")))

		frappe.db.sql("""
			INSERT INTO `tabCustom DocPerm` (`name`,`role`,`modified_by`,`owner`,`docstatus`,`idx`,`parent`,`if_owner`,`permlevel`,`select`,`read`,`write`,`create`,`delete`,`submit`,`cancel`,`amend`,`report`,`export`,`import`,`set_user_permissions`,`share`,`print`,`email`,`_user_tags`,`_comments`,`_assign`,`_liked_by`) 
   			SELECT 
				concat(`tabCustom DocPerm`.`name`,'{}') as name,
				'{}' as role,
				`tabCustom DocPerm`.`modified_by`,
				`tabCustom DocPerm`.`owner`,
				`tabCustom DocPerm`.`docstatus`,
				`tabCustom DocPerm`.`idx`,
				`tabCustom DocPerm`.`parent`,
				`tabCustom DocPerm`.`if_owner`,
				`tabCustom DocPerm`.`permlevel`,
				`tabCustom DocPerm`.`select`,
				`tabCustom DocPerm`.`read`,
				`tabCustom DocPerm`.`write`,
				`tabCustom DocPerm`.`create`,
				`tabCustom DocPerm`.`delete`,
				`tabCustom DocPerm`.`submit`,
				`tabCustom DocPerm`.`cancel`,
				`tabCustom DocPerm`.`amend`,
				`tabCustom DocPerm`.`report`,
				`tabCustom DocPerm`.`export`,
				`tabCustom DocPerm`.`import`,
				`tabCustom DocPerm`.`set_user_permissions`,
				`tabCustom DocPerm`.`share`,
				`tabCustom DocPerm`.`print`,
				`tabCustom DocPerm`.`email`,
				`tabCustom DocPerm`.`_user_tags`,
				`tabCustom DocPerm`.`_comments`,
				`tabCustom DocPerm`.`_assign`,
				`tabCustom DocPerm`.`_liked_by`
			FROM 
				`tabCustom DocPerm`
			WHERE `tabCustom DocPerm`.role='{}';
		""".format(random_string(2), self.get("to_role"),self.get("from_role")))
	def transfer_page_reports(self):
		frappe.db.sql("""
			INSERT INTO `tabHas Role` (name,role,modified_by,owner,docstatus,idx,parent,parentfield,parenttype) select 
				concat(`tabHas Role`.`name`,'{}') as name,
				'{}' as role,
				`tabHas Role`.`modified_by`,
				`tabHas Role`.`owner`,
				`tabHas Role`.`docstatus`,
				`tabHas Role`.`idx`,
				`tabHas Role`.`parent`,
				`tabHas Role`.`parentfield`,
				`tabHas Role`.`parenttype`
			FROM 
				`tabHas Role`
			WHERE `tabHas Role`.role='{}';
		""".format(random_string(2), self.get("to_role"),self.get("from_role")))