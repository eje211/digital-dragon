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
        }, itemInterval);
    }
};

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

    // Show original background.
    window.backgrounds[0]['element'].show();

    // Get all the other backgrounds if we're on the index page.
    // if (window.location.pathname === "/") init_backgrounds();

    // Make sure the size of backgrounds is kept upon resize.
    $(window).resize(function() {
        $('.dd_bg_cont').css('background-size', 'cover');
    });
});