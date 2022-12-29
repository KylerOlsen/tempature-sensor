// import { Chart } from './chart';
// import zoomPlugin from './chartjs-plugin-zoom';

// Chart.register(zoomPlugin);

let chart;
let current_selection;

class Chart_File {

    constructor(type, file_name, path, file_list) {
        this.next = null;
        this.prev = null;

        this.type = type;
        this.path = path;
        this.file_name = file_name;
        this.element = document.createElement("li");

        this.element.addEventListener("click", e => {this.click()});
        this.element.innerText = file_name;
        file_list.appendChild(this.element);
    }

    click() {
        if (current_selection) current_selection.element.classList.remove("file-selected");
        this.element.classList.add("file-selected");
        current_selection = this;
        this.getFileData();
    }

    getFileData() {
        fetch(`${this.type}?data=${this.path+'/'+this.file_name}`).then(data => {
            return data.json();
        }).then(json => {
            updateChart(json["data"]);
            this.updateMetadata(json["metadata"]);
        })
    }

    updateMetadata(data) {
        let element = document.createElement("ul");
        for (let [key, value] of Object.entries(data)) {
            let new_element = document.createElement("li");
            new_element.innerText = `${key} : ${value}`
            element.appendChild(new_element);
        }
        document.querySelector('#metadata').innerHTML = "";
        document.querySelector('#metadata').appendChild(element);
    }
}

class EventData_File extends Chart_File {

    getFileData() {
        fetch(`${this.type}?data=${this.path+'/'+this.file_name}`).then(data => {
            return data.json();
        }).then(json => {
            document.querySelector("#chartContainer").classList.add("hideChart");
            this.updateMetadata(json["data"]);
        })
    }

    updateMetadata(data) {
        let table = document.createElement("table");
        let table_body = document.createElement("tbody");
        let table_header = document.createElement("thead");
        let table_header_row = document.createElement("tr");
        for (let [key, value] of Object.entries(data)) {
            let table_element = document.createElement("th");
            table_element.innerText = `${key}`
            table_header_row.appendChild(table_element);
        }
        table_header.appendChild(table_header_row);
        table.appendChild(table_header);
        for (let i = 0; i < data['datetime'].length; i++) {
            let table_row = document.createElement("tr");
            for (let [key, value] of Object.entries(data)) {
                let table_element = document.createElement("td");
                table_element.innerText = `${value[i]}`
                table_row.appendChild(table_element);
            }
            table_body.appendChild(table_row);
        }
        table.appendChild(table_body);
        document.querySelector('#metadata').innerHTML = "";
        document.querySelector('#metadata').appendChild(table);
    }
}

