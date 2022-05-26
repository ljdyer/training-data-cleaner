$(function () {
    $(document).keydown(function (event) {
        handleKeydown(event);
    });
});

function handleKeydown(event) {
    // Regular numbers
    if (event.which >= 48 & event.which <= 57){
        selectByNumber(event.which - 48);
    // Numpad
    } else if (event.which >= 96 & event.which <= 105) {
        selectByNumber(event.which - 96);
    }
}

function selectByNumber(number) {
    console.log(number.toString())
    link = $(".number").filter(function () {
        return $(this).text() == number.toString();
    }).parent('tr').find('a')
    link[0].click();
}