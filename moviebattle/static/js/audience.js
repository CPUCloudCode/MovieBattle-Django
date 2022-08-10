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

previous = $( ".form-select" ).val()

$( ".form-select" ).focus(function() {
    previous = $( this ).val()
  });

$( ".form-select" ).change(function() {
    datas = {
        "id": $('#gameId').text(),
        "rounds": $( this ).val(),
        csrfmiddlewaretoken: $('#token').text(), 
    }
    // serialize the data for sending the form data.
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: "changeAudience",
        data: datas,
        success: function (response) {
        // on successfull creating object           
            if(response.change == 'true') {
                $('#count').text(parseInt($( ".form-select" ).val())*2)
                $('#start').toggleClass('disabled')
            } else {
                $(".form-select").val(previous)
                return;
            }

        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    });
  });

  $( "#reload" ).click(function() {
    datas = {
        "id": $('#gameId').text(),
        csrfmiddlewaretoken: $('#token').text(), 
    }
    // serialize the data for sending the form data.
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: "reload",
        data: datas,
        success: function (response) {
        // on successfull creating object           
            $('#counter').text(response.counts)
            if(response.counts==response.rounds) {
                $('#start').toggleClass('disabled')
            }
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    });
  });

  $( "#audienceVote" ).click(function() {
    if($(this).val() == "on") {
        $(this).val("off")
    } else {
        $(this).val("on")
    }
  });