$(function () {
    $(document).keydown(function (event) {
        handleKeydown(event);
    });
});

function handleKeydown(e) {
    keyPressed = e.key.toLowerCase();
    if (e.ctrlKey){
        keyPressed = 'ctrl_' + keyPressed;
    }
    $('[data-shortcut]').each(function() {
        if (keyPressed == $(this).attr('data-shortcut')){
            e.preventDefault();
            $(this)[0].click();
        }
    })
}

// function selectByNumber(number) {
//     console.log(number.toString())
//     link = $(".number").filter(function () {
//         return $(this).text() == number.toString();
//     }).parent('tr').find('a')
//     link[0].click();
// }