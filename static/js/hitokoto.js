// hitokoto.js By HShiDianLu.
// Copyright © 2024 HShiDianLu. All Rights Reserved.
// Powered By Hitokoto.

// 动画
$(window).on('load', function () {
    setTimeout(function () {
        $(".bracket-left").css("left", "0");
        $(".bracket-left").css("top", "0");
        $(".bracket-right").css("right", "0");
        $(".bracket-right").css("bottom", "0");
        $(".bracket-right").css("opacity", "1");
        $(".bracket-left").css("opacity", "1");
        setTimeout(function () {
            $(".word").css("opacity", "1");
            $(".word").css("top", "0");
            setTimeout(function () {
                setTimeout(function () {
                    $("#string-op").css("opacity", "1");
                }, 150);
                $(".author").css("opacity", "1");
                $(".author").css("left", "-50px");
            }, 300);
        }, 150);
    }, 200);
});

// Tooltips

tippy("#string-change", {
    content: "换一换",
    placement: "bottom",
    animation: 'shift-away'
});

tippy("#string-copy", {
    content: "复制一言",
    placement: "bottom",
    animation: 'shift-away'
});

tippy("#string-disabled", {
    content: "隐藏 UI",
    placement: "bottom",
    animation: 'shift-away'
});

// 换一换

var btnRotate = 0;

function stringChange() {
    $(".word").css("opacity", "0");
    $(".author").css("opacity", "0");
    btnRotate += 360;
    $("#string-change svg").css("transform", "rotate(" + (btnRotate) + "deg)");
    var loadingInterval = setInterval(function () {
        btnRotate += 360;
        $("#string-change svg").css("transform", "rotate(" + (btnRotate) + "deg)");
    }, 1000)
    $.ajax({
        url: "/getHitokoto",
        type: "POST",
        success: function (result) {
            if (result['result'] == "success") {
                text = result['data']['content'];
                who = result['data']['from'];
                setTimeout(function () {
                    $(".word").text(result['data']['content']);
                    $(".author").text(result['data']['from']);
                    setTimeout(function () {
                        clearInterval(loadingInterval);
                        $(".word").css("opacity", "1");
                        $(".author").css("opacity", "1");
                    }, 100)
                }, 300)
            } else if (result['code'] == 1429) {
                clearInterval(loadingInterval);
                Swal.fire({
                    toast: true,
                    showConfirmButton: false,
                    icon: 'error',
                    timer: 2000,
                    title: '错误',
                    text: "操作过于频繁，请稍后再试。",
                    position: 'bottom-start'
                })
            } else {
                clearInterval(loadingInterval);
                Swal.fire({
                    toast: true,
                    showConfirmButton: false,
                    icon: 'error',
                    timer: 2000,
                    title: '错误',
                    text: "更换失败。错误码：" + result['code'],
                    position: 'bottom-start'
                })
            }
        }
    })
}

// 复制
function stringCopy() {
    copy(text + "  " + who);
    Swal.fire({
        toast: true,
        showConfirmButton: false,
        icon: 'success',
        timer: 2000,
        title: '复制成功',
        text: "一言已复制到您的剪贴板。",
        position: 'bottom-start'
    })
}

// 隐藏UI

var UIState = true;

function stringDisabled() {
    if (!UIState) {
        return;
    }
    $("#footer-hitokoto").css("opacity", "0");
    $("#navbar").css("opacity", "0");
    $("#string-op").css("opacity", "0");
    Swal.fire({
        toast: true,
        showConfirmButton: false,
        icon: 'info',
        timer: 2000,
        title: '已隐藏 UI',
        text: "轻点屏幕以重新显示 UI。",
        position: 'bottom-start'
    })
    setTimeout(function () {
        $("#footer-hitokoto").css("display", "none");
        $("#navbar").css("display", "none");
        $("#string-op").css("display", "none");
        UIState = false;
    }, 300)
}

$(document).click(function () {
    if (UIState) {
        return;
    }
    $("#footer-hitokoto").css("display", "block");
    $("#navbar").css("display", "block");
    $("#string-op").css("display", "inline-block");
    setTimeout(function () {
        $("#footer-hitokoto").css("opacity", "1");
        $("#navbar").css("opacity", "1");
        $("#string-op").css("opacity", "1");
    }, 1)
    setTimeout(function () {
        UIState = true;
    }, 300)
})