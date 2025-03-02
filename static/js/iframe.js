// iframe.js By HShiDianLu.
// Copyright © 2024-2025 HShiDianLu. All Rights Reserved.

function changeFrameHeight() {
    let iframe = document.getElementById("iframe");
    iframe.height = document.documentElement.clientHeight - 60;
}

$("body").append("<iframe id=\"iframe\"\n" +
    "        name=\"iframe\"\n" +
    "        height=\"100%\"\n" +
    "        width=\"100%\"\n" +
    "        src=\"" + iframeLink + "\"\n" +
    "        scrolling=\"auto\"\n" +
    "        frameborder=\"0\"\n" +
    "        onload=\"changeFrameHeight()\">\n" +
    "</iframe>");

$("iframe").css("opacity", "1");

window.onresize = function () {
    changeFrameHeight();
}