window.addEventListener('load', () => {
  let today = new Date();
  document.getElementById('monthSelector').value = today.getFullYear().toString() + '-' + (today.getMonth() + 1).toString().padStart(2, "0");
})
document.getElementById('monthSelector').addEventListener('change', (e)=>{
  let input = e.target;
  let dateParts = input.value.split('-');
  let date = dateParts[0] + '.' + dateParts[1];
  let rows = document.getElementsByTagName('tr');
  for(let i = 1; i < rows.length; i++){
    if(rows[i].children[2].innerHTML.substring(0,7) != date){
      rows[i].classList.add('hidden');
    }
    else{
      rows[i].classList.remove('hidden');
    }
  }
  console.log(input.value);
})

csvButtons = document.getElementsByClassName('exportCSV');
for (let i = 0; i < csvButtons.length; i++){
  csvButtons[i].addEventListener("click", (e) => {
    let table = e.target.previousElementSibling;
    let data = []
    var rows = table.querySelectorAll("tr");
    for (var i = 0; i < rows.length; i++) {
      if(rows[i].classList.contains('hidden')){
        continue;
      }
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

jsonButtons = document.getElementsByClassName('exportJSON');
for (let i = 0; i < jsonButtons.length; i++){
  jsonButtons[i].addEventListener("click", (e) => {
    let table = e.target.previousElementSibling.previousElementSibling;
    var data = [];

    // first row needs to be headers
    var headers = [];
    for (var i=0; i<table.rows[0].cells.length; i++) {
        headers[i] = table.rows[0].cells[i].innerHTML.toLowerCase().replace(/ /gi,'');
    }

    // go through cells
    for (var i=1; i<table.rows.length; i++) {
        if(table.rows[i].classList.contains('hidden')){
          continue;
        }

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