function makeChart() {
    // let raw_data = [12.18,12.20,12.18,11.89,11.94,12.04,12.06,12.11,12.07,12.04,12.05,12.05,12.04,12.04,12.02,12.04,12.04,12.03,12.04,12.04,12.03,12.04,12.03,12.05,12.04,12.03,12.04,12.04,12.03,12.04,12.04,12.04,12.04,12.09,12.04,12.03,12.04,12.04,12.04,12.04,12.04,12.03,12.04,12.04,12.04,12.10,12.03,12.03,12.04,12.04,12.03,12.03,12.03,12.03,12.02,12.01,12.02,12.03,12.10,12.02,12.02,12.03,12.02,11.82,11.80,7.94,8.53,8.97,8.87,9.29,9.37,9.57,9.67,9.79,9.82,9.91,9.94,9.94,9.99,10.07,10.16,10.23,10.33,10.32,10.41,10.44,10.46,10.39,10.35,10.27,10.15,10.07,9.98,9.94,9.94,9.94,10.14,10.17,10.32,10.35,10.45,10.52,10.56,10.57,10.38,10.38,10.20,10.23,10.21,10.30,10.36,10.39,10.45,10.55,10.55,10.63,10.47,10.43,10.25,10.25,10.33,10.37,10.50,10.55,10.53,10.55,10.65,10.68,10.69,10.69,10.74,10.81,10.91,11.02,11.10,11.20,11.27,11.31,12.02,12.42,12.81,13.18,13.68,14.20,14.40,14.64,14.79,14.88,14.96,14.93,14.97,14.89,14.89,14.82,14.74,14.78,14.62,14.51,14.45,14.32,14.27,14.27,14.25,14.27,14.29,14.25,14.29,14.28,14.31,14.28,14.29,14.28,14.25,14.26,14.27,14.25,14.29,14.29,14.26,14.28,14.31,14.32,14.26,14.23,14.26,14.25,14.26,14.29,14.28,14.28,14.26,14.29,14.33,14.37,14.24,14.25,14.29,14.27,14.26,14.22,14.25,14.26,14.26,14.29,14.26,14.29,14.26,14.33,14.28,14.21,14.22,14.21,14.23,14.23,14.25,14.25,14.21,14.29,14.28,14.22,14.24,14.23,14.22,14.27,14.26,14.21,14.14,14.12,14.01,13.94,14.02,13.88,13.85,13.89,13.87,13.86,13.85,13.84,13.82,13.88,13.82,13.81,13.84,13.87,13.94,13.89,13.91,13.90,13.98,13.98,13.97,14.01,14.00,14.01,14.08,14.20,14.08,14.15,14.17,14.17,14.21,14.16,14.18,14.21,14.21,14.21,14.21,14.16,14.15,14.23,14.16,14.15,14.19,14.15,14.22,14.23,14.18,14.22,14.19,14.15,14.23,14.15,14.14,14.15,14.18,14.19,14.19,14.20,13.46,12.71,12.55,12.53,12.43,12.39,12.40,12.32,12.32,12.28,12.19,12.26,12.23,12.16,12.20,12.17,12.22,12.20,12.18,12.19,12.16,12.27,12.29,12.28,12.31,12.31,12.31,12.34,12.37,12.41,12.39,12.43,12.47,12.48,12.53,12.54,12.54,12.58,12.60,12.64,12.64,12.69,12.73,12.74,12.78,12.79,12.78,12.85,12.86,12.92,12.91,13.01,13.03,13.06,13.12,13.13,13.14,13.14,13.16,13.36,13.33,13.46,13.44,13.52,13.57,13.61,13.73,13.69,13.76,13.82,13.85,13.92,13.99,14.05,14.11,14.12,14.20,14.14,14.28,14.16,14.20,14.18,14.15,14.15,14.17,14.21,14.20,14.15,14.19,14.18,14.20,14.18,14.15,14.21,14.16,14.18,14.15,14.19,14.17,14.16,14.20,14.15,14.26,14.19,14.18,14.22,14.18,14.22,14.15,14.16,14.20,14.18,14.23];
    let raw_data = [];
    for (let i = 0; i <= 100; i++)
        raw_data.push(Math.log(i) * 2 + 6);

    // let data_list = [];
    let labels = [];
    for (let i = 0; i < raw_data.length; i++)
        labels.push(i);

    let data = {
        labels: labels,
        datasets: [{
            label: 'y = ln(x)',
            backgroundColor: 'rgb(16, 99, 255)',
            borderColor: 'rgb(16, 99, 255)',
            data: raw_data,
        }]
    };

    let config = {
        type: 'line',
        data: data,
        options: {
            scales: {
                y: {
                    max: 16,
                    min: 6,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
        }
    };

    chart = new Chart(
        document.querySelector('#chart'),
        config
    );
}

function updateChart(raw_data) {
    document.querySelector("#chartContainer").classList.remove("hideChart");
    let labels = [];
    for (let i = 0; i < raw_data.length; i++)
        labels.push(i);

    chart.data = {
        labels: labels,
        datasets: [{
            label: 'Volage over time',
            backgroundColor: 'rgb(16, 99, 255)',
            borderColor: 'rgb(16, 99, 255)',
            data: raw_data,
        }]
    };
    chart.update("none");
}

function displayFiles(type, files, path, element) {
    let current_file, previous_file;

    for (let [key, value] of Object.entries(files.folders)) {
        let folder = document.createElement("details");
        folder.innerHTML = `<summary>${key}</summary>`;
        element.appendChild(folder);
        if (path === '') displayFiles(type, value, key, folder);
        else displayFiles(type, value, path+'/'+key, folder);
    }

    let file_list = document.createElement("ul");
    element.appendChild(file_list);
    for (let value of files.files) {
        if (value.endsWith("EventData"))
            current_file = new EventData_File(type, value, path, file_list);
        else
            current_file = new Chart_File(type, value, path, file_list);
        if (previous_file) {
            previous_file.next = current_file;
            current_file.prev = previous_file;
        }
        previous_file = current_file;
    }
}

function getFiles(type) {
    fetch(`${type}?files=true`).then(data => {
        return data.json();
    }).then(json => {
        document.querySelector("#fileTree").innerHTML = "";
        displayFiles(type, json, "", document.querySelector("#fileTree"));
    })
}

function main() {
    makeChart();
    getFiles("battery.php");
    window.addEventListener("keydown", (event) => {
        if (event.key === "ArrowUp" && current_selection && current_selection.prev) {
            current_selection.prev.click();
            event.preventDefault();
        }
        if (event.key === "ArrowDown" && current_selection && current_selection.next) {
            current_selection.next.click();
            event.preventDefault();
        }
    });
}

window.addEventListener('load', main);
