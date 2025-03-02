// homework.js By HShiDianLu.
// Copyright © 2024-2025 HShiDianLu. All Rights Reserved.

if (hitokoto) {
    if (hitokoto['from_who'] == null) {
        hitokoto['from_who'] = "";
    }
    $("#hw-yy").text(hitokoto['hitokoto'])
    $("#hw-yy-src").text("—— " + hitokoto['from_who'] + "「" + hitokoto['from'] + "」");
    $("#hw-yy-inner").css("width", Math.max(parseFloat($("#hw-yy").css("width")), parseFloat($("#hw-yy-src").css("width"))));
}

function toggleAcc(element) {
    console.log($(element).parent().attr('class').split(' ').indexOf("acc-open"));
    if ($(element).parent().attr('class').split(' ').indexOf("acc-open") !== -1) {
        $(element).parent().removeClass("acc-open");
    } else {
        $(element).parent().addClass("acc-open");
    }
}

function expandPre() {
    setTimeout(expand, 100);
}

function expand() {
    $(".progress").css("top", "-20px");
    $("#hw-yy").css("left", "0");
    $("#hw-yy-src").css("left", "0");
    $("#hw-yy").css("opacity", "1");
    $("#hw-yy-src").css("opacity", "1");
    // if (Cookie.get("updTime") !== updTime) {
    //     Cookie.set("updTime", updTime, "2026-12-31");
    //     for (let i = 0; i <= hwLen; i++) {
    //         Cookie.remove("h" + i);
    //     }
    // }
    for (let i in finishes) {
        console.log(i);
        if (Cookie.get("h" + i) === "1") {
            $("#checkbox-" + i).click();
        }
    }
    for (let i = 0; i < 9; i++) {
        if (finishCa[i] !== caLen[i]) {
            $("#ca-" + i).addClass("acc-open");
        }
    }
}

let expandTimeout = setTimeout(expandPre, 4000);

$(window).on('load', function () {
    expandPre();
    clearTimeout(expandTimeout);
});

let finishCa = [0, 0, 0, 0, 0, 0, 0, 0, 0];

function upd() {
    let sum = 0;
    for (let i = 0; i < 9; i++) {
        let text = "未完成";
        if (finishCa[i] === caLen[i]) {
            text = "已完成";
            $("#ca-" + i).removeClass("acc-open");
        }
        sum += finishCa[i];
        $("#progress-" + i).css("width", Math.ceil(finishCa[i] / hwLen * 100) + "%");
        $("#progress-" + i).text((finishCa[i] / hwLen * 100).toFixed(1) + "%");
        $("#complete-" + i).text(text + " " + finishCa[i] + "/" + caLen[i]);
    }
    if (sum === hwLen) {
        swal({
            title: "恭喜！",
            text: "你完成了全部的作业！伸个懒腰，放松一下吧。",
            icon: "info",
            button: "关闭",
        });

        let end = Date.now() + 1000;

        (function frame() {
            confetti({
                particleCount: 5,
                angle: 60,
                spread: 55,
                startVelocity: randomNum(30, 70),
                gravity: randomNum(1, 10) / 10,
                tick: 1000,
                origin: {x: 0, y: 1}
            });
            confetti({
                particleCount: 5,
                angle: 120,
                spread: 55,
                startVelocity: randomNum(30, 70),
                gravity: randomNum(1, 10) / 10,
                tick: 1000,
                origin: {x: 1, y: 1}
            });
            if (Date.now() < end) {
                requestAnimationFrame(frame);
            }
        }());
    }
}

function finishHw(id) {
    if (!finishes[id]) {
        $("#detail-" + id).css("color", "gray");
        $("#row-id-" + id).css("color", "gray");
        $("#delete-line-" + id).css("width", 90 + parseFloat($("#detail-" + id).css("width")));
        finishes[id] = true;
        finishCa[hws[id][0]]++;
        Cookie.set("h" + id, "1", "2026-12-31")
    } else {
        $("#detail-" + id).css("color", "black");
        $("#row-id-" + id).css("color", "black");
        $("#delete-line-" + id).css("width", 0);
        finishes[id] = false;
        finishCa[hws[id][0]]--;
        Cookie.remove("h" + id)
    }
    upd();
}