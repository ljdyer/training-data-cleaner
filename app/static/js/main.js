function addCellClasses() {
    // selectorsAndClasses defined in Jinja template
    // eslint-disable-next-line no-undef
    for (const [currentSelector, classesToAdd] of Object.entries(selectorsAndClasses)) {
        $('.table').find(currentSelector).each(() => {
            $(this).addClass(classesToAdd);
        });
    }
}

$(() => {
    addCellClasses();
});
