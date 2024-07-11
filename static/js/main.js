// main.js By HShiDianLu.
// Copyright © 2024 HShiDianLu. All Rights Reserved.

// 链接转跳
function link(id) {
    $("#" + id).click();
}

// 返回顶部

var topState = true;

function back() {
    if (topState) {
        return
    }
    $("html,body").finish().animate({"scrollTop": 0}, 500);
    $("#back-to-top").css("transform", "scale(0%)");
    $("#back-to-top").css("opacity", "0");
    topState = true;
    setTimeout(function () {
        $("#back-to-top").css("display", "none");
    }, 300)
}

setInterval(function () {
    if ($(document).scrollTop() >= 100 && topState) {
        topState = false;
        $("#back-to-top").css("display", "block");
        setTimeout(function () {
            $("#back-to-top").css("transform", "scale(100%)");
            $("#back-to-top").css("opacity", "1");
        }, 300)
    } else if ($(document).scrollTop() < 100 && !topState) {
        topState = true;
        $("#back-to-top").css("transform", "scale(0%)");
        $("#back-to-top").css("opacity", "0");
        setTimeout(function () {
            $("#back-to-top").css("display", "none");
        }, 300)
    }
    if (windowOpen) {
        if ($(window).width() * 0.8 > 800) {
            $("#login-window").css("width", "800px");
        } else {
            $("#login-window").css("width", "80%");
        }
    }
}, 0)

// 滚动定位
function scroll(element) {
    $("html,body").finish().animate({"scrollTop": $(element).offset().top - 85}, 500);
}

// 平滑加载

function appear(i) {
    var blocks = document.getElementsByClassName("block");
    blocks[i].style.opacity = "1";
    blocks[i].style.top = "0";
}

function contentOut() {
    var basic = 100;
    var blocks = document.getElementsByClassName("block");
    for (var i = 0; i < blocks.length; i++) {
        setTimeout("appear(" + i + ")", basic * i);
    }
}

// 登录 & 注册

var closeTimeout;
var windowOpen = false;

function close() {
    windowOpen = false;
    $("#login-box").css("opacity", "0");
    $("#recaptcha-text").css("color", "white");
    $(".recaptcha-link").css("opacity", "0");
    setTimeout(function () {
        $("#login-bg").css("opacity", "0");
        $("#login-window").css("width", "0");
    }, 100)
    setTimeout(function () {
        $(".error").css("opacity", "0");
        if (windowState) {
            switchWindow();
        }
    }, 600)
    closeTimeout = setTimeout(function () {
        $("#login-bg").css("display", "none");
        $(".input-data input").val("");
    }, 500)
}

$.ajax({
    url: "/getImg",
    type: "POST",
    success: function (result) {
        var img = document.getElementById("login-img");
        try {
            img.src = result['url'];
            img.title = result['copyright'];
            $(".fadeImg").css("opacity", "1");
        } catch (error) {
            console.warn(error);
        }
    }
})

function openLogin() {
    windowOpen = true;
    clearTimeout(closeTimeout);
    $("#login-bg").css("display", "block");
    setTimeout(function () {
        $("#login-bg").css("opacity", "1");
        if ($(window).width() * 0.8 > 800) {
            $("#login-window").css("width", "800px");
        } else {
            $("#login-window").css("width", "80%");
        }
        setTimeout(function () {
            $("#login-box").css("opacity", "1");
            $("#recaptcha-text").css("color", "darkgray");
            $(".recaptcha-link").css("opacity", "1");
        }, 100)
    }, 1)
}

var windowState = false;

