$(document).ready(function(){
	var my_token = window.localStorage.getItem("token");
	var monthNames = [
	    "January", "February", "March",
	    "April", "May", "June", "July",
	    "August", "September", "October",
	    "November", "December"
	];

	function pretty_date(date){
		date = date.substring(0, date.length-1);
		var dateObj = new Date(date);
		
		var hours = dateObj.getUTCHours();
		var minutes =  dateObj.getUTCMinutes();
		var date = dateObj.getUTCDate();
		var postfix = "th";

		if(hours < 10)	hours = "0" + hours;
		else			hours = ""  + hours; 

		if(minutes<10)  minutes = "0" + minutes;
		else 			minutes = ""  + minutes;

		if(date%10 == 1)	 	postfix = "st";
		else if(date%10 == 2)	postfix = "nd";
		else if(date%10 == 3)	postfix = "rd";

		if(date<10)		date = "0" + date;
		else 			date = ""  + date;

		postfix = "<sup>" + postfix + "</sup>"

		return hours + ":" + minutes + " hrs " + date + postfix + " " + monthNames[dateObj.getUTCMonth()] + " " + dateObj.getUTCFullYear();
	};

	function approvalToggle(meetingName, itemname){
	    $.ajax({
	    	url: '/requirement/toggle/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			data: {
				'name': meetingName,
				'item': itemname
			},
			success: function(data, textStatus, jqXHR){
				if('error' in data){
			    	$("#status_heading").html("Error: " + data['error']);
			    	$('#statusModal').modal('show');
				}
				else{
			    	$("#status_heading").html("Successfully update approval status!");
			    	$('#statusModal').modal('show');					
				}
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
		    	$("#status_heading").html("Failure in updating approval status!");
		    	$('#statusModal').modal('show');
			}
	    });
	}

    // page is now ready, initialize the calendar...
    $('#calendar').fullCalendar({
	    contentHeight: window.innerHeight*0.61,
	    handleWindowResize: true,
	    eventClick: function(event, jsevent, view){
	    	$('#view_meeting_name').html(event.title);
	    	$('#view_meeting_venue').html(event.venue);
	    	$('#view_meeting_type').html(event.type);
	    	$('#view_meeting_start').html(pretty_date(event.stime));
	    	$('#view_meeting_end').html(pretty_date(event.etime));
	    	$('#view_meeting_organizer').html(event.organizer);
	    	$('#view_meeting_participants').html(event.participants);
	    	$('#view_meeting_headcount').html(event.headcount);
	    	$('#view_meeting_createdBy').html(event.createdBy);
	    	$('#view_meeting_createdOn').html(pretty_date(event.createdOn));

	    	var new_table = "<table class='table table-bordered'>";
	    	new_table += 
	    		"<tr> \
					<th>Item</th> \
					<th>Qty</th> \
					<th>Cost</th> \
					<th>isApproved</th> \
	    		</tr>"
	    	for(var i=0; i<event.requirements.length; i++){
	    		new_table += "<tr>";
	    		new_table += "<td>" + event.requirements[i][0] + "</td>"
	    		new_table += "<td>" + event.requirements[i][1] + "</td>"
	    		new_table += "<td>" + event.requirements[i][2] + "</td>"
	    		
	    		var checked = "";
	    		if(event.requirements[i][3] == true)
	    			checked = "checked";
	    		
	    		new_table += 
	    		"<td style='padding-bottom:0px'> \
	    			<div class='checkbox' style='margin:0px'> \
  						<label><input class='approve_toggle' type='checkbox' " + checked + "></label>\
					</div>\
				</td>"
	    		new_table += "</tr>";
	    	}
	    	new_table += "</table>";
	    	if(event.requirements.length != 0){
	    		$('#req_container').html(new_table)
	    		$(".approve_toggle").on('click', function(){
			    	var itemname = $(this).parent().parent().parent().parent().children().first().html();
			    	var meetingName = $('#view_meeting_name').html();
			    	approvalToggle(meetingName, itemname);
			    });
	    	}
	    	else
	    		$('#req_container').html("No Requirements Yet!")

	    	if(event.status == 4)
	    		$("#reschedule_meeting").css("display", "none")
	    	else
	    		$("#reschedule_meeting").css("display", "inline")

	    	$('#viewMeetingModal').modal('show');
	    }
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
				$("#user").html(data['user']);
				console.log(data);
				var meetings = data['meetings'];
				for(var i=0; i<meetings.length; i++){
					var event = {
						title: meetings[i][0],
						start: meetings[i][1],
						end: meetings[i][2],
						venue: meetings[i][3],
						organizer: meetings[i][4],
						type: meetings[i][5],
						stime: meetings[i][1],
						etime: meetings[i][2],
						participants: meetings[i][6],
						requirements: meetings[i][7],
						headcount: meetings[i][8],
						status: meetings[i][9],
						createdBy: meetings[i][10],
						createdOn: meetings[i][11],
					}
					if(event.status == 4)
						event.color = 'green';

					$("#calendar").fullCalendar('renderEvent', event, stick=true);
				}
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

    // On click of username 
    $('#user').on('click', function(){
    	$('#settingLink').click();
    });

    // Update home
    $("#homelink").on("click", function(){
	    $.ajax({
	    	url: '/user/usrdash/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			success: function(data, textStatus, jqXHR){
				var meetings = data['meetings'];
				$("#calendar").fullCalendar('removeEvents');
				for(var i=0; i<meetings.length; i++){
					var event = {
						title: meetings[i][0],
						start: meetings[i][1],
						end: meetings[i][2],
						venue: meetings[i][3],
						organizer: meetings[i][4],
						type: meetings[i][5],
						stime: meetings[i][1],
						etime: meetings[i][2],
						participants: meetings[i][6],
						requirements: meetings[i][7],
						headcount: meetings[i][8],
						status: meetings[i][9],
						createdBy: meetings[i][10],
						createdOn: meetings[i][11],
					}

					if(event.status == 4)
						event.color = 'green';

					$("#calendar").fullCalendar('renderEvent', event, stick=true);
				}
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				console.log(errorThrown);
		    	$("#status_heading").html("Failure in updating calendar!");
		    	$('#statusModal').modal('show');
			}
	    });
    });

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
					
					$("#oldpwd").val('');
					$("#newpwd").val('');
					$("#confirmpwd").val('');
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
				
		    		$("#new_person_name").val('');
		    		$("#new_person_email").val('');
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
		    		
		    		var err_msg = ""
		    		if(data['unknown'].length != 0){
		    			err_msg += "Unkown Names: " + data['unknown'];
		    		}
		    		if(data['ambiguous'].length != 0){
		    			if(data['unknown'].length != 0) err_msg += "<br>";
		    			err_msg += "Ambiguous Names: " + data['ambiguous'];
		    		}
		    		$("#status_heading").html(err_msg);
		    		
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

					var err_msg = ""
		    		if(data['unknown'].length != 0){
		    			err_msg += "Unkown Names: " + data['unknown'];
		    		}
		    		if(data['ambiguous'].length != 0){
		    			if(data['unknown'].length != 0) err_msg += "<br>";
		    			err_msg += "Ambiguous Names: " + data['ambiguous'];
		    		}
		    		$("#status_heading").html(err_msg);

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
		    		if('clash' in data){
		    			for(var k=0; k<data['clash'].length; k++)
		    				$("#extra_stuff").html("<br> Clashes with " + data['clash'][k][0] + 
		    					"<br>hosted from " + pretty_date(data['clash'][k][1]) 
		    					+ " to " + pretty_date(data['clash'][k][2]))
		    		}

		    		$('#statusModal').modal('show');
	    		}
	    		else{
		    		$("#status_heading").html("Success!!");
		    		$('#statusModal').modal('show');	    			
	    		
		    		$("#new_meeting_name").val('');
		    		$("#new_meeting_organizer").val('');
		    		$("#new_meeting_venue").val('');
		    		$("#new_meeting_participants").val('');
		    		$("#new_meeting_date").val('');
		    		$("#new_meeting_stime").val('');
		    		$("#new_meeting_etime").val('');
		    		$("#new_meeting_workflow").val('');
		    		$('#new_meeting_organizer').css('box-shadow', '0px 0px 0px green');
		    		$('#new_meeting_participants').css('box-shadow', '0px 0px 0px green');
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

    // Generate Report
    $("#gen_report").on('click', function(){
    	$.ajax({
	    	url: '/report/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			data: {
				'start': $("#report_sdate").val(),
				'end': 	 $("#report_edate").val(), 
			},
			success: function(data, textStatus, jqXHR){
	    		if('error' in data){
		    		$("#status_heading").html("Error: " + data['error']);
		    		$('#statusModal').modal('show');
	    		}
	    		else{	    		
	    			var new_table = "<table class='table table-striped table-hover'>";
	    			new_table += "<tr> \
	    				<th>Meeting Name</th>\
	    				<th>Start</th>\
	    				<th>End</th>\
	    				<th>Venue</th>\
	    				<th>Organizer</th>\
	    				<th>Meeting Type</th>\
	    				<th>Participants</th>\
    				</tr>"
	    			
	    			for(var i=0; i<data['meetings'].length; i++){
	    				new_table += "<tr>";
	    				for(var j=0; j<data['meetings'][i].length; j++){
	    					new_table += "<td>";
	    					if(j==1 || j==2)
	    						new_table += pretty_date(data['meetings'][i][j]);
	    					else
	    						new_table += data['meetings'][i][j];
	    					new_table += "</td>";
	    				}
	    				new_table += "</tr>";
	    			}
	    			new_table += "</table>"
	    			$("#report").append(new_table);
	    		}
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
	    		$("#status_heading").html("Failed to generate report!");
	    		$('#statusModal').modal('show');
			}    		    		
    	});    	
    });

    // Generate Backup
    $("#gen_backup").on('click', function(){
    	$.ajax({
	    	url: '/report/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			data: {
				'start': $("#report_sdate").val(),
				'end': 	 $("#report_edate").val(), 
			},
			success: function(data, textStatus, jqXHR){
	    		if('error' in data){
		    		$("#status_heading").html("Error: " + data['error']);
		    		$('#statusModal').modal('show');
	    		}
	    		else{	    		
					var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data['meetings']));

					var dlAnchorElem = document.getElementById('downloadAnchorElem');
					dlAnchorElem.setAttribute("href", dataStr);
					dlAnchorElem.setAttribute("download", "backup.json");
					dlAnchorElem.click();
	    		}
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
	    		$("#status_heading").html("Failed to generate report!");
	    		$('#statusModal').modal('show');
			}    		    		
    	});    	
    });

    $("#del_meeting").on("click", function(){
    	$.ajax({
	    	url: '/meeting/delete/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			data: {
				'meetingName': $("#view_meeting_name").html(),
			},
			success: function(data, textStatus, jqXHR){
	    		if('error' in data){
		    		$("#status_heading").html("Error: " + data['error']);
		    		$('#statusModal').modal('show');
	    		}
	    		else{	    			    			
	    			$('#viewMeetingModal').modal('hide');
		    		$("#status_heading").html("Deleted!");
		    		$('#statusModal').modal('show');
		    		$('#homelink').click();
	    		}
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
	    		$("#status_heading").html("Failed to delete meeting!");
	    		$('#statusModal').modal('show');
			}    		    		
    	});   
    });

    $("#reschedule_meeting").on("click", function(){
    	if($("#reschdule_form").css('display') == 'none')
	    	$("#reschdule_form").css("display", "inline");
    	else
	    	$("#reschdule_form").css("display", "none");
    });

    $("#update_reschedule").on("click", function(){
    	$.ajax({
	    	url: '/meeting/reschedule/',
	    	method: 'POST',
			headers: {
				Authorization: "token " + my_token,
			},
			data: {
				'name': $("#view_meeting_name").html(),
				'venue': $("#reschedule_meeting_venue").val(),
				'date': $("#reschedule_meeting_date").val(),
				'stime': $("#reschedule_meeting_stime").val(),
				'etime': $("#reschdule_meeting_etime").val()
			},
			success: function(data, textStatus, jqXHR){
	    		if('error' in data){
		    		$("#status_heading").html("Error: " + data['error']);
		    		if('clash' in data){
		    			for(var k=0; k<data['clash'].length; k++)
		    				$("#extra_stuff").html("<br> Clashes with " + data['clash'][k][0] + 
		    					"<br>hosted from " + pretty_date(data['clash'][k][1]) + " to " + pretty_date(data['clash'][k][2]))
		    		}
		    		$('#statusModal').modal('show');
	    		}
	    		else{	    			    			
	    			$('#viewMeetingModal').modal('hide');
	    			$("#reschdule_form").css("display", "none");
		    		$("#status_heading").html("Rescheduled!");
		    		$('#statusModal').modal('show');
		    		$('#homelink').click();
	    		}
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log("Error!");
				console.log(errorThrown);
	    		// $('#loadingModal').modal('hide');
	    		$("#status_heading").html("Failed to reschedule meeting!");
	    		$('#statusModal').modal('show');
			}    		    		
    	});   
    });	
});