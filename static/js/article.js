// article.js By HShiDianLu.
// Copyright © 2024-2025 HShiDianLu. All Rights Reserved.

// 滚动定位
function scrollToComment() {
    if (!loginState) {
        openLogin();
    } else {
        scroll('#comment-title');
        $("#comment-text").focus();
    }
}

// 点赞

const LIKE_OUTLINE = '<path d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2.144 2.144 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a9.84 9.84 0 0 0-.443.05 9.365 9.365 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111L8.864.046zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a8.908 8.908 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.224 2.224 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.866.866 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"/>';
const LIKE_FULL = '<path d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/>';

function like() {
    if (!loginState) {
        openLogin();
    } else {
        $.ajax({
            url: "/articleOperate",
            type: "POST",
            data: {
                'type': 'like',
                'id': articleID
            },
            success: function (result) {
                if (result['result'] === "success") {
                    if (likeState) {
                        $("#like-label").text(parseInt($("#like-label").text()) - 1);
                        $("#like-svg").html(LIKE_OUTLINE);
                        likeState = false;
                    } else {
                        $("#like-label").text(parseInt($("#like-label").text()) + 1);
                        $("#like-svg").html(LIKE_FULL);
                        likeState = true;
                    }
                } else {
                    Swal.fire({
                        toast: true,
                        showConfirmButton: false,
                        icon: 'error',
                        timer: 2000,
                        title: '点赞失败',
                        text: errorCodeMapping(result['code']),
                        position: 'bottom-start'
                    })
                }
            }
        });
    }
}

// 评论

function expand(id) {
    setInterval(function () {
        $("#" + id).css("height", (102 + $("#" + id + " p").height()) + "px");
    }, 300)
}

let sendState = false;

function send() {
    if (sendBtnState1) {
        cantBack = true;
        $("#comment-text").focus();
    }
    if (sendBtnState1 || sendBtnState2) {
        return;
    }
    if (sendState) {
        return;
    }
    sendState = true;
    $("#comment-err").css("opacity", "0");
    $.ajax({
        url: "/articleOperate",
        type: "POST",
        data: {
            'type': 'comment',
            'id': articleID,
            'comment': $("#comment-text").val()
        },
        success: function (result) {
            sendState = false;
            if (result['result'] === "success") {
                let randomID = randomNum(1000000, 9999999);
                $("#comments").prepend('<div class="comment self-comment" id="c-' + randomID + '">\n' +
                    '                <h3>' + username + '</h3>\n' +
                    '                <p>' + $("#comment-text").val() + '</p>\n' +
                    '                <br/>\n' +
                    '                <small id="d-' + randomID + '" class="comment-date">' + moment(result['data']).fromNow() + '</small>\n' +
                    '                <br/>\n' +
                    '                <br/>\n' +
                    '                <hr class="split-line-long"/>\n' +
                    '            </div>');
                tippy("#d-" + randomID, {
                    content: result['data'],
                    placement: "bottom",
                    animation: 'shift-away'
                });
                $("#send").css("opacity", "0");
                $("#comment-area").removeClass("comment-area-focus");
                $("#comment-text").css("height", "17px");
                $("#comment-text").val("");
                $("#comment-title small").text(parseInt($("#comment-title small").text()) + 1);
                $("#comment-label").text(parseInt($("#comment-label").text()) + 1);
                if (!haveComment) {
                    $("#no-comment").css("opacity", "0");
                }
                expand("c-" + randomID);
            } else {
                $("#comment-err").text(errorCodeMapping(result['code']));
                $("#comment-err").css("opacity", "1");
            }
        }
    });
}

// 评论动画

$("#comment-text").focusin(function () {
    $("#comment-area").addClass("comment-area-focus");
    $("#comment-text").css("height", "100px");
    $("#send").css("opacity", "1");
})

let cantBack = false;

$("#comment-text").focusout(function () {
    setTimeout(function () {
        if (cantBack) {
            cantBack = false;
            return;
        }
        if (!$("#comment-text").val()) {
            $("#send").css("opacity", "0");
            $("#comment-area").removeClass("comment-area-focus");
            $("#comment-text").css("height", "17px");
        }
    }, 100)
})

// 评论监听

let sendBtnState1 = false;
let sendBtnState2 = false;

if (loginState) {
    setInterval(function () {
        if (!sendState) {
            $("#comment-count").text($("#comment-text").val().length + "/200");
            if ($("#comment-text").val().length > 200) {
                $("#comment-err").css("opacity", "0");
                $("#send").addClass("disabled-reverse");
                $("#comment-op span").css("color", "red");
                sendBtnState2 = true;
            } else if (!sendBtnState1) {
                $("#send").removeClass("disabled-reverse");
                $("#comment-op span").css("color", "gray");
                sendBtnState2 = false;
            }
            if (!$("#comment-text").val()) {
                $("#comment-err").css("opacity", "0");
                $("#send").addClass("disabled-reverse")
                sendBtnState1 = true;
            } else if (!sendBtnState2) {
                $("#send").removeClass("disabled-reverse")
                sendBtnState1 = false;
            }
        } else {
            $("#send").addClass("disabled-reverse")
        }
    }, 0)
}

