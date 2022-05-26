$(function () {
    $('tbody').find('tr').click(function(){
        $(this).toggleClass('table-success')
    })
    $(document).keydown(function (event) {
        handleKeydown(event);
    });
    $('#keep').click(handleKeep);
    $('#remove').click(handleRemoveAll);
    $('#skip').click(handleSkip);
});

function handleKeydown(event) {
    // Regular numbers
    if (event.which >= 48 & event.which <= 57){
        console.log('x');
        selectByNumber(event.which - 48);
    // Numpad
    } else if (event.which >= 96 & event.which <= 105) {
        selectByNumber(event.which - 96);
    // k
    } else if (event.which == '13') {
        handleKeep();
    // r
    } else if (event.which == '82') {
        handleRemoveAll();
    // s
    } else if (event.which == '83') {
        handleSkip();
    }
}

function selectByNumber(number) {
    console.log(number.toString())
    $(".row_heading").filter(function () {
        return $(this).text() == number.toString();
    }).parent('tr').toggleClass('table-success');
}

function handleKeep(){
    // If no rows are selected, do nothing
    if (!($('tbody').find('tr.table-success')).length){
        return;
    }
    // Find out which rows to keep
    rowsToRemove = [];
    $('tbody').find('tr').not('.table-success').each(function(){
        rowsToRemove.push($(this).find('.col0').text());
    });
    // Send post request
    console.log(rowsToRemove);
    $.post("/source_dup_action", JSON.stringify(rowsToRemove))
        .done(function () {
            location.reload(true)
        });
}

function handleSkip() {
    $.post("/source_dup_action", JSON.stringify([]))
        .done(function () {
            location.reload(true)
        });
}

function handleRemoveAll() {
    rowsToRemove = [];
    $('tbody').find('tr').each(function () {
        rowsToRemove.push($(this).find('.col0').text());
    });
    console.log(rowsToRemove);
    $.post("/source_dup_action", JSON.stringify(rowsToRemove))
        .done(function () {
            location.reload(true)
        });
}