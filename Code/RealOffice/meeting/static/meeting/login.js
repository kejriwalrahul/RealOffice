$(document).ready(function() {
	
	var my_token = "";

	$("#loginbtn").on("click", function(){
		
		function gotoDash(){
			window.localStorage.setItem('token', my_token);			
			
		};

		$.ajax({
			url: "/login/",
			dataType: "json",
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				$("#failLogInModal").modal("show");
			},
			method: "POST",
			data: {
				username: $("#name").val(),
				password: $("#password").val(),
			},
			success: function(data, textStatus, jqXHR){
				console.log("Success");
				my_token = data['token'];
				gotoDash();
			}
		});

	});

});