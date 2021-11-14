printButtons = document.getElementsByClassName('exportCSV');
for (let i = 0; i < printButtons.length; i++){
  printButtons[i].addEventListener("click", (e) => {
    let table = e.target.previousElementSibling;
    let data = []
    var rows = table.querySelectorAll("tr");
    for (var i = 0; i < rows.length; i++) {
      var row = [], cols = rows[i].querySelectorAll("td, th");
      for (var j = 0; j < cols.length; j++) {
          row.push(cols[j].innerText);
        }
      data.push(row.join(",")); 		
    }
    var dataStr = "data:text/csv;charset=utf-8," + encodeURIComponent(data.join("\n"));
    var a = document.createElement('a');
    a.setAttribute("href", dataStr);
    a.setAttribute("download", "statistics.csv");
    a.click();

    });
}

printButtons = document.getElementsByClassName('exportJSON');
for (let i = 0; i < printButtons.length; i++){
  printButtons[i].addEventListener("click", (e) => {
    let table = e.target.previousElementSibling.previousElementSibling;
    var data = [];

    // first row needs to be headers
    var headers = [];
    for (var i=0; i<table.rows[0].cells.length; i++) {
        headers[i] = table.rows[0].cells[i].innerHTML.toLowerCase().replace(/ /gi,'');
    }

    // go through cells
    for (var i=1; i<table.rows.length; i++) {

        var tableRow = table.rows[i];
        var rowData = {};

        for (var j=0; j<tableRow.cells.length; j++) {

            rowData[ headers[j] ] = tableRow.cells[j].innerHTML;

        }

        data.push(rowData);
    }
    console.log(JSON.stringify(data))
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
    var a = document.createElement('a');
    a.setAttribute("href", dataStr);
    a.setAttribute("download", "statistics.json");
    a.click();
  });
}

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}