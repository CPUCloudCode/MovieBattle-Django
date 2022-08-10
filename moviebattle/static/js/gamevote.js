
    /*
        On submiting the form, send the POST ajax
        request to server and after successfull submission
        display the object.
    */
        $( document ).ready(function() {
            if(!$("#movie1Img").attr("src")) {
                $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#movie1Title').text() + "&callback=?", function(json) {
                    if (json != "Nothing found." && json.total_results>0){                 
                            console.log(json);
                            $("#movie1Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                            //$('#poster').html('<p>Your search found: <strong>' + json.results[0].title + '</strong></p><img src=\"http://image.tmdb.org/t/p/w500/' + json.results[0].poster_path + '\" class=\"img-responsive\" >');
                    } else {
                        $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=undefined&callback=?", function(json) {
                            $("#movie1Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                        });
                    }
                });
            }
            if(!$("#movie2Img").attr("src")) {
                $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#movie2Title').text() + "&callback=?", function(json) {
                    if (json != "Nothing found." && json.total_results>0){                 
                            console.log(json);
                            $("#movie2Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                            //$('#poster').html('<p>Your search found: <strong>' + json.results[0].title + '</strong></p><img src=\"http://image.tmdb.org/t/p/w500/' + json.results[0].poster_path + '\" class=\"img-responsive\" >');
                    } else {
                        $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=undefined&callback=?", function(json) {
                            $("#movie2Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                        });
                    }
                });
            }
            var intervalId = window.setInterval(function(){
                /// call your function here
                console.log("5Sek controller")
                console.log("Bool: " + $('#spinner').is(':visible'))
                /*if($('#spinner').is(':visible')) {
                    console.log("Check iot")
                    check()
                } */
                console.log("Check iot")
                check()
            }, 5000);
        });
    
        $("#movie1Vote").submit(function (e) {
            // preventing from page reload and default actions
            e.preventDefault();
            datas = {
                "id": $('#gameId').text(),
                "winner_title": $('#movie1Title').text(),
                "title1": $('#movie1Title').text(),
                "title2": $('#movie2Title').text(),
                csrfmiddlewaretoken: $('#token').text(), 
            }
            
            // serialize the data for sending the form data.
            // make POST ajax call
            $.ajax({
                type: 'POST',
                url: $('#url').text(),
                data: datas,
                success: function (response) {
                    // on successfull creating object
                    // 1. clear the form.
                    $('#btnVote2').hide()
                    $('#btnVote1').removeClass('btn-outline-warning')
                    $('#btnVote1').addClass('btn-success')
                    $('#btnVote1').addClass('disabled')
                    $('#btnVote1').text('Voted!')
                    $('#spinner').show()
                },
                error: function (response) {
                    // alert the error if any error occured
                    alert(response["responseJSON"]["error"]);
                }
            });
        });
        $("#movie2Vote").submit(function (e) {
            // preventing from page reload and default actions
            e.preventDefault();
            datas = {
                "id": $('#gameId').text(),
                "winner_title": $('#movie2Title').text(),
                "title1": $('#movie1Title').text(),
                "title2": $('#movie2Title').text(),
                csrfmiddlewaretoken: $('#token').text(), 
            }
            
            // serialize the data for sending the form data.
            // make POST ajax call
            $.ajax({
                type: 'POST',
                url: $('#url').text(),
                data: datas,
                success: function (response) {
                    // on successfull creating object
                    // 1. clear the form.
                    $('#btnVote1').hide()
                    $('#btnVote2').removeClass('btn-outline-warning')
                    $('#btnVote2').addClass('btn-success')
                    $('#btnVote2').addClass('disabled')
                    $('#btnVote2').val('Voted!')
                    $('#spinner').show()
                },
                error: function (response) {
                    // alert the error if any error occured
                    alert(response["responseJSON"]["error"]);
                }
            });
        });

        function check() {
            // preventing from page reload and default actions
            datas = {
               "id": $('#gameId').text(),
               csrfmiddlewaretoken: $('#token').text(), 
           }
           
           // serialize the data for sending the form data.
           // make POST ajax call
           $.ajax({
               type: 'POST',
               url: $('#checkUrl').text(),
               data: datas,
               success: function (response) {
                   // on successfull creating object
                   // 1. clear the form.
                   if(response.redirect) {
                    window.location = "/";
                   }
                   if(response.canVote && ($('#movie1Title').text()!=response.title1 || $('#movie2Title').text()!=response.title2)) {
                    href1 = response.href1
                    href2 = response.href2
                    $("#movie1Img").attr("src", href1)
                    $("#movie2Img").attr("src", href2)
                    console.log("Player can vote again!")
                    $('#movie1Title').text(response.title1)
                    $('#movie2Title').text(response.title2)
                    if(!href1) {
                        $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#movie1Title').text() + "&callback=?", function(json) {
                            if (json != "Nothing found." && json.total_results>0){                 
                                    console.log(json);
                                    $("#movie1Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                                    //$('#poster').html('<p>Your search found: <strong>' + json.results[0].title + '</strong></p><img src=\"http://image.tmdb.org/t/p/w500/' + json.results[0].poster_path + '\" class=\"img-responsive\" >');
                            } else {
                                $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=undefined&callback=?", function(json) {
                                    $("#movie1Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                                });
                            }
                        });
                    }
                    if(!href2) {
                        $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#movie2Title').text() + "&callback=?", function(json) {
                            if (json != "Nothing found." && json.total_results>0){                 
                                    console.log(json);
                                    $("#movie2Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                                    //$('#poster').html('<p>Your search found: <strong>' + json.results[0].title + '</strong></p><img src=\"http://image.tmdb.org/t/p/w500/' + json.results[0].poster_path + '\" class=\"img-responsive\" >');
                            } else {
                                $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=undefined&callback=?", function(json) {
                                    $("#movie2Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                                });
                            }
                        });
                    }
                    // Vote 1
                    $('#btnVote1').show()
                    $('#btnVote1').addClass('btn-outline-warning')
                    $('#btnVote1').removeClass('btn-success')
                    $('#btnVote1').removeClass('btn-outline-danger')
                    $('#btnVote1').removeClass('disabled')
                    $('#btnVote1').text('Voted for it')

                    // Vote 2
                    $('#btnVote2').show()
                    $('#btnVote2').addClass('btn-outline-warning')
                    $('#btnVote2').removeClass('btn-success')
                    $('#btnVote2').removeClass('btn-outline-danger')
                    $('#btnVote2').removeClass('disabled')
                    $('#btnVote2').val('Vote for it')

                    $('#rounds').text(response.round + "/" + response.rounds)

                    // Spinner
                    $('#spinner').hide()

                   } 
                   

               },
               error: function (response) {
                   // alert the error if any error occured
                   alert(response["responseJSON"]["error"]);
               }
           });
       }
    
    
        