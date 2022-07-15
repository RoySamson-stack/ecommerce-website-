//create an onlick for the update-btn to update the cart
$(document).ready(function() {
		$(".update-cart").click(function() {
				var product_id = $(this).data("product");
				var action = $(this).data("add");
				$.ajax({
						url: "/update_item/",
						method: "POST",
						data: {
								id: product_id,
								action: action
						},
						success: function(data) {
							console.log(data);
								location.reload();
						}
				});
		});
}
);