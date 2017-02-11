$(document).ready(function() {

    // page is now ready, initialize the calendar...

    $('#calendar').fullCalendar({
        // put your options and callbacks here
	    contentHeight: window.innerHeight*0.61,
	    handleWindowResize: true
    })
});
