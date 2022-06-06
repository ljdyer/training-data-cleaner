function refresh() {
    const action = 'start_over';
    const data = { action };
    $.post('/source_dup', JSON.stringify(data)).done(handleResponse);
}

function handleResponse(response) {
    const responseParsed = JSON.parse(response);
    if ('df_len' in response) {
        const dfLen = responseParsed.df_len;
        const rowOrRows = parseInt(dfLen, 10) === 1 ? 'row' : 'rows';
        $('#num-rows').text(dfLen.toString() + ' ' + rowOrRows);
    }
    writeTable(responseParsed.df);
    updateShowingInfo(responseParsed.source_num, responseParsed.num_sources);
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
    tableBody.find('th,td.index').click(() => { handleRowClick($(this).parent()); });
}

function updateShowingInfo(sourceNum, numSources) {
    if (numSources == 0) {
        $('#source-number').text(0);
    } else{
        $('#source-number').text(parseInt(sourceNum) + 1);
    }
    $('#num-sources').text(numSources);
}

function skipPage() {
    action = 'next_page';
    data = { action };
    $.post('/source_dup', JSON.stringify(data))
        .done(function (response) {
            handleResponse(response);
        });
}

function handleRowClick($row) {
    isChecked = $row.hasClass('table-success');
    $row.toggleClass('table-success');
    if ($('#submitImmediately').is(':checked') && !isChecked) {
        submit();
    }
}

function deselectAll() {
    $('tbody').find('tr').removeClass('table-success');
    updateNumSelected();
}

function selectAll() {
    $('tbody').find('tr').addClass('table-success');
    updateNumSelected();
}

function updateNumSelected() {
    $('#num-selected').text($('tr.table-success').length);
}

function submit() {
    // Get indices of selected rows
    let remove = [];
    $('tbody').find('tr:not(.table-success)').find('td.index').each(function() {
        remove.push(parseInt($(this).text()));
    });
    let update = {};
    $('tbody').find('tr.table-success').each(function() {
        let idx = parseInt($(this).find('td.index').text());
        let source = $(this).find('td.source').text();
        let target = $(this).find('td.target').text();
        update[idx] = [source, target];
    });
    action = 'submit';
    data = {action, remove, update};
    $.post('/source_dup', JSON.stringify(data))
        .done(function (response) {
            handleResponse(response);
        });
}

function startOver() {
    data = { action: 'start_over'};
    $.post('/source_dup', JSON.stringify(data))
        .done(function (response) {
            handleResponse(response);
        });
    }

function handleKeydown(e) {
    keyPressed = e.key.toLowerCase();
    $focusedElement = $(e.target);
    let focusedTag = $focusedElement.prop('tagName');
    if (focusedTag == 'BODY') {
        if (keyPressed == 's') {
            startOver();
        } else if (keyPressed == 'p') {
            skipPage();
        } else if (keyPressed == 'a') {
            selectAll();
        } else if (keyPressed == 'd') {
            deselectAll();
        } else if (keyPressed == 'enter') {
            submit();
        } else {
            number = parseInt(keyPressed);
            if (Number.isInteger(number)) {
                if (0 < number && number < 10) {
                    $theRow = $($('tbody').find('tr')[number-1]);
                    if ($theRow.length) {
                        handleRowClick($theRow);
                    }
                }
            }
        }
    } else{
        if (keyPressed == 'escape') {
            $(e.target).blur();
        }
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