// Copyright (c) 2024, Karan Mistry and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {

        if (frm.doc.status === "Booked") {
            // GET THE SEAT NUMBER
            frm.add_custom_button(__("Assign Seat"),
                () => {
                    let d = new frappe.ui.Dialog({
                        title: 'Select Seat',
                        fields: [
                            {
                                label: 'Seat Number',
                                fieldname: 'seat_number',
                                fieldtype: 'Data'
                            },
                        ],
                        primary_action_label: 'Assign',
                        primary_action(values) {
                            console.log(values);
                            frm.set_value("seat", values.seat_number)
                            frm.save()
                            d.hide();
                        }
                    });
                    d.show();
                },
                "Actions")
        }

        if (!frm.doc.gate_pass) {
            // CREATE GATE PASS
            frm.add_custom_button(__("Create Gate Pass"),
                () => {
                    let d = new frappe.ui.Dialog({
                        title: 'Create Gate Pass',
                        fields: [
                            {
                                label: 'Ticket',
                                fieldname: 'ticket',
                                fieldtype: 'Link',
                                options: "Airplane Ticket",
                                default: frm.doc.name,
                                read_only: 1,
                            },
                            {
                                label: 'Gate Number',
                                fieldname: 'gate_number',
                                fieldtype: 'Data',
                                reqd: 1,
                            },
                            {
                                label: 'Status',
                                fieldname: 'status',
                                fieldtype: 'Select',
                                options: "\nPending\nApproved\nExpired\nUsed",
                                reqd: 1,
                                default: "Pending",
                            },
                            {
                                label: 'Start Date',
                                fieldname: 'start_date',
                                fieldtype: 'Date',
                                default: "Today",
                                reqd: 1,
                            },
                            {
                                label: 'End Date',
                                fieldname: 'end_date',
                                fieldtype: 'Date',
                                default: "Today",
                                reqd: 1,
                            },
                            {
                                label: 'Purpose',
                                fieldname: 'purpose',
                                fieldtype: 'Data',
                                default: "Airplane Ticket",
                                reqd: 1,
                            },
                            {
                                label: 'Remarks',
                                fieldname: 'remarks',
                                fieldtype: 'Small Text',
                            },
                        ],
                        primary_action_label: 'Create',
                        primary_action(values) {
                            console.log(values);
                            frappe.call({
                                method: "frappe.client.insert",
                                args: {
                                    doc: {
                                        doctype: "Gate Pass",
                                        ticket: values.ticket,
                                        gate_number: values.gate_number,
                                        status: values.status,
                                        start_date: values.start_date,
                                        end_date: values.end_date,
                                        purpose: values.purpose,
                                        remarks: values.remarks || "",
                                    }
                                },
                                callback: function (response) {
                                    var response_message = response.message;
                                    if (response_message) {
                                        // console.log(response_message)
                                        frappe.show_alert({
                                            message: __('Gate Pass is Created Successfully!'),
                                            indicator: 'green'
                                        }, 5);
                                        frm.set_value("gate_pass", response_message.name);
                                        frm.save();
                                    }
                                }
                            })
                            d.hide();
                        }
                    });
                    d.show();
                },
                "Actions");
        }


        // CHECK IF THE PAYMENT ALREADY EXIST OR NOT
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Ticket Payment",
                filters: { ticket: frm.doc.name },
                fields: ["name"]
            },
            callback: function (response) {
                var response_message = response.message

                if (response_message == [] || response_message == "" || response_message == null) {
                    // ADD CREATE PAYMENT BUTTON
                    frm.add_custom_button(__("Create Payment"),
                        () => {
                            let d = new frappe.ui.Dialog({
                                title: 'Create Payment',
                                fields: [
                                    {
                                        label: 'Ticket',
                                        fieldname: 'ticket',
                                        fieldtype: 'Link',
                                        options: "Airplane Ticket",
                                        default: frm.doc.name,
                                        read_only: 1,
                                    },
                                    {
                                        label: 'Status',
                                        fieldname: 'status',
                                        fieldtype: 'Select',
                                        options: "\nPaid\nUnpaid\nPartially Paid",
                                        reqd: 1,
                                    },
                                    {
                                        label: 'Payment Method',
                                        fieldname: 'payment_method',
                                        fieldtype: 'Select',
                                        options: "\nCash\nDebit Card\nCredit Card\nUPI\nBank Draft",
                                        reqd: 1,
                                    },
                                    {
                                        label: 'Amount Paid',
                                        fieldname: 'amount_paid',
                                        fieldtype: 'Currency',
                                        default: frm.doc.total_amount,
                                        reqd: 1,
                                    },
                                ],
                                primary_action_label: 'Assign',
                                primary_action(values) {
                                    console.log(values);
                                    frappe.call({
                                        method: "frappe.client.insert",
                                        args: {
                                            doc: {
                                                doctype: "Ticket Payment",
                                                ticket: values.ticket,
                                                status: values.status,
                                                payment_method: values.payment_method,
                                                amount_paid: values.amount_paid,
                                            }
                                        },
                                        callback: function (response) {
                                            var response_message = response.message;
                                            if (response_message) {
                                                console.log(response_message)
                                                frappe.show_alert({
                                                    message: __('Payment is Created Successfully!'),
                                                    indicator: 'green'
                                                }, 5);

                                                if (frm.is_dirty()) {
                                                    frm.save()
                                                } else {
                                                    frm.reload_doc()
                                                }
                                            }
                                        }
                                    })
                                    d.hide();
                                }
                            });
                            d.show();
                        },
                        "Actions")
                }
            }
        });
    },
});
