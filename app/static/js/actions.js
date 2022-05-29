$(function () {
    console.log('y')
    // Assign click events for action buttons
    $('[data-action]').click(function(){
        handleAction($(this));
    })
        // $('*[data-action]').click(function(){
        //     console.log('fire');
        //     $.get(editUrl, {'issue_id': issueId, 'action': $(this).attr('data-action')});
        // })
});

function handleAction($e){
    action = $e.attr('data-action')
    switch (action){
        case 'select_all':
            $('tr').removeClass('table-success').addClass('table-danger')
            break;
        case 'deselect_all':
            $('tr').removeClass('table-danger').addClass('table-success')
            break;
        case 'remove_all':
            url = editUrl;
            data = { 'issue_id': issueId, 'action': action };
            $.post(url, data).done(function () {
                location.reload(true)
            });
            break;       
    }
}