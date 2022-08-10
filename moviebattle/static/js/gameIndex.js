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

$('#carousel-select-1').click(function () {
    $('#url').val($('#carousel-img-1').attr("src"))
    $("#previewImg").attr("src", $('#carousel-img-1').attr("src"));

});
$('#carousel-select-2').click(function () {
    $('#url').val($('#carousel-img-2').attr("src")) 
    $("#previewImg").attr("src", $('#carousel-img-2').attr("src"));
});
$('#carousel-select-3').click(function () {
    $('#url').val($('#carousel-img-3').attr("src")) 
    $("#previewImg").attr("src", $('#carousel-img-3').attr("src"));
})

$("#check").click(function () {
    $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=d9575db1bee61ed336421f02ae0aea37&query=" + $('#movie').val() + "&callback=?", function(json) {
            if (json != "Nothing found." && json.total_results>0){                 
                    console.log(json);
                    $("#previewImg").show()
                    $('#carouselDark').show()
                    $("#previewImg").attr("src","http://image.tmdb.org/t/p/w500/" + json.results[0].poster_path);
                    
                    let max = 3;
                    if(json.total_results<3) {
                        max = json.total_results;
                    }
                    for (let i = 0; i<max; i++) {
                        let imgPath = '#carousel-img-' + (i+1);
                        let titlePath = '#carousel-title-' + (i+1);
                        $(imgPath).attr("src","http://image.tmdb.org/t/p/w500/" + json.results[i].poster_path);
                        $(titlePath).text(json.results[i].original_title);
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
