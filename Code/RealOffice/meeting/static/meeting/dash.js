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

    	window.localStorage.removeItem("realoffice_token");

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

    // Add new person form
    $("#add_new_person").on("click", function(){
    	$.ajax({
	    	url: '/person/add/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			data: {
				'name': $("#new_person_name").val(),
				'email': $("#new_person_email").val(),
			},
			success: function(data, textStatus, jqXHR){
	    		if('error' in data){
		    		$("#status_heading").html("Error: " + data['error']);
		    		$('#statusModal').modal('show');
	    		}
				else{
		    		$("#status_heading").html("Success!!");
		    		$('#statusModal').modal('show');
				}			
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
	    		$("#status_heading").html("Failed to add person!");
	    		$('#statusModal').modal('show');
			}    		
    	});    	
    });

    // Check if organizer exists
    $("#new_meeting_organizer").on("change", function(){
    	$.ajax({
	    	url: '/person/check/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			data: {
				'persons': $("#new_meeting_organizer").val(),
			},
			success: function(data, textStatus, jqXHR){
	    		if(data['unknown'].length == 0 && data['ambiguous'].length == 0)
		    		$('#new_meeting_organizer').css('box-shadow', '0px 0px 6px green');
				else{
		    		$('#new_meeting_organizer').css('box-shadow', '0px 0px 6px red');
		    		$("#status_heading").html("Unkown Names: " + data['unknown'] + 
		    			"<br>" + "Ambiguous Names: " + data['ambiguous']);
		    		$('#statusModal').modal('show');
				}			
			},
			error: function(jqXHR, textStatus, errorThrown){
	    		$('#new_meeting_organizer').css('box-shadow', '0px 0px 6px red');
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
	    		$("#status_heading").html("Failed to check person!");
	    		$('#statusModal').modal('show');
			}    		
    	});    	
    });

    // Check if participants exist
    $("#new_meeting_participants").on("change", function(){
    	$.ajax({
	    	url: '/person/check/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			data: {
				'persons': $("#new_meeting_participants").val(),
			},
			success: function(data, textStatus, jqXHR){
	    		if(data['unknown'].length == 0 && data['ambiguous'].length == 0)
		    		$('#new_meeting_participants').css('box-shadow', '0px 0px 6px green');
				else{
		    		$('#new_meeting_participants').css('box-shadow', '0px 0px 6px red');
		    		$("#status_heading").html("Unkown Names: " + data['unknown'] + 
		    			"<br>" + "Ambiguous Names: " + data['ambiguous']);
		    		$('#statusModal').modal('show');
				}			
			},
			error: function(jqXHR, textStatus, errorThrown){
	    		$('#new_meeting_participants').css('box-shadow', '0px 0px 6px red');
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
	    		$("#status_heading").html("Failed to check person!");
	    		$('#statusModal').modal('show');
			}    		
    	});    	
    });    

    // Add meeting form
    $("#addMeetingBtn").on("click", function(){
    	console.log("Triggered");
    	$.ajax({
	    	url: '/meeting/add/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			data: {
				'name': 		$("#new_meeting_name").val(),
				'organizer': 	$("#new_meeting_organizer").val(), 
				'venue': 		$("#new_meeting_venue").val(), 
				'participants': $("#new_meeting_participants").val(), 
				'date': 		$("#new_meeting_date").val(), 
				'stime': 		$("#new_meeting_stime").val(), 
				'etime': 		$("#new_meeting_etime").val(),
				'workflow': 	$("#new_meeting_workflow").val()
			},
			success: function(data, textStatus, jqXHR){
	    		if('error' in data){
		    		$("#status_heading").html("Error: " + data['error']);
		    		$('#statusModal').modal('show');
	    		}
	    		else{
		    		$("#status_heading").html("Success!!");
		    		$('#statusModal').modal('show');	    			
	    		}
			},
			error: function(jqXHR, textStatus, errorThrown){
	    		$('#participants').css('box-shadow', '0px 0px 6px red');
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
	    		$("#status_heading").html("Failed to add meeting!");
	    		$('#statusModal').modal('show');
			}    		    		
    	});
    });

});