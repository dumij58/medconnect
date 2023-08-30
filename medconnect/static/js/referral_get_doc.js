const doctorUrl = document.currentScript.getAttribute("get-doc-url");

async function fetchSuggestions(url, datalistElement) {
    const response = await fetch(url);
    const data = await response.json();
    
    const otherOption = document.createElement('option');
    otherOption.value = "Other Doctor";
    datalistElement.appendChild(otherOption);

    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        datalistElement.appendChild(option);
    });
}

fetchSuggestions(doctorUrl, document.getElementById('doctor-list'));