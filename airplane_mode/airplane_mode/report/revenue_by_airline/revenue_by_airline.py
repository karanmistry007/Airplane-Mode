# Copyright (c) 2024, Karan Mistry and contributors
# For license information, please see license.txt

import frappe


# MAIN FUNCTION
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


# GET COLUMNS
def get_columns():
    return [
        {
            "fieldname": "airline",
            "label": "Airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": "200",
        },
        {
            "fieldname": "revenue",
            "label": "Revenue",
            "fieldtype": "Currency",
            "width": "200",
        },
    ]


# GET ALL THE DATA
def get_data(filters):
    airline_revenue = {}
    data = []

    # FETCH LIST OF AIRLINES
    airlines = frappe.db.get_all("Airline", fields=["name"])
    for airline in airlines:
        airline_revenue[airline.name] = 0

    # FETCH ALL THE AIRPLANE TICKETS
    tickets = frappe.db.get_all(
        "Airplane Ticket", filters=filters, fields=["flight", "total_amount"]
    )

    # CALCULATE REVENUE FOR ALL THE AIRLINES
    for ticket in tickets:
        total_amount = ticket.total_amount
        flight_id = ticket.flight
        airline = get_airline_from_flight(flight_id)
        if airline and airline in airline_revenue:
            airline_revenue[airline] += total_amount

    # CONVERT THE DATA INTO REPORT FORMAT
    for airline, revenue in airline_revenue.items():
        data.append({"airline": airline, "revenue": revenue})

    return data


# GET THE AIRLINE NAME FROM FLIGHT
def get_airline_from_flight(flight_id):
    if flight_id:
        airplane = frappe.db.get_value("Airplane Flight", flight_id, "airplane")
        if airplane:
            return frappe.db.get_value("Airplane", airplane, "airline")
    return None
