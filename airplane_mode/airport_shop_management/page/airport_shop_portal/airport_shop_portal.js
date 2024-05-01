frappe.pages['airport-shop-portal'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});

	// HIDING THE TITLE DIV
	// let parent_title_div = document.getElementsByClassName("page-head");
	// parent_title_div[0].setAttribute("id", "parent-title");
	// let title_id = document.getElementById("parent-title");
	// title_id.style.display = "none";

	// PAGE TITLE
	page.set_title("Airport Shop Portal");


	$(
		frappe.render_template("airport_shop_portal", {
			// ENTER THE DATA AS OBJECT FOR JINJA //
		})
	).appendTo(page.body);
	// END RENDER THE PAGE //

	// CALL RENDER THE SHOP CARD FUNCTION
	render_shop_cards()

	// RENDER THE SHOP CARD FUNCTION
	function render_shop_cards() {
		var main_data = [];
		$.ajax({
			url: `${window.location.origin}/api/resource/Airport%20Shop?fields=["name","shop_name","shop_number","banner_image","airport","status","tenant_name","route"]&order_by=status%20asc&limit_page_length=none`,

			// SUCCESS RESPONSE //
			success: function (response) {
				main_data = response.data

				if (main_data) {
					$.each(main_data, function (index, item) {
						console.log(item)
						var color = "#2376d0bf"
						if (item.status == "Available For Lease") {
							color = "#2376d0bf"
						}
						if (item.status == "On Lease") {
							color = "#0a720a9c"
						}
						if (item.status == "Closed") {
							color = "#ad1818bf"
						}
						$(".cards-container").append(`
							<div class="card 1 p-4" key=${index}>
								<h3>
									Shop : ${item.name}
									</h2>
									<h5>
										Shop Name: ${item.shop_name}
									</h5>
									<h5>
										Shop Number: ${item.shop_number}
									</h5>
									<h5>
										Status: 
										<span style="padding: 2px 5px;border-radius: 10px;font-size: 14px;color: white;background-color:${color};">
											${item.status} 
										</span>
									</h5>
									<h5>
										Airport: ${item.airport}
									</h5>
									<h5>
										Tenant Name: ${item.tenant_name}
									</h5>
									<a href="../${item.route}">
										<button class="btn btn-primary">
											View Shop Details
										</button>
									</a>
								</div>
								`)
					})
				}
			}
		});
	}

}
