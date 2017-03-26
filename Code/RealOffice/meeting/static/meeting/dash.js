$(document).ready(function(){
	var my_token = window.localStorage.getItem("token");

    // page is now ready, initialize the calendar...
    $('#calendar').fullCalendar({
	    contentHeight: window.innerHeight*0.61,
	    handleWindowResize: true
    });

    // Load User Info
    $('#loadingModal').modal('show');
    var my_token = window.localStorage.getItem('realoffice_token');
    if(my_token == null){
	    $('#loadingModal').modal('hide');
    	$("#status_heading").html("You are not logged in!");
    	$('#statusModal').modal('show');
    }
    else{
	    $.ajax({
	    	url: '/user/usrdash/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			success: function(data, textStatus, jqXHR){
				console.log("Success");
	    		$('#loadingModal').modal('hide');
				$("#user").html(data['user'])
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				console.log(errorThrown);
	    		$('#loadingModal').modal('hide');
		    	$("#status_heading").html("Failure in fetching your information!");
		    	$('#statusModal').modal('show');
			}
	    });    	
    }

    // Setup Log Out
    $('#logout').on("click", function(){

    	$.ajax({
    		url: "/logout/",
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
			},
			headers: {
				Authorization: "token " + my_token
			},
			method: "POST",
			success: function(data, textStatus, jqXHR){
				console.log("Success");
				window.location.href = "/";
			}
    	});
    });

    // Change Password Form
    $("#change_password").on("click", function(){

    	if( $("#newpwd").val() != $("#confirmpwd").val() ){
    		$("#status_heading").html("Passwords dont match!");
    		$('#statusModal').modal('show');
    		console.log("No req");
    	}
    	else{
			// $('#loadingModal').modal('show');
	    	$.ajax({
		    	url: '/user/change_pass/',
		    	method: 'POST',
				headers: {
					Authorization: "token " + my_token,
				},
				data: {
					old_pass: $("#oldpwd").val(),
					new_pass: $("#newpwd").val(),
				},
				success: function(data, textStatus, jqXHR){
					console.log("Success");
		    		// $('#loadingModal').modal('hide');
		    		$("#status_heading").html("Successfully changed password!");
		    		$('#statusModal').modal('show');
				},
				error: function(jqXHR, textStatus, errorThrown){
					console.log("Error!");
					console.log(errorThrown);
		    		// $('#loadingModal').modal('hide');
		    		$("#status_heading").html("Failed to change password!");
		    		$('#statusModal').modal('show');
				}    		
	    	});    		
    	}

     });

    
});