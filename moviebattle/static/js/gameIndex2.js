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

$("#sendForm").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    if(!$('#url').val()) {
        $("#check").click()
        return;
    }
    datas = {
        "id": $('#gameId').text(),
        "title": $('#movie').val(),
        "href": $('#url').val(),
        csrfmiddlewaretoken: $('#token').text(), 
    }
    
    // serialize the data for sending the form data.
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: datas,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            if(response.sended == 'true') {
                myAlertSuccess()
            } else if(response.sended =='false') {
                myAlertFailure()
            }
            $('#url').val("")
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
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
                                $('#movie').val($(this).attr("title"))
                                $("html, body").scrollTop(0);
                            }))))
                        }     
                    }
            } else {
                $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=undefined&callback=?", function(json) {
                    $("#previewImg").show()
                    $("#previewImg").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                });
            }
        });
});

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
