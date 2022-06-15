let lastToggled = null;
let lastToggledState = '';
let $settingsComponents = null;
const thisRoute = '/edit';

function range(from, to) {
    const lowest = Math.min(from, to);
    const highest = Math.max(from, to);
    return Array.from({ length: highest - lowest + 1 }, (v, k) => k + lowest);
}

function applyOptions(options) {
    $('#filter-scope').toggle(!options.filter_scope_disabled);
    $('#order-col').toggle(!options.order_col_disabled);
    $('#remove-all').toggleClass('disabled', options.disable_remove_all);
}

function updateNumSelected() {
    $('#num-selected').text($('tr.table-secondary').length);
}

function toggleRow($row) {
    $row.toggleClass('table-secondary');
    lastToggled = parseInt($row.find('th').text(), 10);
    lastToggledState = $row.hasClass('table-secondary');
    updateNumSelected();
}

function toggleMultiple($row) {
    const rowClicked = parseInt($row.find('th').text(), 10);
    const indicesToToggle = range(rowClicked, lastToggled);
    $('tbody').find('tr').each((idx, e) => {
        const $this = $(e);
        if (indicesToToggle.indexOf(idx + 1) !== -1) {
            $this.toggleClass('table-secondary', lastToggledState);
        }
    });
}

function handleRowClick($row, shiftKey) {
    if (!shiftKey) {
        toggleRow($row);
    }
    if (shiftKey) {
        toggleMultiple($row);
    }
}

function deselectAll() {
    $('tbody').find('tr').removeClass('table-secondary');
    updateNumSelected();
}

function selectAll() {
    $('tbody').find('tr').addClass('table-secondary');
    updateNumSelected();
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
    tableBody.find('th,td.index').on('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const $row = $(e.currentTarget).parent();
        handleRowClick($row, e.shiftKey);
    }).on('dblclick', (e) => {
        index = parseInt($(e.currentTarget).parent().find('td.index').text(), 10);
        showIndex(index);
    });
    updateNumSelected();
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

function handleResponse(response) {
    const responseParsed = JSON.parse(response);
    if ('options' in responseParsed) {
        applyOptions(responseParsed.options);
    }
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

function postToFlask(data) {
    $.post(thisRoute, JSON.stringify(data)).done(handleResponse);
}

function postActionOnly(action) {
    const data = { action };
    postToFlask(data);
}

function refreshWithNewSettings() {
    const filter = $('#filter').find(':selected').val();
    const filterScope = $("input[name='filter-scope']").filter(':checked').attr('id');
    const order = $('#order').find(':selected').val();
    const orderColumn = $("input[name='order-column']").filter(':checked').attr('id');
    const orderOrientation = $("input[name='order-orientation']").filter(':checked').attr('id');
    const settings = {
        filter,
        filter_scope: filterScope,
        order,
        order_col: orderColumn,
        order_orientation: orderOrientation,
    };
    const action = 'new_settings';
    const data = { action, settings };
    postToFlask(data);
}

function submit() {
    // Get indices of selected rows
    const remove = [];
    $('tbody').find('tr.table-secondary').find('td.index').each(function getRemoveRowInfo() {
        remove.push(parseInt($(this).text(), 10));
    });
    const update = {};
    $('tbody').find('tr:not(.table-secondary)').each(function getUpdateRowInfo() {
        const idx = parseInt($(this).find('td.index').text(), 10);
        const source = $(this).find('td.source').text();
        const target = $(this).find('td.target').text();
        update[idx] = [source, target];
    });
    const action = 'submit';
    const data = { action, remove, update };
    postToFlask(data);
}

// handleKeyDown is used in shortcuts.js
// eslint-disable-next-line no-unused-vars
function handleKeydown(e) {
    const keyPressed = e.key.toLowerCase();
    const $focusedElement = $(e.target);
    const focusedTag = $focusedElement.prop('tagName');
    const cellFocused = (focusedTag === 'TD');
    // Escape blurs currently selected element
    if (keyPressed === 'escape') {
        $(e.target).blur();
    // Other shortcuts fire as long as a table cell is not being edited
    } else if (!cellFocused) {
        $('[data-shortcut-key]').each((idx, e_) => {
            const thisShortcutKey = $(e_).attr('data-shortcut-key').toLowerCase();
            if (keyPressed === thisShortcutKey) {
                $(e_).trigger('click');
            }
        });
    }
}

$(() => {
    $settingsComponents = $('[data-settings-component="true"]');
    $('#skip-page').click(() => postActionOnly('next_page'));
    $('#select-all').click(selectAll);
    $('#deselect-all').click(deselectAll);
    $('#submit').click(submit);
    $('#start-over').click(() => postActionOnly('start_over'));
    $('#remove-all').click(() => postActionOnly('remove_all'));
    refreshWithNewSettings();
    $settingsComponents.change(refreshWithNewSettings);
});
