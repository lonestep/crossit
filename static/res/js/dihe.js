$(function() {

  	$("#btn-login").click(function(e){
  		
  		e.preventDefault();
  		
  		});
  	$("#inputEmail").on('input',function(e){
  		
  		var newCt = $("#inputEmail").val();
  		if(newCt.indexOf('@') != -1)
  		alert(1);
  		
  		});
  		
});