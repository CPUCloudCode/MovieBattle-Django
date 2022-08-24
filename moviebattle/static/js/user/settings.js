var avatar;
window.allowAvatar = true
window.allowBanner = true
$('#formFileAvatar').change(function(e){
    const reader = new FileReader();
    var image = $(this).val()
    if(image.includes('.jpeg') || image.includes('.jpg') || image.includes('.png') || image.includes('.gif')
    || image.includes('.JPEG') || image.includes('.JPG') || image.includes('.PNG') || image.includes('.GIF')) {
        if(image.includes('.gif')) {
            var rank = $('#rank')
            if('default'=='default') {
                myAlertPermissionFailure()
                $("html, body").scrollTop(0);
                window.allowAvatar = false
                return;
            }
        }
        reader.addEventListener("load", () => {
            const uploaded_image = reader.result;
            image = reader.result;
            $('#avatarPreview').attr('src', image)
        });
        avatar = this.files[0]
        reader.readAsDataURL(this.files[0]);
        window.allowAvatar = true
        return;
    } else {
        myAlertFailure()
        $("html, body").scrollTop(0);
        window.allowAvatar = false
    }
    
})

$('#formFileBanner').change(function(){
    const reader = new FileReader();
    var image = $(this).val()
    if(image.includes('.jpeg') || image.includes('.jpg') || image.includes('.png') || image.includes('.gif')
    || image.includes('.JPEG') || image.includes('.JPG') || image.includes('.PNG') || image.includes('.GIF')) {
        if(image.includes('.gif')) {
            var rank = $('#rank')
            if(rank=='default') {
                myAlertPermissionFailure()
                $("html, body").scrollTop(0);
                window.allowBanner = false
                return;
            }
        }
        reader.addEventListener("load", () => {
            const uploaded_image = reader.result;
            image = reader.result;
            $('#bannerPreview').attr('src', image)
        });
        reader.readAsDataURL(this.files[0]);
        window.allowBanner = true
        return;
    } else {
        myAlertFailure()
        $("html, body").scrollTop(0);
        window.allowAvatar = false
    }
})

$("#linkFavourite").click(function() {
    $('#updateForm').hide()
    $("#favourites").show()
})

$("#linkProfile").click(function() {
    $('#updateForm').show()
    $("#favourites").hide()
})

$("#updateForm").submit(function (e) {
    // preventing from page reload and default actions
    if(window.allowAvatar && window.allowBanner) {
        
    } else {
        myAlertFailure()
        $("html, body").scrollTop(0);
        e.preventDefault();
    }
});

$("#favouriteSeriesBtn").click(function () {
    $.getJSON("https://api.themoviedb.org/3/search/tv?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#favouriteSeries').val() + "&callback=?", function(json) {
            if (json != "Nothing found." && json.total_results>0){                 

                    var posterPath = json.results[0].poster_path
                    if(!posterPath) {
                        posterPath = json.results[1].poster_path
                    }
                    
                    let max = 9;
                    if(json.total_results<9) {
                        max = json.total_results;
                    }
                    $('#previewSeries').empty()
                    $('#previewSeries').append('<h4>Preview Favourite</h4>')
                    for (let i = 0; i<max; i++) {
                        if(json.results[i].poster_path != null) {
                            let imgPath = "http://image.tmdb.org/t/p/w500/" + json.results[i].poster_path;
                            $('#previewSeries').append($('<img class="favourite-small-image" src="' + imgPath + '" alt=""></img>').click(function() {
                                $('#favouriteSeriesImg').attr('src', $(this).attr('src'))
                            }))
                        }     
                    }
            } else {
                $('#previewSeries').empty()
                $('#previewSeries').append('<h4>Preview Favourite</h4>')
            }
        });
});

$("#favouriteMovieBtn").click(function () {
    $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#favouriteMovie').val() + "&callback=?", function(json) {
            if (json != "Nothing found." && json.total_results>0){                 

                    var posterPath = json.results[0].poster_path
                    if(!posterPath) {
                        posterPath = json.results[1].poster_path
                    }
                    
                    let max = 9;
                    if(json.total_results<9) {
                        max = json.total_results;
                    }
                    $('#previewMovie').empty()
                    $('#previewMovie').append('<h4>Preview Favourite</h4>')
                    for (let i = 0; i<max; i++) {
                        if(json.results[i].poster_path != null) {
                            let imgPath = "http://image.tmdb.org/t/p/w500/" + json.results[i].poster_path;
                            $('#previewMovie').append($('<img class="favourite-small-movie-image" src="' + imgPath + '" alt=""></img>').click(function() {
                                $('#favouriteMovieImg').attr('src', $(this).attr('src'))
                            }))
                        }     
                    }
            } else {
                $('#previewMovie').empty()
                $('#previewMovie').append('<h4>Preview Favourite</h4>')
            }
        });
});

$("#updateFavourite").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();

    datas = {
        "movie": $('#favouriteMovieImg').attr('src'),
        "series": $('#favouriteSeriesImg').attr('src'),
        csrfmiddlewaretoken: $('#token').text(), 
    }
    $.ajax({
        type: 'POST',
        url: "updatefavourite/",
        data: datas,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form. 
            $('#previewMovie').empty()
            $('#previewSeries').empty()
            myAlertSuccess()
            $("html, body").scrollTop(0);
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    });
});

function myAlertSuccess(){
    $(".alert-success").fadeIn();
    setTimeout(function(){
      $(".alert-success").fadeOut(); 
    }, 3000);
  }
function myAlertFailure(){
    $(".alert-danger").fadeIn();
    setTimeout(function(){
        $(".alert-danger").fadeOut(); 
    }, 3000);
}

function myAlertPermissionFailure(){
    $(".alert-warning").fadeIn();
    setTimeout(function(){
        $(".alert-warning").fadeOut(); 
    }, 3000);
}
