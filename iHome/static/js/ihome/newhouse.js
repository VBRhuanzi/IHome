function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get('/api/1.0/areas', function (response) {
        if (response.errno == '0') {
            // 渲染城区信息到界面上
            /*
            $.each(response.data, function (i, area) {
                $('#area-id').append('<option value="'+area.aid+'">'+area.aname+'</option>');
            });
            */

            // 使用art-template模板引擎中的js生成要渲染的html内容
            var html = template('areas-tmpl', {'areas':response.data});
            // 将生成的html赋值给某个标签
            $('#area-id').html(html);
        } else {
            alert(response.errmsg);
        }
    });

    // TODO: 处理房屋基本信息提交的表单数据
    $('#form-house-info').submit(function (event) {
        event.preventDefault();

        // var title = $('#house-title').val();
        var params = {};
        // params['title'] = title;

        // 收集$(this)表单中的带有name的input标签数据，生成字典对象，封装到数组中
        // obj == {name:'title',value:'1'}
        // obj == {name:'price',value:'1'}
        // obj == {name:'facility',value:'8'}
        // obj == {name:'facility',value:'10'}
        $(this).serializeArray().map(function (obj) {
            // console.log(obj);
            params[obj.name] = obj.value;
        });

        facilities = [];
        // 收集界面上所有的"被选中"的checkbox,而且name必须是facility
        $(':checkbox:checked[name=facility]').each(function (i, elem) {
            // console.log(i, elem);
            facilities[i] = elem.value;
        });
        params['facility'] = facilities;
        // console.log(params);

        $.ajax({
            url:'/api/1.0/houses',
            type:'post',
            data:JSON.stringify(params),
            contentType:'application/json',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (response) {
                if (response.errno == '0') {
                    // 发布新的房源信息成功后的操作:隐藏基本信息的表单，展示上传图片的表单
                    $('#form-house-info').hide();
                    $('#form-house-image').show();
                    // 将发布成功的house_id渲染到界面上
                    $('#house-id').val(response.data.house_id);
                } else if (response.errno == '4101') {
                    location.href = 'login.html';
                } else {
                    alert(response.errmsg);
                }
            }
        });
    });


    // TODO: 处理图片表单的数据
    $('#form-house-image').submit(function (event) {
        event.preventDefault();

        // 模拟表单的自己的提交行为，因为这个表单里面需要发送文字和图片，非json数据
        $(this).ajaxSubmit({
            url:'/api/1.0/houses/image',
            type:'post',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            contentType:'application/json',
            success:function (response) {
                if (response.errno == '0') {
                    // 将上传的房屋图片渲染出来
                    $('.house-image-cons').append('<img src="'+response.data.house_image_url+'">');
                } else if (response.errno == '4101') {
                    location.href = 'login.html';
                } else {
                    alert(response.errmsg);
                }
            }
        });
    });
});