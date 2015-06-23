function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function showMsg(isOK, info, closeontimeout)
{
    if (closeontimeout == undefined) {
        closeontimeout = true;
    }

    $("#info_dialog p").html('<span class="glyphicon" style="float:left; margin:0 7px 50px 0;"></span>');
    if (!isOK)
    {
        $("#info_dialog .modal-title").html('提示');
        $("#info_dialog p").prop("class", "alert alert-danger");
        $("#info_dialog p span").addClass("glyphicon-exclamation-sign");
        $("#info_dialog div.modal-header").attr("class", "modal-header label-danger");
    }
    else
    {
        $("#info_dialog .modal-title").html('信息');
        $("#info_dialog p").prop("class", "alert alert-success");
        $("#info_dialog p span").addClass("glyphicon-ok-sign");
        $("#info_dialog div.modal-header").attr("class", "modal-header label-success");
    }
    $("#info_dialog p span").after(info);
    $('#info_dialog').modal('show');
    if (closeontimeout)
    {
        setTimeout(function () {
            $('#info_dialog').modal('hide');
        }, 1500);
    }
}

Array.prototype.ArrContain=function(value)
{
  for(var i=0;i<this.length;i++)
  {
     if(this[i]==value)
      return true;
  }
  return false;
}

function checkPasswd(val){
  return (val.length >= 6)
}

$(function() {
  		
});