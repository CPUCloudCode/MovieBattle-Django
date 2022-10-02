
$('.movie-select').each(function(){
    $(this).click(function() {
        var link = '[value=' + $(this).attr('link') + ']'
        $('#categorySelect option')
            .removeAttr('selected')
            .filter(link)
                .attr('selected', true)
    })
})
var cards = $('#presented')
var marketplace = $('#marketplace')
var ownsets = $('#ownsets')
$('#btnradio1').click(function() {
    $(cards).show()
    $(marketplace).hide()
    $(ownsets).hide()
    $(this).toggleClass('btn-light');
    $(this).toggleClass('btn-outline-light');
    $('#btnradio2').removeClass('btn-light');
    $('#btnradio2').addClass('btn-outline-light');
    $('#btnradio3').removeClass('btn-light');
    $('#btnradio3').addClass('btn-outline-light');
})
$('#btnradio2').click(function() {
    $(cards).hide()
    $(ownsets).hide()
    $(marketplace).show()
    $(this).toggleClass('btn-light');
    $(this).toggleClass('btn-outline-light');
    $('#btnradio1').removeClass('btn-light');
    $('#btnradio1').addClass('btn-outline-light');
    $('#btnradio3').removeClass('btn-light');
    $('#btnradio3').addClass('btn-outline-light');
})
$('#btnradio3').click(function() {
    $(cards).hide()
    $(ownsets).show()
    $(marketplace).hide()
    $(this).toggleClass('btn-light');
    $(this).toggleClass('btn-outline-light');
    $('#btnradio2').removeClass('btn-light');
    $('#btnradio2').addClass('btn-outline-light');
    $('#btnradio1').removeClass('btn-light');
    $('#btnradio1').addClass('btn-outline-light');
})

$('#marketplaceForm').submit(function (e) {
    e.preventDefault();
    if (!$.trim( $('#marketplace').html()).length ){
        $.ajax({
            type: 'GET',
            url: "marketplace",
            data: {},
            success: function (response) {
                // if not valid user, alert the user
                const obj = response["test"]
                console.log("Test: " + obj)
                $('#marketplace').empty()
                obj.forEach((item) => {
                    console.log("Item: " + item)
                    console.log("ID: " + item.id)
                    console.log("poster: " + item.poster)
                    $('#marketplace').append('<div class="col-md-3 col-sm-12 movie-select d-flex align-items-center flex-column mt-4 mb-4" link="all"> <a style="text-decoration: none;" href="'+ "host/" + item.id + "/" +'" alt="square card"><div class="card bg-dark text-white set-card" style="width: 16.5rem;"><img src="' + item.poster + '" class="card-img-top" alt="..."><div class="card-body overflow-hidden" style="max-height: 10rem;min-height: 10rem"><h3 class="card-title">' + item.title + '</h3> <p class="card-text">' + item.description + '</p> </div></div></a></div>')
                })
                

            },
            error: function (response) {
                console.log(response)
            }
        })
    }
})

$('#ownsetsForm').submit(function (e) {
    e.preventDefault();
    if (!$.trim( $('#ownsets').html()).length ){
        $.ajax({
            type: 'GET',
            url: "ownsets",
            data: {},
            success: function (response) {
                // if not valid user, alert the user
                const obj = response["test"]
                console.log("Test: " + obj)
                $('#ownsets').empty()
                obj.forEach((item) => {
                    console.log("Item: " + item)
                    console.log("ID: " + item.id)
                    console.log("poster: " + item.poster)
                    $('#ownsets').append('<div class="col-md-3 col-sm-12 movie-select d-flex align-items-center flex-column mt-4 mb-4" link="all"> <a style="text-decoration: none;" href="'+ "host/" + item.id + "/" +'" alt="square card"><div class="card bg-dark text-white set-card" style="width: 16.5rem;"><img src="' + item.poster + '" class="card-img-top" alt="..."><div class="card-body overflow-hidden" style="max-height: 10rem;min-height: 10rem"><h3 class="card-title">' + item.title + '</h3> <p class="card-text">' + item.description + '</p> </div></div></a></div>')
                })
                

            },
            error: function (response) {
                console.log(response)
            }
        })
    }
})


/*<div class="card-header card-all">
    <div class="card-header_overlay">
        <span class="pill pill-green">All</span>
    </div>
    </div>
    <div class="card-title">
        <h4>Play with every movie available</h4>			
    </div>*/
