let textWithoutMarkers = {};
let $allActionButtons = null;
const thisRoute = '/find_replace';

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
    if ($row.attr('data-edited')) { $row.toggleClass('table-success'); }
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
    updateNumSelected();
}

function postToFlask(data) {
    $.post(thisRoute, JSON.stringify(data)).done(handleResponse);
}

function postActionOnly(action) {
    const data = { action };
    postToFlask(data);
}

function preview() {
    const action = 'preview';
    // Snake case used for settings passed to Flask app
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
    postToFlask(data);
    $allActionButtons.removeClass('disabled');
}

function deselectAll() {
    $('tbody').find('tr').each((idx, e) => {
        const $this = $(e);
        if ($this.attr('data-edited')) {
            $this.addClass('table-success');
        }
        $this.removeClass('table-secondary');
    });
    updateNumSelected();
}

function selectAll() {
    $('tbody').find('tr').addClass('table-secondary');
    $('tbody').find('tr').removeClass('table-success');
    updateNumSelected();
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
Get index, source, and target from rows that do not have table-secondary class
but have table-success class
*/
function getUnselectedRowInfo() {
    const unselected = {};
    $('tbody').find('tr:not(.table-secondary)').each((idx, e) => {
        const $this = $(e);
        const index = parseInt($this.find('td.index').text(), 10);
        let source = '';
        let target = '';
        if ($this.hasClass('table-success')) {
            source = $this.find('td.source').text();
            target = $this.find('td.target').text();
        } else {
            for (let i = 0; i < textWithoutMarkers.length; i += 1) {
                if (textWithoutMarkers[i].index === index) {
                    source = textWithoutMarkers[i].source;
                    target = textWithoutMarkers[i].target;
                }
            }
        }
        unselected[index] = [source, target];
    });
    return unselected;
}

function replaceRemove() {
    const remove = getSelectedRowIndices();
    const update = getUnselectedRowInfo();
    const action = 'replace_remove';
    const data = { action, remove, update };
    postToFlask(data);
}

function replaceLeave() {
    const update = getUnselectedRowInfo();
    const action = 'replace_leave';
    const data = { action, update };
    postToFlask(data);
}

// handleKeyDown is used in shortcuts.js
// eslint-disable-next-line no-unused-vars
function handleKeydown(e) {
    const keyPressed = e.key.toLowerCase();
    const { ctrlKey } = e;
    const $focusedElement = $(e.target);
    const focusedTag = $focusedElement.prop('tagName');
    const cellFocused = (focusedTag === 'TD');
    // Escape blurs currently selected element
    if (keyPressed === 'escape') {
        $(e.target).blur();
    // Other shortcuts fire as long as a table cell is not being edited
    } else if (['find', 'replace'].indexOf($focusedElement.attr('id')) !== -1
               && keyPressed === 'enter') {
        preview();
    } else if (!cellFocused) {
        $('[data-shortcut-key]').each((idx, e_) => {
            const thisShortcutKey = $(e_).attr('data-shortcut-key').toLowerCase();
            const needCtrlKey = ($(e_).attr('data-shortcut-ctrl') === 'true');
            if (keyPressed === thisShortcutKey && ctrlKey === needCtrlKey) {
                $(e_).trigger('click');
            }
        });
    }
}

$(() => {
    $allActionButtons = $('a[data-action-button=true]');
    $('#find, #replace').on('input', () => { $allActionButtons.addClass('disabled'); });
    $('#source, #target, #both, #either').on('click', () => { $allActionButtons.addClass('disabled'); });
    $('#regex').on('change', () => { $allActionButtons.addClass('disabled'); });
    $('#preview').on('click', preview);
    $('#skip-page').on('click', () => { postActionOnly('next_page'); });
    $('#select-all').on('click', selectAll);
    $('#deselect-all').on('click', deselectAll);
    $('#remove-all').on('click', () => { postActionOnly('remove_all'); });
    $('#replace-all').on('click', () => { postActionOnly('replace_all'); });
    $('#replace-remove').on('click', replaceRemove);
    $('#replace-leave').on('click', replaceLeave);
    if ($('#find').val().length > 0) { preview(); }
});
