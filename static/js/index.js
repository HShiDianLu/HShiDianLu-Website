// index.js By HShiDianLu.
// Copyright © 2024-2025 HShiDianLu. All Rights Reserved.

// 一言

function loadHitokoto() {
    if (hitokoto) {
        $("#yy").text(hitokoto['hitokoto'])
        let src = true;
        // if (!(hitokoto['from'] == "网友" || hitokoto['from'] == "原创" || hitokoto['from'] == "网易云" || hitokoto['from'] == "网络" || hitokoto['from'] == "QQ音乐")) {
        if (hitokoto['from_who'] == null) {
            hitokoto['from_who'] = "";
        }
        $("#yy-src").text("—— " + hitokoto['from_who'] + "「" + hitokoto['from'] + "」");
        //     src = true;
        // }
        $("#yy-box").css("width", Math.max(parseFloat($("#yy").css("width")), parseFloat($("#yy-src").css("width"))) + "px");
        let offset = 115;
        if (!src) {
            offset = 85;
        }
        $("#title-box").css("height", parseFloat($("#yy-box").css("height")) + offset + "px");
        setTimeout(function () {
            $("#yy-box").css("opacity", "1");
            $("#top-split").css("width", "150px");
        }, 500)
        setTimeout(function () {
            contentOut();
        }, 300)
    } else {
        $("#top-split").css("display", "none");
        contentOut();
    }
}

// Override

autoContentOut = false;

let loadHitokotoTimeout = setTimeout(function () {
    loadHitokoto();
}, 4000)

$(window).on('load', function () {
    loadHitokoto();
    clearTimeout(loadHitokotoTimeout);
});

// 复制IGN
function copyMinecraft() {
    copy("HSh1DianLu");
    Swal.fire({
        toast: true,
        showConfirmButton: false,
        icon: 'success',
        timer: 2000,
        title: '复制成功',
        text: "游戏ID已复制到您的剪贴板。",
        position: 'bottom-start'
    })
}