function switchWindow() {
    if (ajaxRespond) {
        return;
    }
    var input2 = document.getElementById("input2");
    $("#reg-btn").css("color", "white");
    $("#login-btn").css("color", "rgb(62, 105, 232)");
    $("#input1-label").css("opacity", "0");
    $("#input2-label").css("opacity", "0");
    $("#login-box h3").css("opacity", "0");
    $(".error").css("opacity", "0");
    if (!windowState) {
        usernameTippy.enable();
        passwordTippy.enable();
        $(".input-data input").val("")
        input2.type = "text";
        $("#login-window").css("height", "650px");
        $("#login-btngroup").css("top", "0");
        $("#login-box").css("padding-top", "35px");
        setTimeout(function () {
            $(".reg input").css("cursor", "text");
            $(".reg").css("opacity", "1");
        }, 200)
        setTimeout(function () {
            $("#login-box h3").html("注册 <small>Register</small>");
            $("#reg-btn").text("登录");
            $("#login-btn").text("注册");
            $("#input1-label").text("邮箱");
            $("#input2-label").text("用户名");
        }, 300)
        windowState = true;
    } else {
        usernameTippy.disable();
        passwordTippy.disable();
        input2.type = "password";
        $(".reg").css("opacity", "0");
        $(".common input").val("");
        setTimeout(function () {
            $("#login-window").css("height", "550px");
            $("#login-box").css("padding-top", "70px");
            $("#login-btngroup").css("top", "-180px");
        }, 200)
        setTimeout(function () {
            $(".reg input").css("cursor", "default");
            $(".reg input").val("");
        }, 300)
        setTimeout(function () {
            $("#login-box h3").html("登录 <small>Login</small>");
            $("#reg-btn").text("注册");
            $("#login-btn").text("登录");
            $("#input1-label").text("用户名 / 邮箱");
            $("#input2-label").text("密码");
        }, 300)
        windowState = false;
    }
    setTimeout(function () {
        $("#input1-label").css("opacity", "1");
        $("#input2-label").css("opacity", "1");
        $("#login-btn").css("color", "white");
        $("#reg-btn").css("color", "");
        $("#login-box h3").css("opacity", "1");
    }, 300)
}

function errorDetect(num) {
    var err = false;
    for (var i = 1; i <= num; i++) {
        if ($("#input" + i).val() == "") {
            $("#input" + i + "-err").text($("#input" + i + "-label").text() + "不能为空");
            $("#input" + i + "-err").css("opacity", "1");
            err = true;
        } else {
            $("#input" + i + "-err").css("opacity", "0");
        }
    }
    return err;
}

function validUsername(username) {
    if (username.length < 4) {
        return 1;
    }
    if (username.length > 16) {
        return 2;
    }
    var reg = /^[a-zA-Z0-9_]+$/;
    if (!reg.test(username)) {
        return 3;
    }
    if (/\s/.test(username)) {
        return 4;
    }
    return 0;
}

function validPassword(password) {
    if (password.length < 8) {
        return 1;
    }
    var reg = new RegExp(/^(?![^a-zA-Z]+$)(?!\D+$)/);
    if (reg.test(password)) {
        return 0;
    } else {
        return 2;
    }
}

function validEmail(str) {
    var reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
    return reg.test(str);
}

var ajaxRespond = false;

grecaptcha.ready(function () {
    if (!loginState) {
        var loginBtn = document.getElementById("nav-login");
        loginBtn.onclick = openLogin;
        $("#nav-login").removeClass("disabled-reverse");
    }
})

