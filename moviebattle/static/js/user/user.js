$(document).ready(function(){
    const myArray = $("#user-description").text().split("\n")
    jQuery.each( myArray, function( i, val ) {
        if(val) {
            if(val.startsWith("<")) {
                $("#user-card").append(val)
            } else {
                $("#user-card").append(val)
            }
        }
      });
      $('#user-card').children().each(function () {
        $(this).addClass("mb-4") // "this" is the current element in the loop
    });
});

$('#linkSocial').click(function() {
    $(this).addClass("active")
    $('#linkProfile').removeClass('active')
    $('#profile').hide()
    $('#social').show()
    $('#sets').hide()
    $('#linkSets').removeClass('active')

    if(!$.trim( $('#socialCards').html()).length) {
        url = $('#urlsocial').val()

        datas = {
            csrfmiddlewaretoken: $('#token').val(), 
        }
        
        // serialize the data for sending the form data.
        // make POST ajax call
        
        $.ajax({
            type: 'GET',
            url: 'get/social/',
            data: datas,
            success: function (response) {
                $('#social').show()
                var socialCards = $('#socialCards')
                
                    socialCards.empty()
                    response.users.forEach ((book, index) => {
                        console.log(`i:${index} | Autor:`, book);
                        if(book['avatar'].includes('profile_image')) {
                            socialCards.append('<div class="col mt-4"><a class="socialRef" href="' + "/user/view/" + book['username'] + '"><div class="card bg-dark social-card" style="width: 18rem;"><img src="/media/' + book['avatar'] + '" class="card-img-top social-img" alt="..."><div class="card-body text-white"><h5 class="card-title">' + book['username'] +'</h5><a href="' + "/user/view/" + book['username'] + '" class="btn btn-primary mt-4">Visit</a></div></div></a></div>')
                        } else {
                            socialCards.append('<div class="col mt-4"><a class="socialRef" href="' + "/user/view/" + book['username'] + '"><div class="card bg-dark social-card" style="width: 18rem;"><img src="' + book['avatar'] + '" class="card-img-top social-img" alt="..."><div class="card-body text-white"><h5 class="card-title">' + book['username'] +'</h5><a href="' + "/user/view/" + book['username'] + '" class="btn btn-primary mt-4">Visit</a></div></div></a></div>')
                        }
                    });

            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        });
    }
})

$('#linkProfile').click(function() {
    $(this).addClass("active")
    $('#linkSocial').removeClass('active')
    $('#linkSets').removeClass('active')
    $('#profile').show()
    $('#social').hide()
    $('#sets').hide()
})

$('#linkSets').click(function() {
    $(this).addClass("active")
    $('#linkSocial').removeClass('active')
    $('#linkProfile').removeClass('active')
    $('#profile').hide()
    $('#social').hide()
    $('#sets').show()
})

$('#follow').click(function() { 
 
    url = $('#urlFollow').text()
    datas = {
        username: $('#username').text(),
        csrfmiddlewaretoken: $('#token').text(), 
    }
    
    // serialize the data for sending the form data.
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: url,
        data: datas,
        success: function (response) {
            $('#followForm').hide()
            $('#unfollowForm').show()
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    });
})

$('#unfollow').click(function() { 
 
    url = $('#urlUnfollow').text()
    datas = {
        username: $('#username').text(),
        csrfmiddlewaretoken: $('#token').text(), 
    }
    
    // serialize the data for sending the form data.
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: url,
        data: datas,
        success: function (response) {
            $('#followForm').show()
            $('#unfollowForm').hide()
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    });
})