# Copyright (c) 2024, Karan Mistry and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document


class AirplaneTicket(Document):

    # BEFORE SAVE EVENT
    def before_save(self):

        # IF THE DOC IS NEW
        if self.is_new():

            # CALL FUNCTION CHECK THE AIRPLANE CAPACITY
            self.check_airplane_capacity()

            # CALL THE GENERATE SEAT FUNCTION
            self.generate_seat()

    # VALIDATE EVENT
    def validate(self):

        # CALL FUNCTION CHECK THE GATE PASS
        self.check_gate_pass()

        # CALL FUNCTION REMOVE DUPLICATE ADD ON ITEMS
        self.remove_duplicate_add_ons()

        # CALL FUNCTION CALCULATE TOTAL AMOUNT
        self.calculate_total_amount()

    # BEFORE SUBMIT EVENT
    def before_submit(self):

        # CALL FUNCTION CHECK THE STATUS IS BOARDED BEFORE SUBMIT
        self.check_the_status_equal_to_booked()

    # CHECK THE STATUS IS BOARDED BEFORE SUBMIT
    def check_the_status_equal_to_booked(self):
        if self.status != "Boarded":
            frappe.throw(
                f'Please Set The Status To "Boarded" Before Submitting The Document!'
            )

    # REMOVE DUPLICATE ADD ON ITEMS
    def remove_duplicate_add_ons(self):

        # DEFINE VARIABLES
        unique_items = {}
        unique_data = []
        add_ons = self.add_ons

        # IF ADD ONS ARE ADDED
        if add_ons:

            # FOR ROW IN CHILD TABLE
            for item in add_ons:
                item_name = item.item

                # IF ITEM NAME IS NOT IN UNIQUE ITEMS DICT APPEND IT TO UNIQUE DATA LIST
                if item_name not in unique_items:
                    unique_items[item_name] = True
                    unique_data.append(item)

        # UPDATE THE CHILD TABLE VALUE AFTER REMOVING DUPLICATE
        self.add_ons = unique_data

    # CALCULATE THE TOTAL AMOUNT
    def calculate_total_amount(self):

        # DEFINE VARIABLES
        flight_price = self.flight_price if self.flight_price else 0
        add_ons = self.add_ons
        total_add_on_amount = 0

        # IF ADD ONS ARE ADDED
        if add_ons:

            # FOR ROW IN CHILD TABLE
            for item in add_ons:

                # SET THE ADD ON AMOUNT
                total_add_on_amount += item.amount if item.amount else 0

        # SET THE TOTAL AMOUNT
        self.total_amount = flight_price + total_add_on_amount

    # GENERATE SEAT NUMBER
    def generate_seat(self):

        # GENERATE RANDOM NUMBER
        random_integer = random.randint(1, 100)

        # GENERATE RANDOM ALPHABET FROM A TO E
        random_alphabet = random.choice("ABCDE")

        # GENERATE SEAT NUMBER
        seat = f"{random_integer}{random_alphabet}"

        # SET THE SEAT NUMBER
        self.seat = seat

    # CHECK THE AIRPLANE CAPACITY
    def check_airplane_capacity(self):

        # DEFINE VARIABLES NAD GET VALUES FROM REQUIRED DOCTYPE
        airplane_flight = self.flight
        flight_name = frappe.db.get_value(
            "Airplane Flight", airplane_flight, "airplane"
        )
        flight_capacity = frappe.db.get_value("Airplane", flight_name, "capacity")

        # GET THE LIST OF TICKETS AS PER THE CURRENT AIRPLANE FLIGHT
        get_all_tickets = frappe.get_list(
            "Airplane Ticket",
            filters={"flight": airplane_flight},
            fields=["name"],
        )

        # THROW ERROR IF THE NO OF TICKETS ARE MORE THAN THE SELECTED AIRPLANE FLIGHT
        if len(get_all_tickets) >= flight_capacity:
            frappe.throw("All The Tickets of The Selected Flight Has Been Booked!")

    # CHECK THE GATE PASS
    def check_gate_pass(self):
        if self.status == "Boarded" and (
            self.gate_pass == None or self.gate_pass == ""
        ):
            frappe.throw("""You cannot get "Boarded" without the "Gate Pass" please create one!""")
