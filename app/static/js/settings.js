$(function () {
    $('input').on('input', function (e) {
        $('#submit').removeClass('disabled');
        $('#undo').removeClass('disabled');
    });
})

function handleKeydown(e) {
    keyPressed = e.key.toLowerCase();
    $focusedElement = $(e.target)
    let focusedTag = $focusedElement.prop("tagName");
    if (focusedTag == 'BODY'){
        if (keyPressed == 'u'){
            $('#undo').click()
        } else if (keyPressed == 'r') {
            $('restore').click()
        } else if (keyPressed == 'enter') {
            $('submit').click()
        }   
    } else{
        if (keyPressed == 'escape'){
            $(e.target).blur();
        }
    }
}