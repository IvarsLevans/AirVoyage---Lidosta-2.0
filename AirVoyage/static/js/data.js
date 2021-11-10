document.getElementById("airports").addEventListener("click", (e) => {
  addDelete(e)
})
document.getElementById("airplanes").addEventListener("click", (e) => {
  addDelete(e)
})
function addDelete(e){
  button = e.target;
  if(button.classList.contains('delete')) {
    row = e.target.parentElement.parentElement
    key = row.getElementsByClassName('key')[0].textContent;

    url = '/data';
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.onload = function() {
      if(request.responseText === "successful"){
        row.parentElement.removeChild(row);
      }
      else if(request.responseText === "permissionDenied"){
        document.location.href = '../'
      }
    };

    request.onerror = function() {
      // request failed
    };
    formData = new FormData();
    formData.append('action', 'delete');
    formData.append('key', key);
    request.send(formData);
  }
  else if (button.classList.contains('apply')){

  }
}

let editedFields = new FormData();
let editedAirportsAbrriviations = '';
function doubleClick(node) {
  if(node.classList.contains('editable')) {
    node.ondblclick=function() {
      // airportAbbreviation = node.parentElement.getElementsByClassName('key')[0].textContent;
      // if(!(airportAbbreviation in editedAirportsAbrriviations.split(' '))){
      //   editedAirportsAbrriviations += ' ' + airportAbbreviation;
      //   values = ''
      //   for(let cell of node.parentElement.cells){
      //     values += cell.textContent + ',';
      //   }
      //   editedFields.append(airportAbbreviation, values);
      //   console.log(editedFields.get(airportAbbreviation))
      // }
      // else{
      //   values = ''
      //   for(let cell of node.parentElement.cells){
      //     values += cell.textContent + ',';
      //   }
      //   editedFields[editedAirportsAbrriviations] = values();
      // }
      var val=this.innerHTML;
      var input=document.createElement("input");
      input.value=val;

      input.onblur=function(){
        let responseText = changeField(
          this.parentNode,     
          node.parentElement.parentElement.parentElement.id,
          node.parentElement.getElementsByClassName('key')[0].getAttribute('key'),
          node.getAttribute('value'),
          this.value);
        var val = this.value;
        this.parentNode.innerHTML=val;
      }
      
      this.innerHTML="";
      this.appendChild(input);
      input.focus();
    }
  }
}
document.querySelectorAll("table tr td").forEach(function(node) {
  doubleClick(node)
});

function changeField(node, table, key, field, value){
  url = '/data';
  var request = new XMLHttpRequest();
  request.open('POST', url, true);
  request.onload = function() {
    if(request.responseText == ''){
      node.innerHTML = 'error'
      node.style.color = "red";
    }
    else{
      node.style.color = "black";
      if(node.classList.contains('key')){
        node.setAttribute('key', node.innerHTML);
      }
    }
  };

  request.onerror = function() {
    // request failed
  };
  formData = new FormData();
  console.log(table, key, field, value)
  if(key == '' && node.classList.contains('key')){
    formData.append('action', 'new');
  }
  else{
    formData.append('action', 'edit');
  }
  formData.append('table', table);
  formData.append('key', key);
  formData.append('field', field);
  formData.append('value', value);
  request.send(formData);
}

document.getElementsByClassName("add")[0].addEventListener("click", (e) => {addAddButton(e)});
document.getElementsByClassName("add")[1].addEventListener("click", (e) => {addAddButton(e)});
function addAddButton(e) {
  tbody = e.target.parentElement.parentElement.parentElement;
  let element = tbody.children[1].cloneNode(true);
  element.setAttribute('value', '');
  var children = Array.from(element.children);
  for(let i = 0; i < children.length - 1; i++){
    children[i].textContent = 'None';
    doubleClick(children[i]);
  }
  tbody.insertBefore(element, tbody.lastChild);
  element.getElementsByClassName('key')[0].setAttribute('key', '');
  var targLink = element.getElementsByClassName('key')[0];
  var clickEvent = document.createEvent ('MouseEvents');
  clickEvent.initEvent ('dblclick', true, true);
  targLink.dispatchEvent (clickEvent);
}