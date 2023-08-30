const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const tooltip = bootstrap.Tooltip.getInstance('#info-tooltip');
const passInput = document.getElementById('password');

passInput.addEventListener("focus", function() {
    tooltip.show();
})
passInput.addEventListener("input", function() {
    tooltip.hide();
})
passInput.addEventListener("blur", function() {
    tooltip.hide();
})