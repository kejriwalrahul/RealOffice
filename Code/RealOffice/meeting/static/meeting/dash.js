$(document).ready(function(){
	var my_token = window.localStorage.getItem("token");

    // page is now ready, initialize the calendar...
    $('#calendar').fullCalendar({
        // put your options and callbacks here
	    contentHeight: window.innerHeight*0.61,
	    handleWindowResize: true
    });

    // Log Out
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
			}
    	});

    });
});