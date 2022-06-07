// Function use before definition allowed
/* eslint-disable no-use-before-define */

function handleResponse(response) {
    const responseParsed = JSON.parse(response);
    if ('df_len' in responseParsed) {
        const dfLen = responseParsed.df_len;
        const rowOrRows = parseInt(dfLen, 10) === 1 ? 'row' : 'rows';
        $('#num-rows').text(`${dfLen.toString()} ${rowOrRows}`);
    }
    writeTable(responseParsed.df);
    updateShowingInfo(responseParsed.source_num, responseParsed.num_sources);
}

function submit() {
    // Get indices of selected rows
    const remove = [];
    $('tbody').find('tr:not(.table-success)').find('td.index').each((index, element) => {
        remove.push(parseInt($(element).text(), 10));
    });
    const update = {};
    $('tbody').find('tr.table-success').each((index, element) => {
        const idx = parseInt($(element).find('td.index').text(), 10);
        const source = $(element).find('td.source').text();
        const target = $(element).find('td.target').text();
        update[idx] = [source, target];
    });
    const action = 'submit';
    const data = { action, remove, update };
    $.post('/source_dup', JSON.stringify(data)).done(handleResponse);
}

function handleRowClick($row) {
    const isChecked = $row.hasClass('table-success');
    $row.toggleClass('table-success');
    if ($('#submitImmediately').is(':checked') && !isChecked) {
        submit();
    }
}

function writeTable(dfAsJson) {
    const dfParsed = JSON.parse(dfAsJson);
    const tableBody = $('#data-table').find('tbody');
    // Empty table
    tableBody.empty();
    // Append new rows
    let count = 1;
    for (const row of dfParsed) {
        const newRow = $('<tr>');
        newRow.append($(`<th>${count}</th>`));
        newRow.append($(`<td class="index">${row.index}</td>`));
        newRow.append($(`<td class="source" contenteditable="true">${row.source}</td>`));
        newRow.append($(`<td class="target" contenteditable="true">${row.target}</td>`));
        tableBody.append(newRow);
        count += 1;
    }
    tableBody.find('th,td.index').on('click', (event) => {
        handleRowClick($(event.currentTarget).parent());
    });
}

function updateShowingInfo(sourceNum, numSources) {
    if (numSources === 0) {
        $('#source-number').text(0);
    } else {
        $('#source-number').text(parseInt(sourceNum, 10) + 1);
    }
    $('#num-sources').text(numSources);
}

function refresh() {
    const action = 'start_over';
    const data = { action };
    $.post('/source_dup', JSON.stringify(data)).done(handleResponse);
}

function skipPage() {
    const action = 'next_page';
    const data = { action };
    $.post('/source_dup', JSON.stringify(data)).done(handleResponse);
}

function updateNumSelected() {
    $('#num-selected').text($('tr.table-success').length);
}

function deselectAll() {
    $('tbody').find('tr').removeClass('table-success');
    updateNumSelected();
}

function selectAll() {
    $('tbody').find('tr').addClass('table-success');
    updateNumSelected();
}

function startOver() {
    const data = { action: 'start_over' };
    $.post('/source_dup', JSON.stringify(data)).done(handleResponse);
}

// handleKeyDown is used in shortcuts.js
// eslint-disable-next-line no-unused-vars
function handleKeydown(e) {
    const keyPressed = e.key.toLowerCase();
    const $focusedElement = $(e.target);
    const focusedTag = $focusedElement.prop('tagName');
    if (focusedTag === 'BODY') {
        if (keyPressed === 's') {
            startOver();
        } else if (keyPressed === 'p') {
            skipPage();
        } else if (keyPressed === 'a') {
            selectAll();
        } else if (keyPressed === 'd') {
            deselectAll();
        } else if (keyPressed === 'enter') {
            submit();
        } else {
            const number = parseInt(keyPressed, 10);
            if (Number.isInteger(number)) {
                if (number > 0 && number < 10) {
                    const $theRow = $($('tbody').find('tr')[number - 1]);
                    if ($theRow.length) {
                        handleRowClick($theRow);
                    }
                }
            }
        }
    } else if (keyPressed === 'escape') {
        $(e.target).blur();
    }
}

$(() => {
    $('#skip-page').click(skipPage);
    $('#select-all').click(selectAll);
    $('#deselect-all').click(deselectAll);
    $('#submit').click(submit);
    $('#start-over').click(startOver);
    refresh();
});
