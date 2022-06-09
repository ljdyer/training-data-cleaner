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
        newRow.append($(`<td class="source" contenteditable="true">${row.source}</td>`));
        newRow.append($(`<td class="target" contenteditable="true">${row.target}</td>`));
        tableBody.append(newRow);
        count += 1;
    }
    // tableBody.find('th,td.index').click(function toggleParent() {
    //     toggleRow($(this).parent());
    // });
    updateNumSelected();
}

function handleResponse(response) {
    const responseParsed = JSON.parse(response);
    if ('df_len' in responseParsed) {
        const dfLen = responseParsed.df_len;
        const rowOrRows = parseInt(dfLen, 10) === 1 ? 'row' : 'rows';
        $('#num-rows').text(`${dfLen.toString()} ${rowOrRows}`);
    }
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

// function applyOptions(options) {
//     $('#filter-scope').toggle(!options.filter_scope_disabled);
//     $('#order-col').toggle(!options.order_col_disabled);
//     $('#remove-all').toggleClass('disabled', options.disable_remove_all);
// }

// function toggleRow($row) {
//     $row.toggleClass('table-secondary');
//     updateNumSelected();
// }

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
    $.post('/edit', JSON.stringify(data)).done(handleResponse);
}

// function submit() {
//     // Get indices of selected rows
//     const remove = [];
//     $('tbody').find('tr.table-secondary').find('td.index').each(function getRemoveRowInfo() {
//         remove.push(parseInt($(this).text(), 10));
//     });
//     const update = {};
//     $('tbody').find('tr:not(.table-secondary)').each(function getUpdateRowInfo() {
//         const idx = parseInt($(this).find('td.index').text(), 10);
//         const source = $(this).find('td.source').text();
//         const target = $(this).find('td.target').text();
//         update[idx] = [source, target];
//     });
//     const action = 'submit';
//     const data = { action, remove, update };
//     $.post('/edit', JSON.stringify(data)).done(handleResponse);
// }

// function startOver() {
//     const data = { action: 'start_over' };
//     $.post('/edit', JSON.stringify(data)).done(handleResponse);
// }

// function removeAll() {
//     const data = { action: 'remove_all' };
//     $.post('/edit', JSON.stringify(data)).done(handleResponse);
// }

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
    // $('#submit').click(submit);
    // $('#start-over').click(startOver);

    // $('#remove-all').click(removeAll);
    // const filter = $.urlParam('filter');
    // if (filter) { $('#filter').val(filter); }
    // const filterScope = $.urlParam('filter_scope');
    // if (filterScope) {
    //     $('#filter-scope').show(0, () => {
    //         const thisFilterScope = $('#filter-scope').find(`#${filterScope}`);
    //         thisFilterScope.click();
    //         thisFilterScope.blur();
    //     });
    // }
    // const order = $.urlParam('order');
    // if (order) { $('#order').val(order); }
    // const orderCol = $.urlParam('order_col');
    // if (orderCol) {
    //     $('#order-col').show(0, () => {
    //         const thisOrderCol = $('#order-col').find(`#${orderCol}`);
    //         thisOrderCol.click();
    //         thisOrderCol.blur();
    //     });
    // }
    // const orderOrientation = $.urlParam('order_orientation');
    // if (orderOrientation) {
    //     $('#order-orientation').show(0, () => {
    //         const thisOrderOrientation = $('#order-orientation').find(`#${orderOrientation}`);
    //         thisOrderOrientation.click();
    //         thisOrderOrientation.blur();
    //     });
    // }
    // refreshWithNewSettings();
    // $("#filter, #order, input[name='filter-scope'], input[name='order-column'], input[name='order-orientation']").change(refreshWithNewSettings);
});
