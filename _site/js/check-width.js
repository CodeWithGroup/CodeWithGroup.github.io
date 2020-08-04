$(function () {
    var $window = $(window);
    var $pane = $('#main-container');

    function checkWidth() {
        var windowsize = $window.width();
        if (windowsize < 768) {
            if ($pane.hasClass('toggled')) {
                $pane.toggleClass('toggled');
            }
        }
        else if (!$pane.hasClass('toggled')) {
            $pane.addClass('toggled');
        }
    }

    // Execute on load
    checkWidth();
    // Bind event listener
    $(window).resize(checkWidth);
});