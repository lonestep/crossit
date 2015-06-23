require.config({
	timeout:15,
    shim : {
        'bs332/js/bootstrap.min': ['css!bs332/css/bootstrap.min.css','css!bs332/css/bootstrap-theme.min.css'],
        'fc227/fullcalendar.min':['css!fc227/fullcalendar.min.css','css!fc227/fullcalendar.print.css'],
        'js/dihe':['css!css/dihe.css'],
    }
});
requirejs(['jquery-1.11.2.min','bs332/js/bootstrap.min','css','fc227/lib/moment.min','fc227/fullcalendar.min','hc403/js/highcharts','css','js/dihe'],
function(){
    $('#preload').remove();
    $('div.container,nav.navbar').fadeIn(500);
	});