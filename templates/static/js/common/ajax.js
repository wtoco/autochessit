# tcp单例测试
function tcp_easy_check(){
    var ip;
    var port;
    ip = $('#ip').val();
    port = $('#port').val();
    $.ajax({
        url: '/networktools/common/tcp_easy_test/',
        method: 'POST',
        data: {ip:ip,port:port},
        success: function(data) {
               $('#test_msg').val(data);
        },
        beforeSend: function(){
            $('#test_msg').val('正在处理，请稍等！');
        }
    })
}


# udp单例测试
function udp_easy_check(){
    var ip;
    var port;
    ip = $('#ip').val();
    port = $('#port').val();
    $.ajax({
        url: '/networktools/common/udp_easy_test/',
        method: 'POST',
        data: {ip:ip,port:port},
        success: function(data) {
               $('#test_msg').val(data);
        },
        beforeSend: function(){
            $('#test_msg').val('正在处理，请稍等！');
        }
    })
}

# ping&tracert ip地址
function ping_tracert_check(){
    var ip;
    ip = $('#ip').val();
    $.ajax({
        url: '/networktools/common/ping_tracrt_to_file/',
        method: 'POST',
        data: {ip:ip},
        success: function(data) {
            $('#test_msg').val(data);
        },
        beforeSend: function(){
            $('#test_msg').val('正在处理，请稍等！');
        }
    })
}

# 批量tcp测试
function tcp_group_test() {
    var file = $("#datafile").val();
    var form_data = new FormData();
    var file_info = $('#datafile')[0].files[0];
    form_data.append('file',file_info);

    if (file == null || file == '') {
        alert("please input file!");
    } else {
        $.ajax({
            type: 'POST',
            url: "/networktools/common/tcp_group_test/",
            dataType: 'json',
            data: form_data,
            processData: false,  // tell jquery not to process the data
            contentType: false,
            success: function (result) {
                var test = result.filepreview;
                $("#filepreview").html(result.filepreview)
                $("#result").html(result.result)
            },

        });
    }
}


# 批量udp测试
function udp_group_test() {
    var file = $("#datafile").val();
    var form_data = new FormData();
    var file_info = $('#datafile')[0].files[0];
    form_data.append('file',file_info);

    if (file == null || file == '') {
        alert("please input file!");
    } else {
        $.ajax({
            type: 'POST',
            url: "/networktools/common/udp_group_test/",
            dataType: 'json',
            data: form_data,
            processData: false,  // tell jquery not to process the data
            contentType: false,
            success: function (result) {
                var test = result.filepreview;
                $("#filepreview").html(result.filepreview)
                $("#result").html(result.result)
            },

        });
    }
}

# 测试所有接口
function test_all_ports(){
    var ip;
    ip = $('#ip').val();
    $.ajax({
        url: '/networktools/common/test_all_ports/',
        method: 'POST',
        data: {ip:ip},
        success: function(data) {
            $('#test_msg').val(data);
        },
        beforeSend: function(){
            $('#test_msg').val('正在处理，请稍等！');
        }
    })
}

# js在线预览图片
function jsReadFile(files) {
	var file = files[0];
	var reader = new FileReader();

	reader.onload = (
		function(file){
			return function(e) {
				$("#filepreview").html(this.result);
			};
		}
	)(file);
	reader.readAsText(file);
}