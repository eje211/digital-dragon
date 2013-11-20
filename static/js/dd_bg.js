/**
 * Rotate the top banner picture on the index page.
 * At each rotation, also swipe in and out the banner text.
 * Based on: <http://trendmedia.com/news/infinite-rotating-images-using-jquery-javascript/>
 */
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

/**
 * Gather the size of the background image of a div so that
 * it can then be resized accordingly.
 *
 * var elem: the element to be resized.
 * var url : the URL of that element's background image.
 *
 * NOTE: The url variable could be gathered from the element's
 * CSS properties but it's simpler to just keep it in
 * window.backgrounds and pass it when needed.
 */
var set_img_data = function(elem, url) {
    // Only refresh image data if we have to.
    if (set_img_data.url === url) return _resize_bg(elem);
    set_img_data.url = url;
    var img = new Image();
    img.onload = function() {
        set_img_data.bg_width = this.width;
        set_img_data.bg_ratio = this.width / this.height;
        _resize_bg(elem);
    }
    img.src = url;
}

/**
 * Resize a background div based on its background-image
 * property, as supplied by the set_img_data() function.
 * NOTE: Pseaudo-private function: this function should
 * only ever be called by set_img_data().
 * 
 * var elem: the element to be resized.
 */
var _resize_bg = function(elem) {
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

/**
 * What to do when the main window is resized:
 * reset the size of the background image of the div accordinly.
 */
var resize_callback = function() {
    set_img_data(
        window.backgrounds[window.current_bg_item]['element'],
        window.backgrounds[window.current_bg_item]['url']
    );
}

/**
 * Gather information about the first backrgound item
 * so that it can be included in the rotation.
 */
var init_first_background = function () {
    var first_bg = {
        'url': $('.dd_bg_cont').eq(0).css('background-image').slice(4, -1),
        'text' : [],
        'link': $('#title-tag p a').attr('href'),
        'element' : $('.dd_bg_cont').eq(0)
    };
    // Put each line of the tag text into an array cell.
    $('#title-tag p').each(function(key, value) {first_bg['text'][key] = $(value).text();});
    window.backgrounds = [first_bg];
};

/**
 * Get data from the JSON file and create new DIVs for the
 * rotating backgrounds based on it. Also save a record
 * of that data in window.backgrounds .
 */
var init_backgrounds = function() {
    $.getJSON('/static/js/backgrounds.js', function(data) {
        // Add the new backgrounds to the DOM.
        $.each(data, function(key, image) {
            // For each new entry, create a DIV after the last one.
            $('.dd_bg_cont').last().after('<div class="dd_bg_cont"></div>');
            // Set its background image.
            $('.dd_bg_cont').last().css('background-image', 'url(' + image['url'] + ')');
            // Split each line of text into an array.
            image['text'] = image['text'].split('\n');
            // Resize the background image.
            set_img_data($('.dd_bg_cont').last(), image['url']);
        });
        // Add all the DIVs we've added to window.backgrounds .
        $.merge(window.backgrounds, data);
        // Set the "element" value to each item in the array.
        $('.dd_bg_cont').each(function (key, value) {
            window.backgrounds[key]['element'] = value;
        });
        // Now that we have all the data we need, start the rotation.
        InfiniteRotator.init();
    });
}

/**
 * Main fuction. Start everything.
 */
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