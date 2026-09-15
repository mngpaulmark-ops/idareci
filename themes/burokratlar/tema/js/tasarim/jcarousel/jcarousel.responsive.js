(function($) {
    $(function() {
        var jcarousel = $('.fotogaleri');

        jcarousel
            .on('jcarousel:reload jcarousel:create', function () {
                var carousel = $(this),
                    width = carousel.innerWidth();

                if (width >= 768) {
                    width = width / 4;
                } else if (width >= 600) {
                    width = width / 3;
                } else if (width >= 350) {
                    width = width / 2;
                }

                carousel.jcarousel('items').css('width', Math.ceil(width) + 'px');
            })
            .jcarousel({
                wrap: 'circular'
            }).jcarouselAutoscroll({
				interval: 3000,
				target: '+=1',
				autostart: true
			});

        $('.sol_f')
            .jcarouselControl({
                target: '-=1'
            });

        $('.sag_f')
            .jcarouselControl({
                target: '+=1'
            });
		
		$('.jcarousel').hover(function() {
				$(this).jcarouselAutoscroll('stop');
			}, function() {
				$(this).jcarouselAutoscroll('start');
			});
		
    });
	
	
	$(function() {
        var jcarousel = $('.videogaleri');

        jcarousel
            .on('jcarousel:reload jcarousel:create', function () {
                var carousel = $(this),
                    width = carousel.innerWidth();

                if (width >= 768) {
                    width = width / 4;
                } else if (width >= 600) {
                    width = width / 3;
                } else if (width >= 350) {
                    width = width / 2;
                }

                carousel.jcarousel('items').css('width', Math.ceil(width) + 'px');
            })
            .jcarousel({
                wrap: 'circular'
            }).jcarouselAutoscroll({
				interval: 3000,
				target: '+=1',
				autostart: true
			});

        $('.sol_v')
            .jcarouselControl({
                target: '-=1'
            });

        $('.sag_v')
            .jcarouselControl({
                target: '+=1'
            });
			
		$('.jcarousel').hover(function() {
				$(this).jcarouselAutoscroll('stop');
			}, function() {
				$(this).jcarouselAutoscroll('start');
			});

    });
})(jQuery);
