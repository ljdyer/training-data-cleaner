// handleKeyDown used by shortcuts.js
// eslint-disable-next-line no-unused-vars
function handleKeydown(e) {
    const keyPressed = e.key.toLowerCase();
    const $focusedElement = $(e.target);
    const focusedTag = $focusedElement.prop('tagName');
    console.log(keyPressed);
    console.log(focusedTag)
    if (focusedTag === 'BODY') {
        if (keyPressed === 'u') {
            console.log($('#undo'));
            $('#undo').trigger('click');
        } else if (keyPressed === 'r') {
            $('#restore').click();
        } else if (keyPressed === 'enter') {
            $('#submit').click();
        }
    } else if (keyPressed === 'escape') {
        $(e.target).blur();
    }
}

$(() => {
    $('input').on('input', () => {
        $('#submit').removeClass('disabled');
        $('#undo').removeClass('disabled');
    });
});
