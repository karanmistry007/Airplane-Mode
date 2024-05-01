# Copyright (c) 2024, Karan Mistry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_months
from frappe.utils.data import today


class AirportShopRent(Document):

    # BEFORE SAVE EVENT
    def before_save(self):

        # CALL FUNCTION CHECK SHOP STATUS
        self.check_shop_status()
        if self.is_new():

            # CALL FUNCTION SET THE PAYMENT DATE
            self.check_payment_date()

    # BEFORE SUBMIT EVENT
    def before_submit(self):
        self.check_status_before_submit()

    # CHECK SHOP STATUS
    def check_shop_status(self):
        shop = self.shop
        shop_status = frappe.db.get_value("Airport Shop", shop, "status")
        if shop_status != "On Lease":
            frappe.throw("""The "Airport Shop" is not On Lease!""")

    # SET THE PAYMENT DATE
    def check_payment_date(self):
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

    # CHECK STATUS BEFORE SUBMIT
    def check_status_before_submit(self):
        if self.status != "Paid":
            frappe.throw("""You cannot submit without "Paid" Status!""")


@frappe.whitelist()
# RENT REMINDER SCHEDULAR EVENT
def send_rent_reminder():
    rent_reminder = frappe.db.get_value(
        "Airport Shop Settings", "Airport Shop Settings", "enable_rend_reminders"
    )
    if rent_reminder == 1:
        pending_rent_list = []
        current_date = today()
        shop_list = frappe.db.get_all(
            "Airport Shop",
            filters={"status": "On Lease"},
            fields=[
                "name",
                "shop_name",
                "airport",
                "tenant_name",
                "email",
                "contract_start_date",
                "contract_end_date",
                "rent_amount",
            ],
        )

        for shop in shop_list:
            last_payed_doc_list = frappe.db.get_list(
                "Airport Shop Rent",
                filters={
                    "shop": shop.name,
                    "status": "Paid",
                },
                fields=["name", "to_date"],
                order_by="to_date desc",
            )
            # print(last_payed_doc)

            if last_payed_doc_list:
                last_payed_doc = last_payed_doc_list[0]
                if getdate(last_payed_doc.to_date) < getdate(current_date):
                    pending_rent_list.append(
                        {
                            "tenant_name": shop.tenant_name,
                            "tenant_email": shop.email,
                            "to_date": last_payed_doc.to_date,
                            "rent_amount": shop.rent_amount,
                            "shop": shop.name,
                            "shop_name": shop.shop_name,
                            "airport": shop.airport,
                        }
                    )

            else:
                pending_rent_list.append(
                    {
                        "tenant_name": shop.tenant_name,
                        "tenant_email": shop.email,
                        "to_date": shop.contract_start_date,
                        "rent_amount": shop.rent_amount,
                        "shop": shop.name,
                        "shop_name": shop.shop_name,
                        "airport": shop.airport,
                    }
                )

        for data in pending_rent_list:
            recipient = data["tenant_email"] or ""
            subject = "Rent Reminder!"
            message = f"""
    <div class="message">
        <p>Hello <b>{data["tenant_name"]}</b>,</br>
            Your Rent Amount <b>{data["rent_amount"]}</b> has been pending from <b>{data["to_date"]}</b> for your shop
            <b>{data["shop_name"]}</b> with id <b>{data["shop"]}</b> in Airport <b>{data["airport"]}</b> Please Kindly Pay
            Your Rent.</br>
            Thank You.
        </p>
    </div>
    <div class="content">
        <p>
            Shop: {data["tenant_name"]}
        </p>
        <p>
            Shop Name: {data["shop_name"]}
        </p>
        <p>
            Airport: {data["airport"]}
        </p>
        <p>
            Rent Amount: {data["rent_amount"]}
        </p>
    </div>"""

            frappe.sendmail(
                recipients=recipient,
                subject=subject,
                message=message,
            )
