var prd = new Object();
var radar = new Object();
var awos = new Object();
var sat = new Object();
prd.radar = radar;
prd.awos = awos;
prd.satellite = sat;
radar.url = "http://127.0.0.1:5000/api/v1.0/watchlist/radar/get/";
awos.url = "http://127.0.0.1:5000/api/v1.0/watchlist/awos/get/";
sat.url = "http://127.0.0.1:5000/api/v1.0/watchlist/satellite/get/";


function time_show(){
	var t = new Date();
	$("#time_utc").html(t.toUTCString().substr(17,8));
	$("#time_bjt").html(t.toTimeString().substr(0,8));
	$("#date").html(t.toDateString().substr(0,10));
	}

function prd_show(){
	if(prd.radar.alert||prd.awos.alert||prd.satellite.alert){
		$("#alert").html("异常");
		$("#alert").addClass("xalert");
	}
	else{
		$("#alert").html("正常");
		$("#alert").removeClass("xalert");
	}

	if(prd.radar.alert){
		$("#radar_filename").text(prd.radar.filename);
		$("#radar_filename").addClass("xalert");
		$("#radar_filetime").text(prd.radar.filetime);
		$("#radar_filetime").addClass("xalert");
	}
	else{
		$("#radar_filename").text(prd.radar.filename);
		$("#radar_filename").removeClass("xalert");
		$("#radar_filetime").text(prd.radar.filetime);
		$("#radar_filetime").removeClass("xalert");
	}

	if(prd.awos.alert){
		$("#awos_filename").text(prd.awos.filename);
		$("#awos_filename").addClass("xalert");
		$("#awos_filetime").text(prd.awos.filetime);
		$("#awos_filetime").addClass("xalert");
	}
	else{
		$("#awos_filename").text(prd.awos.filename);
		$("#awos_filename").removeClass("xalert");
		$("#awos_filetime").text(prd.awos.filetime);
		$("#awos_filetime").removeClass("xalert");
	}

	if(prd.satellite.alert){
		$("#sat_filename").text(prd.satellite.filename);
		$("#sat_filename").addClass("xalert");
		$("#sat_filetime").text(prd.satellite.filetime);
		$("#sat_filetime").addClass("xalert");
	}
	else{
		$("#sat_filename").text(prd.satellite.filename);
		$("#sat_filename").removeClass("xalert");
		$("#sat_filetime").text(prd.satellite.filetime);
		$("#sat_filetime").removeClass("xalert");
	}
}


function prd_get(){
	for (var j in prd){
	$.ajax({
		async: true,
		type: "GET",
		url: prd[j].url,
		dataType: "json"
	}).done(function(data){
		$.each(data,function(i, item){
				if(i == "Alert"){
					prd[data.Prd_Type].alert = item;
				}
				else if(i == "Filename"){
					prd[data.Prd_Type].filename = item;
				}
				else if(i == "Filetime"){
					prd[data.Prd_Type].filetime = item;
				}
			});	
	});
}
}

$(document).ready(function() {
	time_show();
	setInterval(time_show, 1000);
	prd_get();
	setInterval(prd_get, 10000);
	prd_show();
	setInterval(prd_show, 5000);
});
