
$('.movie-select').each(function(){
    $(this).click(function() {
        var link = '[value=' + $(this).attr('link') + ']'
        $('#categorySelect option')
            .removeAttr('selected')
            .filter(link)
                .attr('selected', true)
    })
})
