$(function () {
    console.log('y')
    // Assign click events for action buttons
    $('[data-action]').click(function(){
        url = editUrl;
        data = { 'issue_id': issueId, 'action': $(this).attr('data-action') };
        $.get(url, data).done(function () {
            location.reload(true)
        });
    })
        // $('*[data-action]').click(function(){
        //     console.log('fire');
        //     $.get(editUrl, {'issue_id': issueId, 'action': $(this).attr('data-action')});
        // })
});