"use strict"

$(function () {
    $(document).ready(function () {
        if (localStorage.getItem("CodeWithOpenDyslexic") === "1") {
            $('body').toggleClass('open-dyslexic');
        }
    });

    $('#change-font').click(function () {
        if (localStorage.getItem("CodeWithOpenDyslexic") === "1") {
            localStorage.setItem("CodeWithOpenDyslexic", 0);
        } else {
            localStorage.setItem("CodeWithOpenDyslexic", 1);
        }

        $('body').toggleClass('open-dyslexic');
    });
})