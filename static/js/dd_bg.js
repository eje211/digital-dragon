// Based on: <http://trendmedia.com/news/infinite-rotating-images-using-jquery-javascript/>
var InfiniteRotator = {
    init: function() {
        //initial fade-in time (in milliseconds)
        var initialFadeIn = 1000,
        //interval between items (in milliseconds)
            itemInterval  = 8000,
        //cross-fade time (in milliseconds)
            fadeTime      = 2500,
        //count number of items
            numberOfItems = $('.dd_bg_cont').length;
        //loop through the items
        var infiniteLoop = setInterval(function(){
            $('.dd_bg_cont').eq(window.current_bg_item).fadeOut(fadeTime);
            if (numberOfItems - 1 == window.current_bg_item)
                window.current_bg_item = 0;
            else window.current_bg_item++;

            var current_bg = window.backgrounds[window.current_bg_item];

            // We want the text fade to be slightly faster than the combined image fade.
            var textFade = (fadeTime - 500) / 2;
            $('#title-tag p').hide('slide', {direction: 'left'}, textFade, function() {
                $('#title-tag').html('');
                $.each(current_bg['text'], function(key, text) {
                    $('#title-tag').append('<p><a href="' + current_bg['link'] + '">' + text + '</a></p>');
                });
                $('#title-tag p').hide();
                $('#title-tag p').show('slide', {direction: 'left'}, textFade);
            });
            $('.dd_bg_cont').eq(window.current_bg_item).fadeIn(fadeTime);
        }, itemInterval);
    }
};

var set_img_data = function(elem, url) {
    var img = new Image();
    img.onload = function() {
        bg_width  = this.width;
        bg_height = this.height;
        bg_ratio  = this.width / this.height;
        resize_bg(elem, bg_width, bg_height, bg_ratio);
    }
    img.src = url;
}

var resize_bg = function(elem, bg_width, bg_height, bg_ratio) {
    var max_height = parseInt($(elem).css('max-height'));
    if ($(window).width() / bg_ratio >= max_height) {
        var width = $(window).width();
        var height = Math.round($(window).width() / bg_ratio);
    } else {
        var height = max_height;
        var width = max_height * bg_ratio;
    }
    $(elem).css({
        'background-size': '' + width + 'px ' + height + 'px' 
    });
}

var init_first_background = function () {
    var first_bg = {
        'url': $('.dd_bg_cont').eq(0).css('background-image').slice(4, -1),
        'text' : [],
        'link': $('#title-tag p a').attr('href'),
        'element' : $('.dd_bg_cont').eq(0)
    };
    $('#title-tag p').each(function(key, value) {first_bg['text'][key]= $(value).text();});
    window.backgrounds = [first_bg];
};

var init_backgrounds = function() {
    $.getJSON('/static/js/backgrounds.js', function(data) {
        // Add the new backgrounds to the DOM.
        $.each(data, function(key, image) {
            $('.dd_bg_cont').last().after('<div class="dd_bg_cont"></div>');
            $('.dd_bg_cont').last().css('background-image', 'url(' + image['url'] + ')');
            // Split each line of text into an array.
            image['text'] = image['text'].split('\\n');
            // Resize the background image for each new div.
            set_img_data($('.dd_bg_cont').last(), image['url']);
        });
        $.merge(window.backgrounds, data);
        $('.dd_bg_cont').each(function (key, value) {
            window.backgrounds[key]['element'] = value;
        });
        // Now add the backgrounds back to the array;
        InfiniteRotator.init();
    });
}

$(function() {
    //set current image rotator item
    window.current_bg_item = 0;
    
    // Create the background data based on the first background.
    init_first_background();

    set_img_data(window.backgrounds[0]['element'], window.backgrounds[0]['url']);
    window.backgrounds[0]['element'].show();
    init_backgrounds();
    $(window).resize(function() {
        set_img_data(window.backgrounds[window.current_bg_item]['element'], window.backgrounds[window.current_bg_item]['url']);
    });
});