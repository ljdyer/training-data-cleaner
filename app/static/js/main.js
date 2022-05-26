$(function () {
    addCellClasses();
}); 

function addCellClasses(){
    for (const [currentSelector, classesToAdd] of Object.entries(selectorsAndClasses)) {
        console.log(currentSelector, classesToAdd)
        $('.table').find(currentSelector).each(function () {
            console.log('adding')
            $(this).addClass(classesToAdd);
        });
    }
}