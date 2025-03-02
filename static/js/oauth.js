// oauth.js By HShiDianLu.
// Copyright © 2024-2025 HShiDianLu. All Rights Reserved.


// Override

autoContentOut = false;

function websiteIn() {
    // Here shouldn't do anything
}

// OAuth Main

setTimeout(function () {
    $("#oauth-text").css("opacity", "1");
}, 100)

$.ajax({
    url: "/oauth/github/login",
    type: "POST",
    data: {
        'code': code
    },
    success: function (result) {
        setTimeout(function () {
            $(".loader").css("opacity", "0");
        }, 700)
        $("#oauth-text").css("opacity", "0");
        setTimeout(function () {
            if (result['result'] === "success") {
                window.location.href = to;
            } else {
                let errorDetail = result['code'];
                if (result['code'] === 1015) {
                    errorDetail = result['data'];
                } else {
                    errorDetail = errorCodeMapping(errorDetail);
                }
                if (result['code'] === 1005) {
                    errorDetail += "。";
                }
                swal({
                    icon: 'error',
                    title: '登录失败',
                    text: errorDetail,
                    buttons: {back: "返回"},
                    closeOnClickOutside: false,
                }).then((result) => {
                    window.location.href = to;
                })
            }
        }, 700)
    }
})