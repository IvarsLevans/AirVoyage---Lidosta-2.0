printButtons = document.getElementsByClassName('print');
for (let i = 0; i < printButtons.length; i++){
  printButtons[i].addEventListener("click", (e) => {
    let div = e.target.parentElement;
    div.classList.add("printable");
    window.print();
    div.classList.remove("printable");
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
window.addEventListener("load", (e)=>{
  temp = location.pathname.split('/');
  if(temp.length > 2 && temp[2]){
    isFound = false;
    orderSelect = document.getElementById('order');
    for(let i = 0; i < orderSelect.options.length; i++){
      if(temp[2] == orderSelect.options[i].value){
        isFound = true;
        break;
      }
    }
    if(isFound){
      orderSelect.value = temp[2];
    }
  }
});
document.getElementById('order').addEventListener("change", (e)=>{
  if(e.target.value != 'any'){
    location.pathname = '/myTickets/' + e.target.value;
  }
  else{
    location.pathname = '/myTickets';
  }
});
