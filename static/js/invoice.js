
function idToRow(index) {
    return "#row-item-" + index;
}

function idToInput(index) {
    return "#price-pay-item-" + index;
}

function idToIconRemove(index) {
    return "#icon-remove-" + index;
}

function idToIconPlus(index) {
    return "#icon-plus-" + index;
}

function disableRow(index) {
//    if (confirm("Вы подтверждаете удаление?")) {

        yesDisableConfirm(index);

//    }
}

function enableRow(index) {
//    if (confirm("Вы подтверждаете добавление?")) {

        yesEnableConfirm(index);

//    }
}

function yesDisableConfirm(index) {
    console.log(index);
    $(idToRow(index)).addClass('warning');
    $(idToInput(index)).attr('readonly', 'readonly');
    $(idToIconPlus(index)).removeClass('hidden');
    $(idToIconRemove(index)).addClass('hidden');
}

function yesEnableConfirm(index) {
    console.log(index);
    $(idToRow(index)).removeClass('warning');
    $(idToInput(index)).removeAttr('readonly');
    $(idToIconPlus(index)).addClass('hidden');
    $(idToIconRemove(index)).removeClass('hidden');
}
