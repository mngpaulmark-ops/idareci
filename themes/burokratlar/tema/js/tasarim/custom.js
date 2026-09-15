$(function () {
    $(document).on("click", ".icon", function() {
        if ($(window).width() <= 1000) {
            $('.left-menu').slideToggle(300);
        } else {
            var leftitem = $('.left-menu');
            if (leftitem.css("margin-left") == "-400px") {
                leftitem.fadeIn().animate({"margin-left" : 0}, {duration: 200, queue: false});
            } else {
                leftitem.fadeIn().animate({"margin-left" : "-400px"}, {duration: 200, queue: false});
            }
        }
    });
});