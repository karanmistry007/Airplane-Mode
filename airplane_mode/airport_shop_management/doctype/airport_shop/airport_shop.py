# Copyright (c) 2024, Karan Mistry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import add_months


class AirportShop(Document):

    # BEFORE SAVE EVENT
    def before_save(self):

        # CALL FUNCTION CHECK CONTRACT DATE
        self.check_contract_date()

        # CALL FUNCTION SET DEFAULT RENT AMOUNT
        self.set_default_rent_amount()

    # SET DEFAULT RENT AMOUNT
    def set_default_rent_amount(self):
        if self.rent_amount == None or self.rent_amount == 0:
            default_rent_amount = frappe.get_value(
                "Airport Shop Settings", "Airport Shop Settings", "default_rent_amount"
            )
            self.rent_amount = default_rent_amount

    # CHECK CONTRACT DATE
    def check_contract_date(self):
        contract_start_date = self.contract_start_date
        contract_end_date = self.contract_end_date
        date_after_month = add_months(contract_start_date, 1)
        if contract_end_date < date_after_month:
            frappe.throw("The contract should be more than 1 month!	")
