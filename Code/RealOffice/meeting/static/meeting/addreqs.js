$(document).ready(function(){
	var my_token = window.localStorage.getItem("realoffice_token");
	if(window.localStorage.getItem("username") != null){
		$('#reminderId').css("display", "inline");
		$('#user').html(window.localStorage.getItem("username"));
	}
	var meeting_name = window.location.href.split('meeting=')[1]
	$("#add_new_requirement").on("click", function(){
    	$.ajax({
	    	url: '/requirement'+'/add/',
	    	method: 'POST',
			data: {
				'item': $("#new_person_item").val(),
				'qty': $("#new_person_qty").val(),
				'cost': $("#new_person_cost").val(),
				'prereqFor'	: meeting_name,
				'orderDetails': $("#orderDetails").val()
			},
			success: function(data, textStatus, jqXHR){
		    	location.reload();		
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
	    		$("#status_heading").html("Failed to add requirement!");
	    		$('#statusModal').modal('show');
			}    		
    	});    	
    });

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

    $("#add_new_reminder").on("click", function(){
    	$.ajax({
	    	url: '/reminder'+'/add/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			data: {
				'recipient': $("#new_person_recipient").val(),
				'recipientType': $("#new_person_type").val(),
				'purpose': $("#new_person_purpose").val(),
				'notificationsFor'	: meeting_name
			},
			success: function(data, textStatus, jqXHR){
		    	location.reload();	
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
	    		$("#status_heading").html("Failed to add reminder!");
	    		$('#statusModal').modal('show');
			}    		
    	});    	
    });
});