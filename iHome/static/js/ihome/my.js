function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// TODO: 点击推出按钮时执行的函数
function logout() {
    alert("lala");
    $.ajax({
        url:"/api/1.0/session",
        type:'delete',
        headers:{'X-CSRFToken':getCookie('csrf_token')},
         success:function (response) {
            if (response.errno == '0'){
                location.href = "index.html";
            } else if (response.errno == "4101"){
                 location.href = "login.html";
            }else{
                alert(response.errmsg);
            }
         }
    })
}

$(document).ready(function(){

    // TODO: 在页面加载完毕之后去加载个人信息
$.get('/api/1.0/users',function (response) {
        if  (response.errno == '0'){
            $('#user-name').html(response.data.name);
            $('#user-mobile').html(response.data.mobile);
            $("#user-avatar").attr("src",response.data.avatar_url);
        } else if (response.errno == '4101'){
            location.href = 'login.html';
        }else　{
            alert(response.errno)
        }
    });

});