// 评论加载

let loadingState = true;
let commentStart = 11
let loaded = false;

if (haveComment) {
    let loadDetect = setInterval(function () {
        if ($("#load").css("opacity") == "1" && !loaded) {
            loadingState = false;
            loaded = true;
            clearInterval(loadDetect);
        }
    }, 0)
}

function loadComment() {
    $.ajax({
        url: "/commentFetch",
        type: "POST",
        data: {
            'id': articleID,
            'start': commentStart
        },
        success: function (result) {
            if (result['result'] === "success") {
                if (result['data'].length === 0) {
                    $("#load").text("没有更多了");
                    return;
                }
                for (let i = 0; i < result['data'].length; i++) {
                    let randomID = 'n-' + randomNum(1000000, 9999999);
                    $("#comments").append('<div class="comment self-comment" id="' + randomID + '">\n' +
                        '                <h3>' + result['data'][i][0] + '</h3>\n' +
                        '                <p>' + result['data'][i][4] + '</p>\n' +
                        '                <br/>\n' +
                        '                <small id="d-' + result['data'][i][1] + '" class="comment-date">' + moment(result['data'][i][3]).fromNow() + '</small>\n' +
                        '                <br/>\n' +
                        '                <br/>\n' +
                        '                <hr class="split-line-long"/>\n' +
                        '            </div>');
                    tippy("#d-" + result['data'][i][1], {
                        content: result['data'][i][3],
                        placement: "bottom",
                        animation: 'shift-away'
                    });
                    expand(randomID);
                }
                commentStart += 5;
            } else {
                Swal.fire({
                    toast: true,
                    showConfirmButton: false,
                    icon: 'error',
                    timer: 2000,
                    title: '评论加载失败',
                    text: errorCodeMapping(result['code']),
                    position: 'bottom-start'
                })
            }
            setTimeout(function () {
                $("#load").text("下拉加载更多");
                loadingState = false;
            }, 300)
        }
    });
}

$(window).scroll(function () {
    if ($(window).scrollTop() + $(window).outerHeight() >= $(document).height() - 10 && !loadingState) {
        loadingState = true;
        loadComment();
        $("#load").text("正在加载···")
    }
});

// 分享链接
function share() {
    if (!loginState) {
        openLogin();
        return;
    }
    $.ajax({
        url: "/articleOperate",
        data: {
            'type': 'share',
            'id': articleID
        },
        type: "POST",
        success: function (result) {
            if (result['result'] === "success" || result['code'] === 1017) {
                if (result['result'] === "success") {
                    $("#share-label").text(parseInt($("#share-label").text()) + 1);
                }
                copy(window.location.href);
                Swal.fire({
                    toast: true,
                    showConfirmButton: false,
                    icon: 'success',
                    timer: 2000,
                    title: '分享成功',
                    text: "链接已复制到您的剪贴板。",
                    position: 'bottom-start'
                })
            } else {
                Swal.fire({
                    toast: true,
                    showConfirmButton: false,
                    icon: 'error',
                    timer: 2000,
                    title: '分享失败',
                    text: errorCodeMapping(result['code']),
                    position: 'bottom-start'
                })
            }
        }
    })
}

// Markdown转换

MathJax = {
    tex: {inlineMath: [['$', '$'], ['\\(', '\\)']]}
};

let renderer = new marked.Renderer();

renderer.code = function (code, type) {
    if (type === "mermaid") {
        return '<div class="mermaid">' + code + '</div>';
    }
    let hlCode;
    if (type != undefined || type == "") {
        hlCode = hljs.highlightAuto(code, [type]);
    } else {
        hlCode = hljs.highlightAuto(code);
    }
    return '<pre><code class="hljs language-' + hlCode.language + '">' + hlCode.value + '</code></pre>';
}

marked.use({renderer: renderer});

markdownText = marked.parse($("#article-content").text(), {
    gfm: true,
    breaks: true,
    smartLists: true
});
$("#article-content").html(markdownText);
// hljs.highlightAll();
hljs.initLineNumbersOnLoad();

mermaid.initialize({
    'theme': 'base',
    'themeVariables': {
        'primaryColor': 'white',
        'textColor': 'rgb(62, 105, 232)',
        'primaryBorderColor': 'rgb(62, 105, 232)',
        'lineColor': 'rgb(62, 105, 232)',
        'primaryTextColor': 'rgb(62, 105, 232)'
    }
});