function login() {
    if (ajaxRespond) {
        return;
    }
    if (!windowState) { // login
        if (errorDetect(2)) {
            return;
        }
        grecaptcha.ready(function () {
            ajaxRespond = true;
            $("#login-btn").addClass("disabled-reverse");
            $("#reg-btn").addClass("disabled-btn");
            $("#login-btn").text("请稍后");
            grecaptcha.execute('6LfgeG8pAAAAALgQp-eRF91eLXmmYuVUcExV_nl2', {action: 'login'}).then(function (token) {
                $.ajax({
                    url: "/login",
                    data: {
                        'username': $("#input1").val(),
                        'password': $("#input2").val(),
                        'token': token
                    },
                    type: "POST",
                    success: function (result) {
                        if (result['result'] == "success") {
                            location.reload(true);
                            $("#loader-background").css("display", "block");
                            setTimeout(function () {
                                // $(".loader").css("opacity", "1");
                                $("#loader-background").css("opacity", "1");
                            }, 1)
                        } else if (result['code'] == 1002) {
                            $("#input2-err").text("用户名或密码错误");
                            $("#input2-err").css("opacity", "1");
                        } else if (result['code'] == 1009) {
                            $("#input2-err").html("您尚未通过邮箱验证。请验证邮箱后重试。");
                            $("#input2-err").css("opacity", "1");
                        } else {
                            $("#input2-err").text("登录失败。错误码：" + result['code']);
                            $("#input2-err").css("opacity", "1");
                        }
                        ajaxRespond = false;
                        $("#login-btn").removeClass("disabled-reverse");
                        $("#reg-btn").removeClass("disabled-btn");
                        $("#login-btn").text("登录");
                    }
                })
            });
        });
    } else { // reg
        var valid = true;
        if (errorDetect(4)) {
            return;
        }
        if ($("#input3").val() != $("#input4").val()) {
            $("#input4-err").text("密码与确认密码不一致");
            $("#input4-err").css("opacity", "1");
            valid = false;
        }
        var validU = validUsername($("#input2").val());
        if (validU != 0) {
            switch (validU) {
                case 1:
                    $("#input2-err").text("用户名长度至少为4位");
                    break;
                case 2:
                    $("#input2-err").text("用户名长度最多为16位");
                    break;
                case 3:
                    $("#input2-err").text("用户名仅能由字母、数字、下划线组成");
                    break;
                case 4:
                    $("#input2-err").text("用户名不能包含空格");
                    break;
            }
            $("#input2-err").css("opacity", "1");
            valid = false;
        }
        if (!validEmail($("#input1").val())) {
            $("#input1-err").text("邮箱格式错误");
            $("#input1-err").css("opacity", "1");
            valid = false;
        }
        var validP = validPassword($("#input3").val());
        if (validP != 0) {
            switch (validP) {
                case 1:
                    $("#input3-err").text("密码长度至少为8位");
                    break;
                case 2:
                    $("#input3-err").text("密码须同时包含数字与字母");
                    break;
            }
            $("#input3-err").css("opacity", "1");
            valid = false;
        }
        if (!valid) {
            return;
        }
        grecaptcha.ready(function () {
            ajaxRespond = true;
            $("#login-btn").addClass("disabled-reverse");
            $("#reg-btn").addClass("disabled-btn");
            $("#login-btn").text("请稍后");
            grecaptcha.execute('6LfgeG8pAAAAALgQp-eRF91eLXmmYuVUcExV_nl2', {action: 'register'}).then(function (token) {
                $.ajax({
                    url: "/register",
                    type: "POST",
                    data: {
                        'email': $("#input1").val(),
                        'username': $("#input2").val(),
                        'password': $("#input3").val(),
                        'token': token
                    },
                    success: function (result) {
                        if (result['result'] == "success") {
                            close();
                            setTimeout(function () {
                                swal({
                                    title: "请验证邮箱",
                                    text: "我们已向您的邮箱发送了一封邮件，请在邮件中点击地址以进行验证。（邮件可能会被判定为垃圾邮件）",
                                    icon: "info",
                                    button: "确定",
                                });
                            }, 600)
                        } else if (result['code'] == 1003) {
                            $("#input2-err").text("用户名包含敏感词");
                            $("#input2-err").css("opacity", "1");
                        } else if (result['code'] == 1004) {
                            $("#input1-err").text("邮箱信息错误");
                            $("#input1-err").css("opacity", "1");
                        } else if (result['code'] == 1006) {
                            $("#input2-err").text("用户名已被使用");
                            $("#input2-err").css("opacity", "1");
                        } else if (result['code'] == 1007) {
                            $("#input1-err").text("邮箱已被注册");
                            $("#input1-err").css("opacity", "1");
                        } else if (result['code'] == 1008) {
                            $("#input4-err").text("邮件发送失败。请稍后重试。");
                            $("#input4-err").css("opacity", "1");
                        } else {
                            $("#input4-err").text("注册失败。错误码：" + result['code']);
                            $("#input4-err").css("opacity", "1");
                        }
                        ajaxRespond = false;
                        $("#login-btn").removeClass("disabled-reverse");
                        $("#reg-btn").removeClass("disabled-btn");
                        $("#login-btn").text("注册");
                    }
                })
            })
        })
    }
}

// (用户) Dropdown

var drop;

$(".dropdown").hover(function () {
    clearTimeout(drop);
    $(".dropdown-content").css("display", "block");
    setTimeout(function () {
        $(".dropdown-content").css("opacity", "1");
    }, 1)
    $(".dropdown-svg").css("transform", "rotate(0deg)");
}, function () {
    $(".dropdown-content").css("opacity", "0");
    drop = setTimeout(function () {
        $(".dropdown-content").css("display", "none");
    }, 300)
    $(".dropdown-svg").css("transform", "rotate(180deg)");
})

