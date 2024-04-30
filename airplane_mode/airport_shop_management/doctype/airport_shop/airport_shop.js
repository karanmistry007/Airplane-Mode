// Copyright (c) 2024, Karan Mistry and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
    refresh(frm) {
        // SET DEFAULT RENT AMOUNT
        if (!frm.doc.rent_amount) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Airport Shop Settings",
                    name: "Airport Shop Settings"
                },
                callback: function (res) {
                    var shop_settings_doc = res.message
                    if (shop_settings_doc) {
                        frm.set_value("rent_amount", shop_settings_doc.default_rent_amount)
                    }
                }
            })
        }
    },
});
