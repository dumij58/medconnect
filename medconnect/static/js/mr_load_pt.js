const selectGender = document.getElementById("gender");
const selectDOB = document.getElementById("dob");

document.addEventListener("DOMContentLoaded", function() {

    preSelectOption(selectGender);
    preSelectDate(selectDOB);

});

function preSelectOption(selectField) {
    var selectedOptionValue = selectField.getAttribute("data-selected-option");

    for (var i = 0; i < selectField.options.length; i++) {
        if (selectField.options[i].value === selectedOptionValue) {
            selectField.options[i].selected = true;
            break;
        }
    }
}

function preSelectDate(dateField) {
    var selectedDateValue = dateField.getAttribute("data-selected-date");

    dateField.value = selectedDateValue;
}