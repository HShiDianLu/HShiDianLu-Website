// article-config.js By HShiDianLu.
// Copyright © 2024-2025 HShiDianLu. All Rights Reserved.
// Powered By Vditor.

// 初始化

let string = "";
for (let i = 0; i < stringArray.length; i++) {
    string += stringArray[i] + "\n";
}

let textEditor = new Vditor('editor', {
    "height": 600,
    "cache": {
        "enable": false
    },
    "mode": "ir",
    "preview": {
        // "mode": "editor",
        "math": {
            "engine": "MathJax"
        }
    },
    "value": string,
    "cdn": "/static/vditor",
    "toolbar": ["headings", "bold", "italic", "strike", "|", "line", "quote", "link", "|", "list", "ordered-list", "table", "|", "code", "inline-code", "|", "undo", "redo"],
})

// 发送

let sendRespond = false;

function send() {
    if (sendRespond) {
        return;
    }
    let err = false;
    $("#input-title-err").css("opacity", "0");
    $("#input-desc-err").css("opacity", "0");
    $("#editor-err").css("opacity", "0");
    if (!$("#input-title").val()) {
        err = true;
        $("#input-title-err").css("opacity", "1");
    }
    if (!$("#input-desc").val()) {
        err = true;
        $("#input-desc-err").css("opacity", "1");
    }
    // if ($("#input-banner").val() == "") {
    //     err = true;
    //     $("#input-banner-err").css("opacity", "1");
    // }
    if (textEditor.getValue() === "\n") {
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
            'banner': $("#input-banner").val(),
            'content': textEditor.getValue()
        },
        type: "POST",
        success: function (result) {
            if (result['result'] === "success") {
                if (type === "edit") {
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
                $("#editor-error").text(errorCodeMapping(result['code']))
                $("#editor-error").css("opacity", "1");
            }
        }
    })
}