// 旧版 Dropdown Event

// var dropdownState = false;

// function dropdown() {
//     if (!dropdownState) {
//         clearTimeout(drop);
//         $(".dropdown-content").css("display", "block");
//         setTimeout(function () {
//             $(".dropdown-content").css("opacity", "1");
//         }, 1)
//         $(".dropdown-svg").css("transform", "rotate(0deg)");
//         dropdownState = true;
//     } else {
//         $(".dropdown-content").css("opacity", "0");
//         drop = setTimeout(function () {
//             $(".dropdown-content").css("display", "none");
//         }, 300)
//         $(".dropdown-svg").css("transform", "rotate(180deg)");
//         dropdownState = false;
//     }
// }
//
// $(document).on("click", function (event) {
//     if (!$(event.target).closest(".dropdown").length) {
//         $(".dropdown-content").css("opacity", "0");
//         drop = setTimeout(function () {
//             $(".dropdown-content").css("display", "none");
//         }, 300)
//         $(".dropdown-svg").css("transform", "rotate(180deg)");
//         dropdownState = false;
//     }
// });

$(".dropdown-content a").hover(function () {
    $(".dropdown-content").css("width", "100px");
    $(".dropdown-content svg").css("left", "-5px");
}, function () {
    $(".dropdown-content").css("width", "80px");
    $(".dropdown-content svg").css("left", "10px");
})

// 随机数
function randomNum(minNum, maxNum) {
    switch (arguments.length) {
        case 1:
            return parseInt(Math.random() * minNum + 1, 10);
            break;
        case 2:
            return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
            break;
        default:
            return 0;
            break;
    }
}

// 复制
function copy(text) {
    var input = $('<input value="' + text + '"/>');
    $("body").prepend(input);
    $("body").find("input").eq(0).select();
    document.execCommand("copy");
    $("body").find("input").eq(0).remove();
}

// Loading

// In

$(".loader").css("opacity", "1");
$("#navbar").css("opacity", "1");

var autoContentOut = true;

function websiteIn() {
    $(".loader").css("opacity", "0");
    $("#loader-background").css("opacity", "0");
    setTimeout(function () {
        $(".loader").css("display", "none");
        $("#loader-background").css("display", "none");
    }, 300)
    if (autoContentOut) {
        contentOut();
    }
}

$(window).on('load', function () {
    websiteIn();
    clearTimeout(loadTimeout);
});

// ForceIn
var loadTimeout = setTimeout(function () {
    websiteIn();
    Swal.fire({
        toast: true,
        showConfirmButton: false,
        icon: 'warning',
        timer: 4000,
        title: '加载超时',
        text: "加载时间过长，已为您强制显示网页。部分功能将在完全加载后可用。",
        position: 'bottom-start'
    })
}, 4000)

// Out
function hrefTo(url) {
    window.location.href = url;
    $("#loader-background").css("display", "block");
    setTimeout(function () {
        // $(".loader").css("opacity", "1");
        $("#loader-background").css("opacity", "1");
    }, 1)
}

// 日期转化

var dates = document.getElementsByClassName("convert-date");
for (var i = 0; i < dates.length; i++) {
    tippy("#" + dates[i].id, {
        content: $(dates[i]).text(),
        placement: "bottom",
        animation: 'shift-away'
    });
    $(dates[i]).text(moment($(dates[i]).text()).fromNow());
}

var datesKeep = document.getElementsByClassName("convert-date-keep");
for (var i = 0; i < datesKeep.length; i++) {
    $(datesKeep[i]).prepend(moment($(datesKeep[i]).text()).fromNow() + " · ");
}

// Login Box Tippy

var passwordTippy = tippy("#input3", {
    content: "至少8位，须同时包含字母与数字",
    placement: "left",
    animation: 'shift-away',
    distance: 20,
    hideOnClick: false
})[0];

var usernameTippy = tippy("#input2", {
    content: "4~16位，仅能由字母、数字、下划线组成",
    placement: "left",
    animation: 'shift-away',
    distance: 20,
    hideOnClick: false,
    theme: ""
})[0];

try {
    usernameTippy.disable();
    passwordTippy.disable();
} catch (error) {
    console.warn(error);
}