# Copyright (c) 2024, Karan Mistry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_months


class AirportShopRent(Document):

    # BEFORE SAVE EVENT
    def before_save(self):

        if self.is_new():

            # CALL FUNCTION SET THE PAYMENT DATE
            self.check_payment_date()

    # SET THE PAYMENT DATE
    def check_payment_date(self):
        print("\n\n\n\n")
        shop = self.shop
        contract_start_date = frappe.db.get_value(
            "Airport Shop", shop, "contract_start_date"
        )
        contract_end_date = frappe.db.get_value(
            "Airport Shop", shop, "contract_end_date"
        )

        shop_rent_list = frappe.db.get_all(
            "Airport Shop Rent",
            filters={
                "shop": shop,
            },
            fields=["name", "from_date", "to_date"],
            order_by="to_date desc",
        )
        if shop_rent_list:
            print(shop_rent_list)
            last_shop_rent_doc = shop_rent_list[0]
            if last_shop_rent_doc.to_date == contract_end_date:
                frappe.throw(
                    """Extend the contract in "Airport Shop" to create a new "Airport Shop Rent"!"""
                )
            self.from_date = last_shop_rent_doc.to_date
            date_after_month = add_months(last_shop_rent_doc.to_date, 1)
            if date_after_month > contract_end_date:
                self.to_date = contract_end_date
            else:
                self.to_date = date_after_month

        else:
            self.from_date = contract_start_date
            self.to_date = add_months(contract_start_date, 1)

        # from_date = getdate(self.from_date)
        # to_date = getdate(self.to_date)
        # shop = self.shop
        # contract_start_date = frappe.db.get_value(
        #     "Airport Shop", shop, "contract_start_date"
        # )
        # print("\n\n\n\n\n")

        # if from_date < contract_start_date:
        #     frappe.throw(""""From Date" cannot be before "Contract Start Date"!""")

        # shop_rent_list = frappe.db.get_all(
        #     "Airport Shop Rent",
        #     filters={
        #         "shop": shop,
        #         "to_date": ["<", from_date],
        #     },
        # )
        # print(shop_rent_list)

        # if shop_rent_list:
        #     frappe.throw(
        #         """Airport Shop Rent already exists with the selected dates!"""
        #     )
