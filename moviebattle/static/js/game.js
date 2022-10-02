
    /*
        On submiting the form, send the POST ajax
        request to server and after successfull submission
        display the object.
    */

    const copyMailId = document.querySelectorAll('.mail-text');

    copyMailId.forEach(copyText => {
        copyText.addEventListener('click', () => {
            const selection = window.getSelection();
            const range = document.createRange();
            range.selectNodeContents(copyText);
            selection.removeAllRanges();
            selection.addRange(range);
    
            try {
                document.execCommand('copy');
                selection.removeAllRanges();
    
                const mailId = copyText.textContent;
                copyText.textContent = 'Copied!';
                copyText.classList.add('success');
    
                setTimeout(() => {
                    copyText.textContent = mailId;
                    copyText.classList.remove('success');
                }, 1000);
            } catch (e) {
                copyText.textContent = 'Couldn\'t copy, hit Ctrl+C!';
                copyText.classList.add('error');
    
                setTimeout(() => {
                    errorMsg.classList.remove('show');
                }, 1200);
            }
        });
    });  

    $( document ).ready(function() {
        $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#movie1Title').text() + "&callback=?", function(json) {
                
            if(!$("#movie1Img").attr("src")) {
                if (json != "Nothing found." && json.total_results>0){                 
                        
                        $("#movie1Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                        
                        //$('#poster').html('<p>Your search found: <strong>' + json.results[0].title + '</strong></p><img src=\"http://image.tmdb.org/t/p/w500/' + json.results[0].poster_path + '\" class=\"img-responsive\" >');
                } else {
                    $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=undefined&callback=?", function(json) {
                        $("#movie1Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                    });
                }
            }
        });
        $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#movie2Title').text() + "&callback=?", function(json) {
            if(!$("#movie2Img").attr("src")) {
                if (json != "Nothing found." && json.total_results>0){                 
                        console.log(json);
                        
                        $("#movie2Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                        //$('#poster').html('<p>Your search found: <strong>' + json.results[0].title + '</strong></p><img src=\"http://image.tmdb.org/t/p/w500/' + json.results[0].poster_path + '\" class=\"img-responsive\" >');
                } else {
                    $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=undefined&callback=?", function(json) {
                        $("#movie2Img").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                    });
                }
            }
        });
        let mode = $('#voteMode').text()
        //alert("Vote: " + mode)
        if(mode == 'True') {
            var intervalId = window.setInterval(function(){
                /// call your function here
                console.log("5Sek controller")
                check()
            }, 5000);
        }
    });

    $("#movie1Vote").submit(function (e) {
        // preventing from page reload and default actions
        e.preventDefault();
        $('#btnVote1').toggleClass("disabled")
        datas = {
            "id": $('#gameId').text(),
            "winner_title": $('#movie1Title').text(),
            "loser_title": $('#movie2Title').text(),
            csrfmiddlewaretoken: $('#token').text(), 
        }
        
        // serialize the data for sending the form data.
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: "post",
            data: datas,
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                id = response.id
                movie1 = response.c1
                movie2 = response.c2
                href1 = response.href1
                href2 = response.href2
                round = response.round
                rounds = response.rounds
                $('#movie1Title').text(movie1)
                $('#movie2Title').text(movie2)
                $('#rounds').text(round + "/" + rounds)
                console.log(response)
                $('#btnVote1').toggleClass("disabled")
                $('#btnVote1').blur()
                $('#btnVote2').blur()
                $("#vote1").text("0 Votes")
                $("#vote2").text("0 Votes")
                $('#vote1').removeClass('bg-primary')
                $('#vote2').removeClass('bg-primary')
                $('#vote1').removeClass('bg-success')
                $('#vote2').removeClass('bg-success')
                $('#vote1').removeClass('bg-danger')
                $('#vote2').removeClass('bg-danger')
                $('#vote1').addClass('bg-primary')
                $('#vote2').addClass('bg-primary')
                $("#movie1Img").attr("src", href1)
                $("#movie2Img").attr("src", href2)

                if(rounds==1) {
                    $("#movie1Vote").hide()
                    $("#movie1VoteHidden").show()
                    $("#movie2Vote").hide()
                    $("#movie2VoteHidden").show()
                    $("#movie1WinnerInput").val(movie1)
                    $("#movie2WinnerInput").val(movie2)
                    $("#movie1LoserInput").val(movie2)
                    $("#movie2LoserInput").val(movie1)
                }
                if(!href1) {
                    $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + movie1 + "&callback=?", function(json) {
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
                    $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + movie2 + "&callback=?", function(json) {
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
            "loser_title": $('#movie1Title').text(),
            csrfmiddlewaretoken: $('#token').text(), 
        }
        $('#btnVote2').toggleClass("disabled")
        // serialize the data for sending the form data.
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: "post",
            data: datas,
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                id = response.id
                movie1 = response.c1
                movie2 = response.c2
                href1 = response.href1
                href2 = response.href2
                round = response.round
                rounds = response.rounds
                $('#movie1Title').text(movie1)
                $('#movie2Title').text(movie2)
                $('#rounds').text(round + "/" + rounds)
                console.log(response)

                $('#btnVote2').blur()
                $('#btnVote1').blur()
                $('#btnVote2').toggleClass("disabled")
                $("#vote1").text("0 Votes")
                $("#vote2").text("0 Votes")
                $('#vote1').removeClass('bg-primary')
                $('#vote2').removeClass('bg-primary')
                $('#vote1').removeClass('bg-success')
                $('#vote2').removeClass('bg-success')
                $('#vote1').removeClass('bg-danger')
                $('#vote2').removeClass('bg-danger')
                $('#vote1').addClass('bg-primary')
                $('#vote2').addClass('bg-primary')
                $("#movie1Img").attr("src", href1)
                $("#movie2Img").attr("src", href2)

                if(rounds==1) {
                    $("#movie1Vote").hide()
                    $("#movie1VoteHidden").show()
                    $("#movie2Vote").hide()
                    $("#movie2VoteHidden").show()
                    $("#movie1WinnerInput").val(movie1)
                    $("#movie2WinnerInput").val(movie2)
                    $("#movie1LoserInput").val(movie2)
                    $("#movie2LoserInput").val(movie1)
                }

                if(!href1) {
                    $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + movie1 + "&callback=?", function(json) {
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
                    $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + movie2 + "&callback=?", function(json) {
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

            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        });
    });

    $("#check").click(function (e) {
       check()
    });

    function check() {
         // preventing from page reload and default actions
         datas = {
            "id": $('#gameId').text(),
            "title1": $('#movie1Title').text(),
            "title2": $('#movie2Title').text(),
            csrfmiddlewaretoken: $('#token').text(), 
        }
        
        // serialize the data for sending the form data.
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: "check",
            data: datas,
            success: function (response) {
                // on successfull creating object
                // 1. clear the form.
                if(response.vote1 >= 100) {
                    $("#vote1").text(response.vote1)
                } else {
                    $("#vote1").text(response.vote1 + " Votes")
                }    
                if(response.vote2 >= 100) {
                    $("#vote2").text(response.vote2)
                } else {
                    $("#vote2").text(response.vote2 + " Votes")
                }  

                $('#vote1').removeClass('bg-primary')
                $('#vote2').removeClass('bg-primary')
                $('#vote1').removeClass('bg-success')
                $('#vote2').removeClass('bg-success')
                $('#vote1').removeClass('bg-danger')
                $('#vote2').removeClass('bg-danger')

                if(response.vote1 == response.vote2) {
                    $('#vote1').addClass('bg-primary')
                    $('#vote2').addClass('bg-primary')
                } else if(response.vote1 > response.vote2) {
                    $('#vote1').addClass('bg-success')
                    $('#vote2').addClass('bg-danger')
                } else if(response.vote2 > response.vote1) {
                    $('#vote2').addClass('bg-success')
                    $('#vote1').addClass('bg-danger')
                }

            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        });
    }
    