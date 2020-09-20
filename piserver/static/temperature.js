function populateTable(temperatureData) {
    let table = document.getElementById("tbl_body");
    for (const sensorId in temperatureData) {
        let row = table.insertRow();
        row.insertCell().innerHTML = `<samp>${sensorId}</samp>`;
        row.insertCell().innerHTML = `${temperatureData[sensorId]} &deg;C`
    }
}

$.getJSON("/temperature/readall", populateTable)
