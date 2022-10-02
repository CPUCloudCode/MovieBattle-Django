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

$('#editSetForm').submit(function(e) {
    let check = $('#modalCheck').prop('checked')
    $.ajax({ // make an AJAX request
        type: "POST",
        url: $(this).attr("action"), // it's the URL of your component B
        data: $(this).serialize() + '&id=' + $('#setEditModal').attr('modalUrl')+ '&public=' + check , // serializes the form's elements
        success: function(response)
        {
          // show the data you got from B in result div
          if(response.updated) {
            myAlertSuccess()
            var setUpdated = $('#' + response.id)
            setUpdated.children('.social-img').attr("src", response.poster)
            if(response.public) {
                setUpdated.children('.card-body').children(".card-title").empty().append(response.title + ' ' + '<span class="badge bg-success">Published</span>')
            } else {
                setUpdated.children('.card-body').children(".card-title").empty().append(response.title + ' ' + '<span class="badge bg-danger">Privat</span>')

            }

            setUpdated.children('.card-body').children(".btn-edit").click(function() {
                $('#setEditModal').modal("show")
                $('#setEditModal').attr("modalUrl", response.id)
                $('#setEditModal .modal-title').text(response.title)
                $('#modalTitle').val(response.title)
                $('#modalDescription').val(response.desc)
                $('#modalBanner').val(response.poster)
                $('#goToEdit').attr('href', "set/edit/" + response.id)
                if(response.length>=8) {
                    $('#modalCheck').prop("checked", response.public)
                    $('#modalCheck').prop('disabled', false);
                    $('#modalCheckLabel').empty().append("Public")
                } else {
                    console.log("Nonono")
                    $('#modalCheck').prop('disabled', true);
                    $('#modalCheckLabel').empty().append(' <span class="badge bg-danger">Too few entries!</span>')
                }
            })

          } else {
            myAlertFailure()
          }
          // Hide Modal
          $('#setEditModal').modal("hide")
          // Update SetView
          
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
      });
      e.preventDefault(); // avoid to execute the actual submit of the form
})

$('#linkProfile').click(function() {
    $(this).addClass("active")
    $('#linkSocial').removeClass('active')
    $('#linkSets').removeClass('active')
    $('#profile').show()
    $('#social').hide()
    $('#sets').hide()
})
$('#delete').click(function() {
    data = {
        csrfmiddlewaretoken: $('#token').text(),
        id: $('#deleteId').text()
    }
    $.ajax({
        type: 'POST',
        url: $('#deleteModal').attr('url'),
        data: data,
        success: function (response) {
            $('#deleteModal').modal('hide')
            if(response.deleted) {
                myAlertDelete()
                $('#' + response.id).parents('.col-4').remove()
            } else {
                myAlertFailure()
            }

        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    });
})

$('#linkSets').click(function() {
    $(this).addClass("active")
    $('#linkSocial').removeClass('active')
    $('#linkProfile').removeClass('active')
    $('#profile').hide()
    $('#social').hide()
    $('#sets').show()
    if(!$.trim( $('#setsCards').html()).length) {
        datas = {
            csrfmiddlewaretoken: $('#token').val(), 
        }
        
        // serialize the data for sending the form data.
        // make POST ajax call
        
        $.ajax({
            type: 'GET',
            url: 'get/sets/',
            data: datas,
            success: function (response) {
                var socialCards = $('#setsCards')
                
                socialCards.empty()
                const obj = response["test"]
                console.log("Lol")
                console.log("Test: " + obj)
                obj.forEach((item) => {
                    console.log("Item: " + item)
                    console.log("ID: " + item.id)
                    console.log("poster: " + item.poster)
                    let statusSpan = (item.public) ? '<span class="badge bg-success">Published</span>' : '<span class="badge bg-danger">Privat</span>'
                    //socialCards.append('<div class="col mt-4"><a class="socialRef" href="' + "/game/host/" + item.id + '"><div class="card bg-dark social-card" style="width: 18rem;">'+'<img src="' + item.poster + '" class="card-img-top social-img" alt="..."><div class="card-body text-white"><h5 class="card-title">' + item.title +'</h5><a href="#" class="btn btn-primary mt-4 me-2">Visit</a> <button href="set/edit/' + item.id + '" class="btn btn-warning mt-4 btn-edit">Edit</button></div></div></a></div>')
                    socialCards.append($('<div class="col-4 mt-4"></div>').append($('<a class="socialRef" href="' + "/game/host/" + item.id + '"></a>')
                    .append($('<div class="card bg-dark social-card" id="'+ item.id +'"></div>')
                    .append($('<img src="' + item.poster + '" class="card-img-top social-img" alt="..."></img>'))
                    .append($('<div class="card-body text-white"></div>')
                    .append($('<h5 class="card-title">' + item.title + ' ' + statusSpan + '</h5>'))
                    .append($('<a href=#" class="btn btn-warning mt-4 me-4 btn-edit">Edit</a>')
                    .click(function() {
                        $('#setEditModal').modal("show")
                        $('#setEditModal').attr("modalUrl", item.id)
                        $('#setEditModal .modal-title').text(item.title)
                        $('#modalTitle').val(item.title)
                        $('#modalDescription').val(item.description)
                        $('#modalBanner').val(item.poster)
                        $('#goToEdit').attr('href', "set/edit/" + item.id)
                        if(item.length>=8) {
                            $('#modalCheck').prop("checked", item.public)
                            $('#modalCheck').prop('disabled', false);
                            $('#modalCheckLabel').empty().append("Public")
                        } else {
                            console.log("Nonono")
                            $('#modalCheck').prop('disabled', true);
                            $('#modalCheckLabel').empty().append(' <span class="badge bg-danger">Too few entries!</span>')
                        }
                    })
                    ).append($('<a href=#" class="btn btn-warning mt-4 btn-danger">Delete</a>')
                    .click(function() {
                        $('#deleteModal').modal("show")
                        $('#deleteTitle').text(item.text)
                        $('#deleteId').text(item.id)
                    })
                    )
                    ))))
                })

            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        });
    }
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

function myAlertSuccess(){
    $(".as").fadeIn();
    setTimeout(function(){
      $(".as").fadeOut(); 
    }, 4000);
  }
function myAlertDelete(){
    $(".ad").fadeIn();
    setTimeout(function(){
      $(".ad").fadeOut(); 
    }, 4000);
  }
function myAlertFailure(){
    $(".alert-danger").fadeIn();
    setTimeout(function(){
        $(".alert-danger").fadeOut(); 
    }, 4000);
}