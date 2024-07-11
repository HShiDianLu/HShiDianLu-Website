// article-config.js By HShiDianLu.
// Copyright © 2024 HShiDianLu. All Rights Reserved.
// Powered By Vditor.

// 初始化

var string = "";
for (var i = 0; i < stringArray.length; i++) {
    string += stringArray[i] + "\n";
}

var textEditor = new Vditor('editor', {
    "height": 500,
    "cache": {
        "enable": false
    },
    "mode": "sv",
    "preview": {
        "mode": "editor"
    },
    "value": string,
    "cdn": "/static/js/vditor",
    "toolbar": ["headings", "bold", "italic", "strike", "|", "line", "quote", "link", "|", "list", "ordered-list", "table", "|", "code", "inline-code", "|", "undo", "redo"],
})

// 发送

var sendRespond = false;

function send() {
    if (sendRespond) {
        return;
    }
    var err = false;
    $("#input-title-err").css("opacity", "0");
    $("#input-desc-err").css("opacity", "0");
    $("#editor-err").css("opacity", "0");
    if ($("#input-title").val() == "") {
        err = true;
        $("#input-title-err").css("opacity", "1");
    }
    if ($("#input-desc").val() == "") {
        err = true;
        $("#input-desc-err").css("opacity", "1");
    }
    if (textEditor.getValue() == "\n") {
        err = true;
        $("#editor-err").text("正文不能为空")
        $("#editor-err").css("opacity", "1");
    }
    if (err) {
        return;
    }
    sendRespond = true;
    $("#editor-btn").addClass("disabled-reverse");
    $.ajax({
        url: "/updateArticle",
        data: {
            'id': articleID,
            'type': type,
            'title': $("#input-title").val(),
            'desc': $("#input-desc").val(),
            'content': textEditor.getValue()
        },
        type: "POST",
        success: function (result) {
            if (result['result'] == "success") {
                if (type == "edit") {
                    $("#editor-btn").removeClass("disabled-reverse");
                    sendRespond = false;
                } else {
                    setTimeout(function () {
                        hrefTo("/article/" + articleID);
                    }, 3000)
                }
                Swal.fire({
                    toast: true,
                    showConfirmButton: false,
                    icon: 'success',
                    timer: 2000,
                    title: success + '成功',
                    text: successText,
                    position: 'bottom-start'
                })
            } else {
                $("#editor-btn").removeClass("disabled-reverse");
                sendRespond = false;
                $("#editor-error").text(success + "失败。错误码：" + result['code'])
                $("#editor-error").css("opacity", "1");
            }
        }
    })
}