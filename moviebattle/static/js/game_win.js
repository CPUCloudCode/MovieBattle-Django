$( document ).ready(function() {
    if(!$('#winnerImg').attr("src") && !$('#winnerImg').attr("src")) {
        $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#winnerTitle').text() + "&callback=?", function(json) {
            if (json != "Nothing found."){                 
                    console.log(json);
                    $("#winnerImg").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                    //$('#poster').html('<p>Your search found: <strong>' + json.results[0].title + '</strong></p><img src=\"http://image.tmdb.org/t/p/w500/' + json.results[0].poster_path + '\" class=\"img-responsive\" >');
            } else {
                $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=15d2ea6d0dc1d476efbca3eba2b9bbfb&query=goonies&callback=?", function(json) {
                    console.log(json);
                });
            }
        });
    } 
});