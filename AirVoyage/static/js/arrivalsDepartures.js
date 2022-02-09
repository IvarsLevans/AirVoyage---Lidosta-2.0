window.addEventListener('load', () => {
  document.getElementsByTagName('table')[0].dataset.mode = 'arrival';
  applyFilters();
})

document.getElementById('arrivalButton').addEventListener('click', () => {
  document.getElementsByTagName('table')[0].dataset.mode = 'arrival';
  applyFilters();
  // arrivalElements = document.getElementsByClassName('arrival');
  // for(i = 0; i < arrivalElements.length; i++){
  //   arrivalElements[i].classList.remove('hidden');
  // }
  // departureElements = document.getElementsByClassName('departure');
  // for(i = 0; i < departureElements.length; i++){
  //   departureElements[i].classList.add('hidden');
  // }
})
document.getElementById('departureButton').addEventListener('click', () => {
  document.getElementsByTagName('table')[0].dataset.mode = 'departure';
  applyFilters();
  // arrivalElements = document.getElementsByClassName('arrival');
  // for(i = 0; i < arrivalElements.length; i++){
  //   arrivalElements[i].classList.add('hidden');
  // }
  // departureElements = document.getElementsByClassName('departure');
  // for(i = 0; i < departureElements.length; i++){
  //   departureElements[i].classList.remove('hidden');
  // }
})

document.getElementById('airportSelect').addEventListener("change", applyFilters);
function applyFilters(){
  mode = document.getElementsByTagName('table')[0].dataset.mode;
  rows = document.getElementsByTagName('tr');
  //isArrivalMode = rows[2].children[0].classList.contains('hidden')
  //airportIndex = isArrivalMode ? 5 : 6;
  selectedOption = document.getElementById('airportSelect').value;
  visibleRows = [];
  for(i = 2; i < rows.length; i++){
    if(mode === 'arrival' && rows[i].children[3].dataset.to == selectedOption){
      rows[i].children[0].innerText = rows[i].children[0].dataset.departuredate;
      rows[i].children[1].innerText = rows[i].children[1].dataset.departuretime;
      rows[i].children[3].innerText = rows[i].children[3].dataset.from;
      rows[i].classList.remove('hidden');
      visibleRows.push(rows[i]);
    }
    else if(mode === 'departure' && rows[i].children[3].dataset.from == selectedOption){
      rows[i].children[0].innerText = rows[i].children[0].dataset.arrivaldate;
      rows[i].children[1].innerText = rows[i].children[1].dataset.arrivaltime;
      rows[i].children[3].innerText = rows[i].children[3].dataset.to;
      rows[i].classList.remove('hidden');
      visibleRows.push(rows[i]);
    }
    else{
      rows[i].classList.add('hidden');
    }
    // if(selectedOption === rows[i].children[airportIndex].innerText ){
    //   rows[i].classList.remove('hidden');
    //   visibleRows.push(rows[i]);
    // }
    // else{
    //   rows[i].classList.add('hidden');
    // }
  }
  for(i = 0; i < visibleRows.length; i++){
    if(i % 2 == 1){
      visibleRows[i].classList.add('darker-background');
    }
    else{
      visibleRows[i].classList.remove('darker-background');
    }
    if(i == visibleRows.length - 1){
      visibleRows[i].classList.add('last-row');
    }
    else{
      visibleRows[i].classList.remove('last-row');
    }
  }
}