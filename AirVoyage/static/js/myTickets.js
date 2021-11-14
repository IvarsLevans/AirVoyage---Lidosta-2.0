printButtons = document.getElementsByClassName('print');
for (let i = 0; i < printButtons.length; i++){
  printButtons[i].addEventListener("click", (e) => {
    let table = e.target.previousElementSibling;
    table.classList.add("printable");
    window.print();
    });
}
cancelButtons = document.getElementsByClassName('cancel');
for (let i = 0; i < cancelButtons.length; i++){
  cancelButtons[i].addEventListener("click", (e) => {
    let table = e.target.previousElementSibling.previousElementSibling;
    
    url = '/myTickets';
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.onload = function() {
      if (request.responseText == "success"){
        table.parentElement.remove();
      }
    };
    formData = new FormData();
    formData.append('action', 'cancel');
    formData.append('ticketId', table.id);
    request.send(formData);
    });
}