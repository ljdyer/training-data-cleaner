function handleAction($e) {
    const action = $e.attr('data-action');
    switch (action) {
        case 'select_all':
            $('tr').removeClass('table-success').addClass('table-danger');
            return;
        case 'deselect_all':
            $('tr').removeClass('table-danger').addClass('table-success');
            return;
        default:
            break;
    }
    // editUrl defined in Jinja template
    // eslint-disable-next-line no-undef
    const url = editUrl;
    const data = { action };
    switch (action) {
        case ('remove_all', 'skip'):
            $.post(url, data).done(() => { window.location.reload(true); });
            break;
        default:
            break;
    }
}

$(() => {
    // Assign click events for action buttons
    $('[data-action]').click(() => handleAction($(this)));
});
