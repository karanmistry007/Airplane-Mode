import frappe


# CHECK THE STATUS IS BOARDED BEFORE SUBMIT
def check_the_status_equal_to_booked(doc, event):
    if doc.status != "Boarded":
        frappe.throw(
            f'Please Set The Status To "Boarded" Before Submitting The Document!'
        )
