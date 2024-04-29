# Copyright (c) 2024, Karan Mistry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GatePass(Document):

    # ON TRASH EVENT
    def on_trash(self):

        # CALL FUNCTION REMOVE THE LINKED GATE PASS
        self.remove_link_gate_pass()

    # REMOVE THE LINKED GATE PASS
    def remove_link_gate_pass(self):
        frappe.db.set_value("Airplane Ticket", self.ticket, "gate_pass", "")
