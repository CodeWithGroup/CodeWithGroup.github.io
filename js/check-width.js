"use strict"

$(function () {
    var $window = $(window);
    var $pane = $('#main-container');

    // Store the window width
    var windowWidth = $window.width();

    function checkWidth(reload) {
        console.log(reload)
        if (!reload) {
            if ($(window).width() === windowWidth) { //prevents the sidebar being opened on scroll on Apple browsers
                checkWidthToggleClass();
            }
        } else {
            checkWidthToggleClass();
        }
    }

    function checkWidthToggleClass() {
        var windowsize = $window.width();
        if (windowsize <= 768) {
            if ($pane.hasClass('toggled')) {
                $pane.toggleClass('toggled');
            }
        }
        else if (!$pane.hasClass('toggled')) {
            $pane.addClass('toggled');
        }
    }

    // Execute on load
    checkWidth(true);
    // Bind event listener
    $(window).resize(checkWidth(false));
});