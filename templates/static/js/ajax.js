function tcp_easy_check(){
    var ip;
    var port;
    ip = $('#ip').val();
    port = $('#port').val();
    if (ip==null || ip == '') {
        alert("Please input ip!");
        return;
    }
    if (port==null || port == '') {
        alert("Please input ip!");
        return;
    }
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



function udp_easy_check(){
    var ip;
    var port;
    ip = $('#ip').val();
    port = $('#port').val();
    if (ip==null || ip == '') {
        alert("Please input ip!");
        return;
    }
    if (port==null || port == '') {
        alert("Please input ip!");
        return;
    }
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


function ping_tracert_check(){
    var ip;
    ip = $('#ip').val();
    if (ip==null || ip == '') {
        alert("Please input ip!");
        return;
    }
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

function tcp_group_test() {
    var file = $("#datafile").val();
    var form_data = new FormData();
    var file_info = $('#datafile')[0].files[0];
    form_data.append('file',file_info);

    if (file == null || file == '') {
        alert("please input file!");
        return;
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



function udp_group_test() {
    var file = $("#datafile").val();
    var form_data = new FormData();
    var file_info = $('#datafile')[0].files[0];
    form_data.append('file',file_info);

    if (file == null || file == '') {
        alert("please input file!");
        return;
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
                $("#result").html(result.result)
            },

        });
    }
}

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


/*version:0.2*/
/*description:添加mac地址,上传mac文件等相应前端操作*/
function selectOnchang(obj) {
    var value = obj.options[obj.selectedIndex].value;
    if (value == 'single') {
        $("#filepreview").remove();
        $("#mac_file").remove();
        if ($("#mac").length <= 0) {
            $("#mac_val").append("<input id=\"mac\" name=\"mac\" placeholder=\"Mac Address：\">")
        }

    } else if (value == 'multiple') {
        if ($("#filepreview").val() != null) {
            return;
        } else {
            $("#mac").remove();
            $("#mac_file_val").append("<form><input id=\"mac_file\" type=\"file\" onchange=\"jsReadFile(this.files)\"></form>")
            $("#filepreview_val").append(
                "<textarea style=\"width:500px;height:200px;\" id=\"filepreview\" readonly=\"readonly\"></textarea>"
            )
        }
    }
}

function sub_mac() {
    if ($("#filepreview").val() == null) {
        var mac = $("#mac").val();
        if (mac == null || mac == '') {
            alert("Please enter mac address!");
            return;
        } else {
            $.ajax({
                url: '/networktools/custom/chengdu/add_mac/',
                method: 'POST',
                data: {mac:mac},
                success: function(data) {
                    if (data.failed != '' || data.failed != '')
                        $('#result').html(data.failed);
                    else {
                        $('#result').html(data.success);
                    }
                },
                beforeSend: function(){
                    $('#filepreview').val('正在处理，请稍等！');
                }
            });
        }

    } else {
        var file = $("#mac_file").val();
        var form_data = new FormData();
        var file_info = $('#mac_file')[0].files[0];
        form_data.append('file',file_info);

        if (file == null || file == '') {
            alert("please input file!");
            return;
        } else {
            $.ajax({
                type: 'POST',
                url: "/networktools/custom/chengdu/add_mac_file/",
                dataType: 'json',
                data: form_data,
                processData: false,  // tell jquery not to process the data
                contentType: false,
                beforeSend:function () {
                    $.mask_fullscreen();
                },
                success: function (result) {
                    if(true) {
                        $.mask_close_all();
                    }
                    $('#result').html(result.success);
                    $('#failed').append(result.failed);
                },
                complete: function () {

                }

            });
        }
    }
}
