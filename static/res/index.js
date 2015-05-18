require.config({
    shim : {
        'bs332/js/bootstrap.min': ['css!bs332/css/bootstrap.min.css','css!bs332/css/bootstrap-theme.min.css'],
        'js/dihe':['css!css/dihe.css'],
    }
});
requirejs(['jquery-1.11.2.min','bs332/js/bootstrap.min','css','js/dihe'],
function(){

	});