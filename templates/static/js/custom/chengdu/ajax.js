# 性能监视器
function performance_monitoring() {
    $.ajax({
        url: '/networktools/custom/chengdu/performance_monitoring/',
        method: 'POST',
        success: function(data) {
            for (var i = 1; i <= data.length ; i++) {
              var tr = $('#performance_table tr').eq(i)
              tr.find("th").eq(3).html(data[i-1].max)
              tr.find("th").eq(4).html(data[i-1].avg)
              tr.find("th").eq(5).html(data[i-1].min)
              tr.find("th").eq(6).html(data[i-1].packets)
              tr.find("th").eq(7).html(data[i-1].Received)
              tr.find("th").eq(8).html(data[i-1].loss)
            };
            $('#test_msg').html('');
        },
        beforeSend: function(){
            $('#test_msg').html('正在处理，请稍等！');
        }
    })
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