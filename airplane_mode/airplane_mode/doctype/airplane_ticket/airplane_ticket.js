// Copyright (c) 2024, Karan Mistry and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {

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

                        frm.set_value("seat",values.seat_number)
                        frm.save()

                        d.hide();
                    }
                });

                d.show();
            },
            "Actions")
    },
});
