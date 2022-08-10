// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );
    $(".row-cards > .col-2").each(function(){
        // Test if the div element is empty
        var movie = $(this).children('p')
        var image = $(this).children('.d-inline-flex').children("img")
        $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + movie.text() + "&callback=?", function(json) {
            if (json != "Nothing found." && json.total_results>0 && json.results[0].poster_path != null){                 
                    console.log(json);
                    console.log("Image: " + image)
                    console.log("HREF: " + "http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path)
                    image.attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                    console.log("ImageAfter: " + image.attr("src"))
                    //$('#poster').html('<p>Your search found: <strong>' + json.results[0].title + '</strong></p><img src=\"http://image.tmdb.org/t/p/w500/' + json.results[0].poster_path + '\" class=\"img-responsive\" >');
            } else {
                $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=undefined&callback=?", function(json) {
                    image.attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                });
            }
        });
    });
});