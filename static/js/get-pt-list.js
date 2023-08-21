const patientUrl = document.currentScript.getAttribute('get-pt-url');
const hospitalUrl = document.currentScript.getAttribute('get-hl-url');

async function fetchSuggestions(url, datalistElement) {
    const response = await fetch(url);
    const data = await response.json();
    
    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        datalistElement.appendChild(option);
    });
}

fetchSuggestions(patientUrl, document.getElementById('patient-list'));
fetchSuggestions(hospitalUrl, document.getElementById('hospital-list'));

const searchBtn = document.getElementById('search-btn');
const ptInput = document.getElementById('pt');
const hlInput = document.getElementById('hl');

function toggleModal() {
    if (ptInput.value.trim() === "" && hlInput.value.trim() === "") {
        searchBtn.setAttribute("data-bs-toggle", "modal");
        searchBtn.setAttribute("data-bs-target", "#alertModal");
        searchBtn.setAttribute("type", "button");
    } else {
        searchBtn.removeAttribute("data-bs-toggle");
        searchBtn.removeAttribute("data-bs-target");
        searchBtn.setAttribute("type", "submit");
    }
}

toggleModal();
ptInput.addEventListener('input', function() {
    toggleModal();
});
hlInput.addEventListener('input', function() {
    toggleModal();
});