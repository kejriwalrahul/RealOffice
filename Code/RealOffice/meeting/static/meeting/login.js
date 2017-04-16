$(document).ready(function() {
	
	var my_token = "";

	$("#loginbtn").on("click", function(){
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
				window.localStorage.setItem('realoffice_token', data['token']);			
				window.location.href = '/dash';				
			}
		});

	});

});