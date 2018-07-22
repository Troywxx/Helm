var prd = new Object();
var radar = new Object();
var awos = new Object();
var sat = new Object();
var radar_166 = new Object();
var awos_166 = new Object();

var alert_api = false;
var alert_manual = true;

prd.radar = radar;
prd.awos = awos;
prd.satellite = sat;
prd.radar_166 = radar_166;
prd.awos_166 = awos_166;

radar.url = "/api/v1.0/watchlist/radar/get/";
awos.url = "/api/v1.0/watchlist/awos/get/";
sat.url = "/api/v1.0/watchlist/satellite/get/";
radar_166.url = "/api/v1.0/watchlist/radar_166/get/";
awos_166.url = "/api/v1.0/watchlist/awos_166/get/";

function alert_manual_set_true(){
	alert_manual = true;
}

function alert_manual_set_false(){
	alert_manual = false;
	setTimeout('alert_manual_set_true()', 600000);
}

function alert_sound(){
	if(alert_api && alert_manual){
		$('#watch').get(0).play();
	}
	else{
		$('#watch').get(0).pause();
	}
}

function time_show(){
	var t = new Date();
	$("#time_utc").html(t.toUTCString().substr(17,8));
	$("#time_bjt").html(t.toTimeString().substr(0,8));
	$("#date").html(t.toDateString().substr(0,10));
	}

function prd_show(){

	if(prd.radar.alert||prd.awos.alert||prd.radar_166.alert||prd.awos_166.alert){
		$("#alert").html("异常");
		$("#alert").addClass("xalert");
		alert_api = true;
	}
	else{
		$("#alert").html("正常");
		$("#alert").removeClass("xalert");
		alert_api = false;
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

	if(prd.radar_166.alert){
		$("#radar_166_filetime").text(prd.radar_166.filetime);
		$("#radar_filetime").addClass("xalert");
	}
	else{
		$("#radar_166_filetime").text(prd.radar_166.filetime);
		$("#radar_filetime").removeClass("xalert");
	}

	if(prd.awos_166.alert){
		$("#awos_166_filetime").text(prd.awos_166.filetime);
		$("#awos_filetime").addClass("xalert");
	}
	else{
		$("#awos_166_filetime").text(prd.awos_166.filetime);
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
		dataType: "json",
		crossDomain:true
	}).done(function(data){
		$.each(data,function(i, item){
				if(i == "Alert"){
					// console.log(typeof(item));
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
	setInterval(prd_get, 1000);
	prd_show();
	setInterval(prd_show, 1000);
	alert_sound();
	setInterval(alert_sound, 1000);
});
