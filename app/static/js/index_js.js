let $ = layui.jquery;
$(document).ready(function () {
    createTag()
});

$("#btn_refresh").click(function () {
    createTag()
});

$('#index').click(function () {
    $.ajax({
        method: 'GET',
        url: '/pic',
        success: function (data) {
            data = JSON.parse(data);
            layer.msg(data.msg)
        }
    })
});

function createTag() {
    let content = $("#show_cont");
    getContent().then(cont => {
        let goodDiv = `<div style=" width: 33%;display: inline-block">
        <button id="good" class="layui-btn" style="width: 100%"><i class="layui-icon">&#xe68c;</i>点赞</button>
    </div>`;
        let talkDiv = `<div style=" width: 33%;display: inline-block">
        <button id="btn_talk" class="layui-btn" style="width: 100%"><i class="layui-icon">&#xe611;</i>评论</button>
    </div>`;
        let collDiv = `<div style="width: 34%; display: inline-block">
        <button id="btn_coll" class="layui-btn" style="width: 100%" ><i class="layui-icon">&#xe627;</i>收藏</button>
    </div>`;
        let actionDiv = `<div style="position: absolute; bottom: 0px;width: 100%">${goodDiv}${talkDiv}${collDiv}</div>`;
        let div = `<div class="layui-anim layui-anim-up layui-bg-gray" style="height: 400px;" id="show_cont">${cont}${actionDiv}</div>`;
        content.html(div);
    });

}

let cont = "";

function getContent() {
    return new Promise(function (resolve, reject) {
        $.ajax({
            method: "GET",
            url: "/get_cont",
            // async: false,
            success: function (data) {
                let resp = JSON.parse(data);
                if (resp.ret === 0) {
                    cont = resp.data;
                    resolve(cont)
                } else {
                    layer.msg("error");
                    reject("error")
                }
            },
            error: function () {
                layer.msg("error")
            }
        });
    });

}


$('#publish').click(function () {
    var content = $('#input_textarea').val();
    $.ajax({
        url: '/publish',
        dataType: 'JSON',
        data: content,
        method: 'POST',
        success:function (resp) {
            data = JSON.parse(resp);
            layer.msg(resp.msg, {time: 1000})
        }
    })
});