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