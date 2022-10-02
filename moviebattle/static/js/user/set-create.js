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



$('x').click(function () {
    alert("Lol")
    $('#url').val($(this).attr("src"))
    $("#previewImg").attr("src", $(this).attr("src"));

});

$("#toggle").click(function () {
    var pattern = $("#toggle").attr("pattern")
    if(pattern == "movie") {
        $("#toggle").attr("pattern", "tv")
        $("#movieStrong").removeClass("strong-active")
        $("#movieStrong").addClass("strong-inactive")
        $("#series").removeClass("strong-inactive")
        $("#series").addClass("strong-active")
    } else {
        $("#toggle").attr("pattern", "movie")
        $("#movieStrong").removeClass("strong-inactive")
        $("#movieStrong").addClass("strong-active")
        $("#series").removeClass("strong-active")
        $("#series").addClass("strong-inactive")
    }
    
})
$("#reset").click(function () {
    $('#movie').val("")
    $('#url').val("")
})

$('#btnReload').click(function() {
    let posterURL = $('#setPoster').val()
    if(posterURL!="") {
        $("#bannerPreview").attr("src",posterURL);
    }
})

$('#createSet').click(function() {
    
    title = $('#setTitle').val()
    desc = $('#setDesc').val()
    poster = $('#setPoster').val()

    if(title == "" || desc == "" || poster == "") {
        alert("Bitte gebe Daten ein!")
        return;
    }

    titles = []
    posters = []
    $('#listRow').children('div').children('div').children('img').each(function () {
        titles.push($(this).attr('id'))
        posters.push($(this).attr('src'))
    });

    datas = {
        "title": title,
        "desc": desc,
        "poster": poster,
        titles: titles,
        posters: posters,
        csrfmiddlewaretoken: $('#token').text(), 
    }
    
    // serialize the data for sending the form data.
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: $(this).attr('url'),
        data: datas,
        traditional: true,
        dataType: 'html',
        success: function (response) {
            window.location = "/user/";
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    });
})

$('#addBtn').click(function (){
    if($('#url').val() != "" && $('#movie').val() != "") {
        let imgPath = $('#url').val()
        let titlePath = $('#movie').val()
        let classes = "img-responsive set-image"
        $('#listRow').append($('<div class="row-item col-4 mt-3"></div>').append($('<div class="mb-3 relative"></div>').append($('<img>', {src: imgPath, class: classes, id: titlePath}).click(function () {
            $(this).parents('.row-item').remove()
        })).append('<span class="position-absolute top-0 start-50 translate-middle badge rounded-pill bg-danger bg-set">Delete</span>').append('<span class="visually-hidden">unread messages</span>')))
        $("html, body").scrollTop(0);
    }
})

$("#check").click(function () {
    var pattern = $("#toggle").attr("pattern")
    console.log("Pattern: " + pattern)
    $.getJSON("https://api.themoviedb.org/3/search/" + pattern + "?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#movie').val() + "&callback=?", function(json) {
            if (json != "Nothing found." && json.total_results>0){                 
                    console.log(json);
                    $("#previewImg").show()
                    $('#carouselDark').show()
                    var posterPath = json.results[0].poster_path
                    if(!posterPath) {
                        posterPath = json.results[1].poster_path
                    }
                    $("#previewImg").attr("src","http://image.tmdb.org/t/p/w500/" + posterPath);
                    $('#url').val("http://image.tmdb.org/t/p/w500/" + posterPath)
                    
                    let max = 12;
                    if(json.total_results<12) {
                        max = json.total_results;
                    }
                    $('#results').empty()
                    for (let i = 0; i<max; i++) {
                        if(json.results[i].poster_path != null) {
                            let imgPath = "http://image.tmdb.org/t/p/w500/" + json.results[i].poster_path;
                            let titlePath = ""
                            if(json.results[i].original_title) {
                                titlePath = json.results[i].original_title;
                            } else {
                                titlePath = json.results[i].name;
                            }
                            let classes = "img-fluid job-image"
                            $('#results').append($('<div class="col-3 mt-3"></div>').append($('<div class="mb-3 job-card"></div>').append($('<img>', {src: imgPath, class: classes, title: titlePath}).click(function () {
                                $('#url').val($(this).attr("src"))
                                $("#previewImg").attr("src", $(this).attr("src"));
                                $('#movie').val($(this).attr("title"));
                                scrollTo('#menuRow')
                            }))))
                        }     
                    }
                    scrollTo('#results')
            } else {
                $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=undefined&callback=?", function(json) {
                    $("#previewImg").show()
                    $("#previewImg").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                });
            }
        });
});

/*     UPLOAD FILE    */
/*$('#formFileAvatar').change(function(e){
    const reader = new FileReader();
    var image = $(this).val()
    if(image.includes('.jpeg') || image.includes('.jpg') || image.includes('.png') || image.includes('.gif')
    || image.includes('.JPEG') || image.includes('.JPG') || image.includes('.PNG') || image.includes('.GIF')) {
        if(image.includes('.gif')) {
            //var rank = $('#rank')
            if('default'=='default') {
                $("html, body").scrollTop(0);
                window.allowAvatar = false
                return;
            }
        }
        reader.addEventListener("load", () => {
            image = reader.result;
            $('#bannerPreview').attr('src', image)
        });
        avatar = this.files[0]
        reader.readAsDataURL(this.files[0]);
        window.allowAvatar = true
        return;
    } else {
        $("html, body").scrollTop(0);
        window.allowAvatar = false
    }
    
})*/


function myAlertSuccess(){
    $(".alert-success").fadeIn();
    setTimeout(function(){
      $(".alert-success").fadeOut(); 
    }, 4000);
  }
function myAlertFailure(){
    $(".alert-danger").fadeIn();
    setTimeout(function(){
        $(".alert-danger").fadeOut(); 
    }, 4000);
}
function scrollTo(id) {
    $("html, body").animate({ scrollTop: $(id).offset().top }, 200);
}

