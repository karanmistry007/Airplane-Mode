// Copyright (c) 2024, Karan Mistry and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
    refresh(frm) {
        // SET THE VIEW WEBSITE LINK
        var website_link = frm.doc.website
        if (website_link) {
            frm.add_web_link(website_link, "Visit Website");
        }
    },
});
