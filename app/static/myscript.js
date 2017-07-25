$(document).ready(function() {
	function time_show(){
	var t = new Date();
	$("#time_utc").html(t.toUTCString().substr(17,8));
	$("#time_bjt").html(t.toTimeString().substr(0,8));
	$("#date").html(t.toDateString().substr(0,10));
	}
	time_show();
	setInterval(time_show, 1000);
});


function postlist_delete(id){
    console.log(typeof(id));
}


$(document).ready(function(){
	function prd_show(){
	var prd = new Array();
	var radar = new Object();
	var awos = new Object();
	var sat = new Object();
	prd.push(radar, awos, sat)
	radar.url = "http://127.0.0.1:5000/api/v1.0/watchlist/radar/get/";
	awos.url = "http://127.0.0.1:5000/api/v1.0/watchlist/awos/get/";
	sat.url = "http://127.0.0.1:5000/api/v1.0/watchlist/satellite/get/";

	for (var j=0; j<3; j++){
	prd_list = $.ajax({
		async: false,
		type: "GET",
		url: prd[j].url,
		dataType: "json"
	});
	$.each(prd_list.responseJSON, function(i, item){
				if(i == "Alert"){
					prd[j].alert = item;
				}
				else if(i == "Filename"){
					prd[j].filename = item;
				}
				else if(i == "Filetime"){
					prd[j].filetime = item;
				}
			});
	}

	if(prd[0].alert||prd[1].alert||prd[2].alert){
		$("#alert").html("异常");
		$("#alert").addClass("xalert");
	}
	else{
		$("#alert").html("正常");
		$("#alert").removeClass("xalert");
	}

	if(prd[0].alert){
		$("#radar_filename").text(prd[0].filename);
		$("#radar_filename").addClass("xalert");
		$("#radar_filetime").text(prd[0].filetime);
		$("#radar_filetime").addClass("xalert");
	}
	else{
		$("#radar_filename").text(prd[0].filename);
		$("#radar_filename").removeClass("xalert");
		$("#radar_filetime").text(prd[0].filetime);
		$("#radar_filetime").removeClass("xalert");
	}

	if(prd[1].alert){
		$("#awos_filename").text(prd[1].filename);
		$("#awos_filename").addClass("xalert");
		$("#awos_filetime").text(prd[1].filetime);
		$("#awos_filetime").addClass("xalert");
	}
	else{
		$("#awos_filename").text(prd[1].filename);
		$("#awos_filename").removeClass("xalert");
		$("#awos_filetime").text(prd[1].filetime);
		$("#awos_filetime").removeClass("xalert");
	}

	if(prd[2].alert){
		$("#sat_filename").text(prd[2].filename);
		$("#sat_filename").addClass("xalert");
		$("#sat_filetime").text(prd[2].filetime);
		$("#sat_filetime").addClass("xalert");
	}
	else{
		$("#sat_filename").text(prd[2].filename);
		$("#sat_filename").removeClass("xalert");
		$("#sat_filetime").text(prd[2].filetime);
		$("#sat_filetime").removeClass("xalert");
	}

	}
	prd_show();
	setInterval(prd_show, 10000);
});