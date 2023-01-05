// import { Chart } from './chart';
// import zoomPlugin from './chartjs-plugin-zoom';

// Chart.register(zoomPlugin);

let chart;
let current_selection;

class File {

    constructor(file_name, path, file_list) {
        this.next = null;
        this.prev = null;

        this.type = this.constructor.type;
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
    }
}

class Chart_File extends File {

    click() {
        if (current_selection) current_selection.element.classList.remove("file-selected");
        this.element.classList.add("file-selected");
        current_selection = this;
        this.getFileData();
    }

    getFileData() {
        fetch(`${this.type}.php?data=${this.path+'/'+this.file_name}`).then(data => {
            return data.json();
        }).then(json => {
            this.updateChart(json["data"]);
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

    updateChart(raw_data) {
        document.querySelector("#chartContainer").classList.remove("hideChart");
        let labels = [];
        for (let i = 0; i < raw_data.length; i++)
            labels.push(i);

        chart.data = {
            labels: labels,
            datasets: [{
                label: "Data",
                backgroundColor: 'rgb(16, 99, 255)',
                borderColor: 'rgb(16, 99, 255)',
                data: raw_data,
            }]
        };
        chart.update("none");
    }

    static getFiles() {
        document.querySelector("#chartContainer").classList.remove("hideChart");
        document.querySelector('#metadata').innerHTML = "";
        document.querySelector('#fileTree').innerHTML = "";
        let raw_data = [];
        for (let i = 0; i <= 100; i++)
            raw_data.push(Math.log(i) * 2);

        let labels = [];
        for (let i = 0; i < raw_data.length; i++)
            labels.push(i);

        chart.data = {
            labels: labels,
            datasets: [{
                label: 'y = ln(x)',
                backgroundColor: 'rgb(16, 99, 255)',
                borderColor: 'rgb(16, 99, 255)',
                data: raw_data,
            }]
        };

        chart.type = 'line';

        chart.options = {
            scales: {
                y: {
                    ticks: {
                        stepSize: 1
                    }
                }
            },
        }

        chart.update("none");

        fetch(`${this.type}.php?files=true`).then(data => {
            return data.json();
        }).then(json => {
            document.querySelector("#fileTree").innerHTML = "";
            this.displayFiles(json, "", document.querySelector("#fileTree"));
        })
    }

    static displayFiles(files, path, element) {
        let current_file, previous_file;

        for (let [key, value] of Object.entries(files.folders)) {
            let folder = document.createElement("details");
            folder.innerHTML = `<summary>${key}</summary>`;
            element.appendChild(folder);
            if (path === '') this.displayFiles(value, key, folder);
            else this.displayFiles(value, path + '/' + key, folder);
        }

        let file_list = document.createElement("ul");
        element.appendChild(file_list);
        for (let value of files.files) {
            current_file = new this(value, path, file_list);
            if (previous_file) {
                previous_file.next = current_file;
                current_file.prev = previous_file;
            }
            previous_file = current_file;
        }
    }
}

class Temperature_Chart_File extends Chart_File {

    static type = "temperature";

    updateChart(raw_data) {
        document.querySelector("#chartContainer").classList.remove("hideChart");
        let labels = [];
        for (let i = 0; i < raw_data.length; i++)
            labels.push(i);

        chart.data = {
            labels: labels,
            datasets: [{
                label: "Temperature over time",
                backgroundColor: 'rgb(16, 99, 255)',
                borderColor: 'rgb(16, 99, 255)',
                data: raw_data,
            }]
        };
        chart.update("none");
    }
}

class Battery_Chart_File extends Chart_File {

    static type = "battery";

    updateChart(raw_data) {
        document.querySelector("#chartContainer").classList.remove("hideChart");
        let labels = [];
        for (let i = 0; i < raw_data.length; i++)
            labels.push(i);

        chart.data = {
            labels: labels,
            datasets: [{
                label: "Voltage over time",
                backgroundColor: 'rgb(16, 99, 255)',
                borderColor: 'rgb(16, 99, 255)',
                data: raw_data,
            }]
        };
        chart.update("none");
    }

    static getFiles() {
        document.querySelector("#chartContainer").classList.remove("hideChart");
        document.querySelector('#metadata').innerHTML = "";
        document.querySelector('#fileTree').innerHTML = "";
        let raw_data = [];
        for (let i = 0; i <= 100; i++)
            raw_data.push(Math.log(i) * 2 + 6);

        let labels = [];
        for (let i = 0; i < raw_data.length; i++)
            labels.push(i);

        chart.data = {
            labels: labels,
            datasets: [{
                label: 'y = ln(x)',
                backgroundColor: 'rgb(16, 99, 255)',
                borderColor: 'rgb(16, 99, 255)',
                data: raw_data,
            }]
        };

        chart.type = 'line';

        chart.options = {
            scales: {
                y: {
                    ticks: {
                        max: 16,
                        min: 6,
                        stepSize: 1
                    }
                }
            },
        }

        chart.update("none");

        fetch(`${this.type}.php?files=true`).then(data => {
            return data.json();
        }).then(json => {
            document.querySelector("#fileTree").innerHTML = "";
            this.displayFiles(json, "", document.querySelector("#fileTree"));
        })
    }

    static displayFiles(files, path, element) {
        let current_file, previous_file;

        for (let [key, value] of Object.entries(files.folders)) {
            let folder = document.createElement("details");
            folder.innerHTML = `<summary>${key}</summary>`;
            element.appendChild(folder);
            if (path === '') this.displayFiles(value, key, folder);
            else this.displayFiles(value, path + '/' + key, folder);
        }

        let file_list = document.createElement("ul");
        element.appendChild(file_list);
        for (let value of files.files) {
            if (value.endsWith("EventData"))
                current_file = new Battery_EventData_File(value, path, file_list);
            else
                current_file = new this(value, path, file_list);
            if (previous_file) {
                previous_file.next = current_file;
                current_file.prev = previous_file;
            }
            previous_file = current_file;
        }
    }
}

class Battery_EventData_File extends File {

    static type = "battery";

    click() {
        if (current_selection) current_selection.element.classList.remove("file-selected");
        this.element.classList.add("file-selected");
        current_selection = this;
        this.getFileData();
    }

    getFileData() {
        fetch(`${this.type}.php?data=${this.path+'/'+this.file_name}`).then(data => {
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

class Acceleration_Chart_File extends Chart_File {

    static type = "acceleration";

    getFileData() {
        fetch(`${this.type}.php?data=${this.path + '/' + this.file_name}`).then(data => {
            return data.json();
        }).then(json => {
            this.updateChart(json["x_data"],json["y_data"],json["z_data"]);
            this.updateMetadata(json["metadata"]);
        })
    }

    updateChart(x_data, y_data, z_data) {
        document.querySelector("#chartContainer").classList.remove("hideChart");
        let labels = [];
        for (let i = 0; i < x_data.length; i++)
            labels.push(i);

        chart.data = {
            labels: labels,
            datasets: [{
                label: "X Data",
                backgroundColor: 'rgb(16, 99, 255)',
                borderColor: 'rgb(16, 99, 255)',
                data: x_data,
            },{
                label: "Y Data",
                backgroundColor: 'rgb(255, 16, 99)',
                borderColor: 'rgb(255, 16, 99)',
                data: y_data,
            },{
                label: "Z Data",
                backgroundColor: 'rgb(16, 255, 99)',
                borderColor: 'rgb(16, 255, 99)',
                data: z_data,
            }]
        };
        chart.update("none");
    }
}

function makeChart() {
    let raw_data = [];
    for (let i = 0; i <= 100; i++)
        raw_data.push(Math.log(i) * 2);

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

window.addEventListener('load', () => {
    makeChart();
    Battery_Chart_File.getFiles();

    document.querySelector("#temp").addEventListener("click", () => { Temperature_Chart_File.getFiles() });
    document.querySelector("#batt").addEventListener("click", () => { Battery_Chart_File.getFiles() });
    document.querySelector("#accel").addEventListener("click", () => { Acceleration_Chart_File.getFiles() });

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
});
