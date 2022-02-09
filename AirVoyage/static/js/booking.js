//filter
const form  = document.getElementById('filters');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  rows = document.querySelectorAll('#flights tr');
  for(i = 1; i < rows.length; i++){
    row = rows[i];
    columns = row.children;
    if(form.from.value !== '' && columns[0].innerText !== form.from.value){
      row.style.display = 'none';
      continue;
    }
    else if(form.to.value !== '' && columns[1].innerText !== form.to.value){
      row.style.display = 'none';
      continue;
    }
    dateFrom = form.dateFrom.value + ' ' + form.timeFrom.value;
    if(dateFrom != ' ' && columns[2].innerText < dateFrom){
      row.style.display = 'none';
      continue;
    }
    dateTo = form.dateTo.value + ' ' + form.timeTo.value;
    if(dateTo[0] !== ' ' && columns[3].innerText > dateTo){
      row.style.display = 'none';
      continue;
    }
    row.style.display = 'table-row';
  }
});

//book
document.getElementById('flights').addEventListener('click', (e) => {
  button = e.target;
  if(button.classList.contains('book')){
    url = '/booking';
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.onload = function() {
      if(request.responseText == "success"){
        button.outerHTML = "Booked";
      }
    };
    formData = new FormData();
    formData.append('action', 'book');
    formData.append('flightId', button.parentElement.parentElement.getAttribute('value'));
    request.send(formData);
  }
})

const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

// do the work...
document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
    const table = th.closest('table');
    Array.from(table.querySelectorAll('tr:nth-child(n+2)'))
        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
        .forEach(tr => table.appendChild(tr) );
})));
