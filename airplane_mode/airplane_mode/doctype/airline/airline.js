// Copyright (c) 2024, Karan Mistry and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
    refresh(frm) {
        // SET THE VIEW WEBSITE LINK
        if (frm.doc.website) {
            var sidebar = frm.sidebar.user_actions;
            sidebar.removeClass('hidden');
            sidebar.append(`<a href="${frm.doc.website}">Visit Website</a>`);
        }
    },
});
