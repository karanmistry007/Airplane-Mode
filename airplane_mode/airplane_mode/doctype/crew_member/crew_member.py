# Copyright (c) 2024, Karan Mistry and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CrewMember(Document):

    # BEFORE SAVE EVENT
    def before_save(self):

        # CALL FUNCTION SET FULL NAME
        self.set_full_name()

    # FUNCTION SET FULL NAME
    def set_full_name(self):
        # DEFINE VARIABLES
        first_name = self.first_name
        last_ame = self.last_name

        # SET FULL NAME
        self.full_name = (first_name if first_name else "") + (
            " " + last_ame if last_ame else ""
        )
