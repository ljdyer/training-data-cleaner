let textWithoutMarkers = {};

function updateNumSelected() {
    $('#num-selected').text($('tr.table-secondary').length);
}

function updateShowingInfo(showingFrom, showingTo, showingTotal) {
    if (showingTotal === 0) {
        $('#showing-from').text(0);
    } else {
        $('#showing-from').text(showingFrom + 1);
    }
    $('#showing-to').text(showingTo + 1);
    $('#showing-total').text(showingTotal);
}

function toggleRow($row) {
    if ($row.attr('data-edited')) {
        $row.toggleClass('table-success');
    }
    $row.toggleClass('table-secondary');
    updateNumSelected();
}

function makeEditable($row) {
    if (!($row.attr('data-edited'))) {
        const index = parseInt($row.find('.index').text(), 10);
        const $sourceCell = $row.find('.source');
        const $targetCell = $row.find('.target');
        // eslint-disable-next-line no-plusplus
        for (let i = 0; i < textWithoutMarkers.length; i++) {
            if (textWithoutMarkers[i].index === index) {
                $sourceCell.text(textWithoutMarkers[i].source);
                $targetCell.text(textWithoutMarkers[i].target);
            }
        }
        $sourceCell.attr('contenteditable', true);
        $targetCell.attr('contenteditable', true);
        $row.addClass('table-success');
        $row.removeClass('table-secondary');
        $row.attr('data-edited', true);
    }
}

function writeTable(dfAsJson, showingFrom) {
    const dfParsed = JSON.parse(dfAsJson);
    const tableBody = $('#data-table').find('tbody');
    // Empty table
    tableBody.empty();
    // Append new rows
    let count = showingFrom + 1;
    for (const row of dfParsed) {
        const newRow = $('<tr>');
        newRow.append($(`<th>${count}</th>`));
        newRow.append($(`<td class="index">${row.index}</td>`));
        newRow.append($(`<td class="source" contenteditable="false">${row.source}</td>`));
        newRow.append($(`<td class="target" contenteditable="false">${row.target}</td>`));
        tableBody.append(newRow);
        count += 1;
    }
    tableBody.find('th,td.index').on('click', (e) => {
        toggleRow($(e.currentTarget).parent());
    });
    tableBody.find('td.source,td.target').on('click', (e) => {
        makeEditable($(e.currentTarget).parent());
        e.currentTarget.focus();
    });
    updateNumSelected();
}

function handleResponse(response) {
    const responseParsed = JSON.parse(response);
    if ('df_len' in responseParsed) {
        const dfLen = responseParsed.df_len;
        const rowOrRows = parseInt(dfLen, 10) === 1 ? 'row' : 'rows';
        $('#num-rows').text(`${dfLen.toString()} ${rowOrRows}`);
    }
    textWithoutMarkers = JSON.parse(responseParsed.df_unmarked);
    writeTable(responseParsed.df, responseParsed.showing_from);
    const showingFrom = responseParsed.showing_from;
    const showingTo = responseParsed.showing_to;
    const showingTotal = responseParsed.showing_total;
    updateShowingInfo(showingFrom, showingTo, showingTotal);
}

function preview() {
    // Snake case used for settings passed to Flask app
    const action = 'preview';
    // eslint-disable-next-line camelcase
    const search_re = $('#find').val();
    // eslint-disable-next-line camelcase
    const replace_re = $('#replace').val();
    const scope = $("input[name='scope']").filter(':checked').attr('id');
    const regex = $('#regex').is(':checked');
    const settings = {
        // eslint-disable-next-line camelcase
        search_re, replace_re, scope, regex,
    };
    const data = { action, settings };
    $.post('/find_replace', JSON.stringify(data)).done(handleResponse);
    $('#skip-page, #select-all, #deselect-all, #replace-remove, #replace-leave, #replace-all, #remove-all').removeClass('disabled');
}

function replaceAll() {
    const action = 'replace_all';
    const data = { action };
    $.post('/find_replace', JSON.stringify(data)).done(handleResponse);
    updateNumSelected();
}

