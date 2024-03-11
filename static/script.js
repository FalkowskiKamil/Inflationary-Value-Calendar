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
        let apiUrl = `http://127.0.0.1:8000/api/list_of_available/`;
        getKeyFromDatabases(apiUrl, listType);
    } else {
        selectBasedOnKey.classList.add("hidden");
        stockInput.classList.remove("hidden");
    }
}

// Function to fetch keys from databases
async function getKeyFromDatabases(apiUrl, listType) {
    let response = await fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `list_type=${encodeURIComponent(listType)}`,
    });
    let data = await response.json();

    let category = Object.keys(data)[0];
    let dataList = data[category];

    for (let i = 0; i < dataList.length; i++) {
        let newOption = document.createElement("option");
        newOption.text = dataList[i];
        newOption.value = dataList[i];
        selectBasedOnKey.appendChild(newOption);
    }
}

// Event listener for database type change
databaseType.addEventListener("change", handleDatabaseTypeChange);
