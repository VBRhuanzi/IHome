function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // TODO: 查询用户的实名认证信息
   $.get('/api/1.0/users/auth', function (response) {
        if (response.errno == '0') {
            if (response.data.real_name && response.data.id_card) {
                // 获取实名认证信息成功：渲染input,禁用input,隐藏保存按钮
                $('#real-name').val(response.data.real_name);
                $('#id-card').val(response.data.id_card);

                $('#real-name').attr('disabled', true);
                $('#id-card').attr('disabled', true);
                $('.btn-success').hide();
            }
        } else if (response.errno == '4101') {
            location.href = 'login.html';
        } else {
            alert(response.errmsg);
        }
    });


    // TODO: 管理实名信息表单的提交行为
    $("#form-auth").submit(function (event) {
        event.preventDefault();

        var real_name = $('#real-name').val();
        var id_card = $('#id-card').val();

        if (!real_name) {
            alert('请输入真实姓名');
        }
        if (!id_card) {
            alert('请输入真实身份证号码');
        }

        var params = {
            'real_name':real_name,
            'id_card':id_card
        };


        $.ajax({
            url:"/api/1.0/users/auth",
            type:"post",
            data:JSON.stringify(params),
            contentType:'application/json',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (response) {
                if (response.errno=="0"){
                   showSuccessMsg();
                    // 因为实名认证只有一次，所以一旦认证成功，就要将inout设置为不可交互，并且要影藏保存按钮
                    $('#real-name').attr('disabled', true);
                    $('#id-card').attr('disabled', true);
                    $('.btn-success').hide();

                }else if (response.errno=="4101"){
                    //跳转页面
                    location.href = "login.html"
                }else{
                    alert(response.errmsg);
                }
            }

        });
    })

});