function deselectAll() {
    $('tbody').find('tr').removeClass('table-secondary');
    updateNumSelected();
}

function selectAll() {
    $('tbody').find('tr').addClass('table-secondary');
    updateNumSelected();
}

function skipPage() {
    const action = 'next_page';
    const data = { action };
    $.post('/find_replace', JSON.stringify(data)).done(handleResponse);
}

function removeAll() {
    const data = { action: 'remove_all' };
    $.post('/find_replace', JSON.stringify(data)).done(handleResponse);
}

/*
Get indices of rows that have table-secondary class
*/
function getSelectedRowIndices() {
    const selected = [];
    $('tbody').find('tr.table-secondary').find('td.index').each((idx, e) => {
        const $this = $(e);
        selected.push(parseInt($this.text(), 10));
    });
    return selected;
}

/*
Get indices of rows that do not have either table-secondary or table-success classes
*/
function getUnselectedUneditedRowInfo() {
    const unselectedUnedited = [];
    $('tbody').find('tr:not(.table-secondary):not(.table-success)').find('td.index').each((idx, e) => {
        const $this = $(e);
        unselectedUnedited.push(parseInt($this.text(), 10));
    });
    return unselectedUnedited;
}
/*
Get index, source, and target from rows that do not have table-secondary class
but have table-success class
*/
function getUnselectedEditedRowInfo() {
    const unselectedEdited = {};
    $('tbody').find('tr.table-success:not(.table-secondary)').each((idx, e) => {
        const $this = $(e);
        const index = parseInt($this.find('td.index').text(), 10);
        const source = $this.find('td.source').text();
        const target = $this.find('td.target').text();
        unselectedEdited[index] = [source, target];
    });
    return unselectedEdited;
}

function replaceRemove() {
    const remove = getSelectedRowIndices();
    const update = getUnselectedEditedRowInfo();
    const replace = getUnselectedUneditedRowInfo();
    const action = 'replace_remove';
    const data = { action, remove, replace };
    $.post('/find_replace', JSON.stringify(data)).done(handleResponse);
}

function replaceLeave() {
    const update = getUnselectedEditedRowInfo();
    const action = 'replace_remove';
    const data = { action, replace };
    $.post('/find_replace', JSON.stringify(data)).done(handleResponse);
}


// handleKeyDown is used in shortcuts.js
// eslint-disable-next-line no-unused-vars
// function handleKeydown(e) {
//     const keyPressed = e.key.toLowerCase();
//     const $focusedElement = $(e.target);
//     const focusedTag = $focusedElement.prop('tagName');
//     if (focusedTag === 'BODY') {
//         if (keyPressed === 's') {
//             startOver();
//         } else if (keyPressed === 'p') {
//             skipPage();
//         } else if (keyPressed === 'a') {
//             selectAll();
//         } else if (keyPressed === 'd') {
//             deselectAll();
//         } else if (keyPressed === 'enter') {
//             submit();
//         } else if (keyPressed === 'x') {
//             removeAll();
//         }
//     } else if (keyPressed === 'escape') {
//         $(e.target).blur();
//     }
// }

$(() => {
    $('#find, #replace').on('input', () => {
        $('#skip-page, #select-all, #deselect-all, #replace-remove, #replace-leave, #replace-all, #remove-all').addClass('disabled');
    });
    $('#source, #target, #both, #either').on('click', () => {
        $('#skip-page, #select-all, #deselect-all, #replace-remove, #replace-leave, #replace-all, #remove-all').addClass('disabled');
    });
    $('#regex').on('change', () => {
        $('#skip-page, #select-all, #deselect-all, #replace-remove, #replace-leave, #replace-all, #remove-all').addClass('disabled');
    });
    $('#preview').on('click', preview);
    $('#skip-page').on('click', skipPage);
    $('#select-all').on('click', selectAll);
    $('#deselect-all').on('click', deselectAll);
    $('#remove-all').on('click', removeAll);
    $('#replace-all').on('click', replaceAll);
    $('#replace-remove').on('click', replaceRemove);
    $('#replace-leave').on('click', replaceLeave);
});
