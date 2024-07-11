// status.js By HShiDianLu.
// Copyright © 2024 HShiDianLu. All Rights Reserved.

$(window).on('load', function () {
    $("#sleep-box").css("height", "295px");
    setTimeout(function () {
        $("#sleep-inner").css("opacity", "1");
        setTimeout(function () {
            $("#sleep-box h2").css("opacity", "1");
            $("#sleep-date-outer").css("opacity", "1");
        }, 300)
        $("#sleep-box .split-line").css("width", "150px");
    }, 300);
});

var dateTippy = tippy("#sleep-date", {
    content: $("#sleep-date").text(),
    placement: "bottom",
    animation: 'shift-away'
})[0];
$("#sleep-date").text(moment($("#sleep-date").text()).fromNow());

setInterval(function () {
    $.ajax({
        url: "/status",
        type: "POST",
        success: function (result) {
            console.log(result)
            $("#sleep-box h2").text(result['data']['status'])
            dateTippy.setContent(result['data']['time']);
            $("#sleep-date").text(moment(result['data']['time']).fromNow());
        }
    })
}, 30000)