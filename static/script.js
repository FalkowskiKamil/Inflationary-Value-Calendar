// DOM elements
let databaseType = document.getElementById("databaseType");
let selectBasedOnKey = document.getElementById("databaseKey");
let stockInput = document.getElementById("stockNameContainer");
let formSubmit = document.getElementById("formSubmit");

// Function to handle changes in the database type
function handleDatabaseTypeChange() {
    formSubmit.classList.remove("hidden");
    selectBasedOnKey.innerHTML = "";
    let listType = databaseType.value;
    if (listType !== "stock") {
        selectBasedOnKey.classList.remove("hidden");
        stockInput.classList.add("hidden");
        let apiUrl = `http://127.0.0.1:8000/api/list_of_available/${listType}`;
        getKeyFromDatabases(apiUrl);
    } else {
        selectBasedOnKey.classList.add("hidden");
        stockInput.classList.remove("hidden");
    }
}

// Function to fetch keys from databases
async function getKeyFromDatabases(apiUrl) {
    let response = await fetch(apiUrl);
    let data = await response.json();
    for (let i = 0; i < data.list.length; i++) {
        let newOption = document.createElement("option");
        newOption.text = data.list[i];
        newOption.value = data.list[i];
        selectBasedOnKey.appendChild(newOption);
    }
}

// Event listener for database type change
databaseType.addEventListener("change", handleDatabaseTypeChange);
