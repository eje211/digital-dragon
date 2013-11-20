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
            numberOfItems = $('.dd_bg_cont').length,
        // We want the text fade to be slightly faster than the combined image fade.
            textFade = (fadeTime - 500) / 2;

        //loop through the items
        var infiniteLoop = setInterval(function(){
            $('.dd_bg_cont').eq(window.current_bg_item).fadeOut(fadeTime);
            // Rotate through item numbers;
            window.current_bg_item = ++window.current_bg_item % numberOfItems;
            // This is easier to read.
            var current_bg = window.backgrounds[window.current_bg_item];

            $('#title-tag p').hide('slide', {direction: 'left'}, textFade, function() {
                $('#title-tag').html('');
                $.each(current_bg['text'], function(key, text) {
                    $('#title-tag').append('<p><a href="' + current_bg['link'] + '">' + text + '</a></p>');
                });
                $('#title-tag p').hide();
                $('#title-tag p').show('slide', {direction: 'left'}, textFade);
            });
            $(current_bg['element']).fadeIn(fadeTime);
            // Reset the element's size, just in case.
            set_img_data(current_bg['element'], current_bg['url']);
        }, itemInterval);
    }
};

var set_img_data = function(elem, url) {
    // Only refresh image data if we have to.
    if (set_img_data.url === url) return resize_bg(elem);
    set_img_data.url = url;
    var img = new Image();
    img.onload = function() {
        set_img_data.bg_width = this.width;
        set_img_data.bg_ratio = this.width / this.height;
        resize_bg(elem);
    }
    img.src = url;
}

var resize_bg = function(elem) {
    var max_height = parseInt($(elem).css('max-height'));
    if ($(window).width() / set_img_data.bg_ratio >= max_height) {
        var width = $(window).width(),
            height = Math.round($(window).width() / set_img_data.bg_ratio);
    } else {
        var height = max_height,
            width = max_height * set_img_data.bg_ratio;
    }
    $(elem).css({
        'background-size': '' + width + 'px ' + height + 'px' 
    });
}

var resize_callback = function() {
    resize_callback.current_bg_item = window.current_bg_item;

    set_img_data(window.backgrounds[window.current_bg_item]['element'], window.backgrounds[window.current_bg_item]['url']);
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
            image['text'] = image['text'].split('\n');
            // Resize the background image for each new div.
            set_img_data($('.dd_bg_cont').last(), image['url']);
        });
        $.merge(window.backgrounds, data);
        // Set the "element" value to each item in the array.s
        $('.dd_bg_cont').each(function (key, value) {
            window.backgrounds[key]['element'] = value;
        });
        // Now that we have all the data we need, start the rotation.
        InfiniteRotator.init();
    });
}

$(function() {
    // Set current image rotation item
    window.current_bg_item = 0;
    
    // Create the background data based on the first background.
    init_first_background();

    // Resize and show original background.
    set_img_data(window.backgrounds[0]['element'], window.backgrounds[0]['url']);
    window.backgrounds[0]['element'].show();

    // Get all the other backgrounds if we're on the index page.
    if (window.location.pathname === "/") init_backgrounds();

    // Set resize callback.
    $(window).resize(resize_callback);
});