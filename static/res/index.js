require.config({
    shim : {
        'bs332/js/bootstrap-typeahead.min':['jquery-1.11.2.min','bs332/js/bootstrap.min'],
        'bs332/js/bootstrap.min': ['css!bs332/css/bootstrap.min.css','css!bs332/css/bootstrap-theme.min.css'],
        'js/dihe':['css!css/dihe.css'],
    }
});
requirejs(['jquery-1.11.2.min','bs332/js/bootstrap.min','bs332/js/bootstrap-typeahead.min','css','js/dihe'],
function(){
    $('#preload').remove();
    $('div.container').fadeIn(500);
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('input.email').typeahead({
        source: ename_list,
        onSelect: function(item) 
        {
            if(item.text === 'Result not Found'){
                return;
            }
            $.post('/chkusr/',{'name':item.value},function(data){
                if(data.exist){
                    $('._reg').hide();
                    $("#btn-login").html('登录').removeClass('register');
                    $("#inputPassword").removeClass("top").addClass("psw");
                    $("#inputPassword").focus();
                }
                else{
                    $("#btn-login").html('注册').addClass('register');
                    $('._reg').fadeIn(500);
                    $("#inputPassword").removeClass("psw").addClass("top");
                    $('#inputVcode').focus();
                }

            });
            
        }
    }).val('');

    $('input').bind('focus',function(e){
        $('.bubble_l').hide();
        $(this).siblings('.bubble_l').fadeIn(500);
    });

    $('input[type="password"]').blur(function(e){
        psw = $(this).val();
        if(!checkPasswd(psw)){
            $(this).addClass('has-error').focus();
        }
        else{
            $(this).removeClass('has-error');
        }
    });

    $('#inputEmail').blur(function(e){
        if(ename_list.ArrContain($('#inputEmail').val())){
            $(this).removeClass('has-error');
        }
        else{
            $('#inputEmail').addClass('has-error').focus();
            return;
        }
    });

    $('#btn-login').click(function(e){
        
        var data = $('form.form-signin').serialize();
        if(!ename_list.ArrContain($('#inputEmail').val())){
            $('#inputEmail').addClass('has-error').focus();
            e.preventDefault();
            return;
        }
        if($('input[type="password"].has-error').length > 0)
        {
         e.preventDefault();
         return;
        }
        if($(this).find('span.glyphicon').length === 0){
            $(this).prepend('<span class="glyphicon glyphicon-refresh ico-spin" aria-hidden="true"></span>');
        }
        //注册
        if($(this).hasClass('register')){
           $('form.form-signin').prop('action', '/reg/');
           /*$.post('/reg/',data,function(json)
           {
             showMsg(json.success, json.msg);
           });*/
        }
        else
        {
            $('form.form-signin').prop('action', '/login/');
           /*$.post('/login/',data,function(json)
           {
             showMsg(json.success, json.msg);
           });*/
        }
    });

});