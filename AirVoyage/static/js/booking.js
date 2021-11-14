const form  = document.getElementById('filters');
form.addEventListener('submit', (event) => {
  event.preventDefault();


  url = '/booking';
  var request = new XMLHttpRequest();
  request.open('POST', url, true);
  request.onload = function() {
    document.getElementById('flights').innerHTML = request.responseText;
  };
  formData = new FormData();
  formData.append('action', 'filter');
  formData.append('from', form.from.value);
  formData.append('to', form.to.value);
  formData.append('dateFrom', form.dateFrom.value + ' ' + form.timeFrom.value);
  formData.append('dateTo', form.dateTo.value + ' ' + form.timeTo.value);
  request.send(formData);
});
document.getElementById('flights').addEventListener('click', (e) => {
  button = e.target;
  if(button.classList.contains('book')){
    url = '/booking';
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.onload = function() {
      if(request.responseText == "success"){
        button.textContent = "Booked";
      }
    };
    formData = new FormData();
    formData.append('action', 'book');
    formData.append('flightId', button.parentElement.parentElement.getAttribute('value'));
    request.send(formData);
  }
})