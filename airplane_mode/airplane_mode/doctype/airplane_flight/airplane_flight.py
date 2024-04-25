# Copyright (c) 2024, Karan Mistry and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):

    # ON SUBMIT EVENT
    def on_submit(self):

        # CALL FUNCTION UPDATE THE STATUS OF DOC TO COMPLETED ON SUBMIT
        self.update_status_to_completed()

    # UPDATE THE STATUS OF DOC TO COMPLETED ON SUBMIT
    def update_status_to_completed(self):
        self.status = "Completed"
