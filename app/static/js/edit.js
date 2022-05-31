$(function () {  
    $("#filter, #order, input[name='filter-scope'], input[name='order-column'], input[name='order-orientation']").change(function(){
        refreshWithNewSettings();
    });
})

function refreshWithNewSettings(filter, filterScope, order, orderColumn, orderOrientation){
    filter = $('#filter').find(":selected").val();
    filterScope = $("input[name='filter-scope']").filter(':checked').attr('id')
    order = $('#order').find(":selected").val();
    orderColumn = $("input[name='order-column']").filter(':checked').attr('id')
    orderOrientation = $("input[name='order-orientation']").filter(':checked').attr('id')
    settings = {
        'filter': filter,
        'filter_scope': filterScope,
        'order': order,
        'order_col': orderColumn,
        'order_orientation': orderOrientation
    }
    console.log(JSON.stringify(settings))
    $.post("/edit", settings)
        .done(function () {
        });
}