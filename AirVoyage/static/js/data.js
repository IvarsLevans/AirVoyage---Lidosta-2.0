// document.getElementById("airports").addEventListener("click", (e) => {
//   addDelete(e)
// })
// document.getElementById("airplanes").addEventListener("click", (e) => {
//   addDelete(e)
// })
tables = [document.getElementById("airports"), document.getElementById("airplanes"), document.getElementById("flights")]
for (let i = 0; i < tables.length; i++){
  tables[i].addEventListener("click", (e) => {addDelete(e)});
}
function addDelete(e){
  button = e.target;
  if(button.classList.contains('delete')) {
    row = e.target.parentElement.parentElement
    key = row.getElementsByClassName('key')[0].getAttribute('key');

    url = '/data';
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.onload = function() {
      if(request.responseText === "permissionDenied"){
        document.location.href = '../'
      }
      else{
        row.parentElement.removeChild(row);
      }
    };

    request.onerror = function() {
      // request failed
    };
    formData = new FormData();
    formData.append('action', 'delete');
    formData.append('table', row.parentElement.parentElement.id);
    formData.append('key', key);
    request.send(formData);
  }
  else if (button.classList.contains('finish')){
    //table, key, fieldName, value  
    
    row = e.target.parentElement.parentElement
    key = row.getElementsByClassName('key')[0].getAttribute('key');

    url = '/data';
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.onload = function() {
      if(request.responseText == 'success'){
        if(button.textContent == 'Enable'){
          button.textContent = 'Disable';
        }
        else{
          button.textContent = 'Enable';
        }
      }
    };

    request.onerror = function() {
      // request failed
    };
    formData = new FormData();
    formData.append('action', 'edit');
    formData.append('table', row.parentElement.parentElement.id);
    formData.append('key', key);
    formData.append('field', button.parentElement.getAttribute('value'));
    if(button.textContent == 'Enable'){
      formData.append('value', 'false');
    }
    else{
      formData.append('value', 'true');
    }
    request.send(formData);
  }
}

let editedFields = new FormData();
let editedAirportsAbrriviations = '';
function doubleClick(node) {
  if(node.classList.contains('editable')) {
    node.ondblclick=function() {

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
    if(request.responseText != 'success'){
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
  if(key == '' && node.classList.contains('key')){
    formData.append('action', 'add');
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

// document.getElementsByClassName("add")[0].addEventListener("click", (e) => {addAddButton(e)});
// document.getElementsByClassName("add")[1].addEventListener("click", (e) => {addAddButton(e)});
addButtons = document.getElementsByClassName("add");
for (let i = 0; i < addButtons.length; i++){
  addButtons[i].addEventListener("click", (e) => {addAddButton(e)});
}
function addAddButton(e) {
  tbody = e.target.parentElement.parentElement.parentElement;
  // let element = tbody.children[1].cloneNode(true);
  let element = createRow(e.target.parentElement.parentElement.parentElement.parentElement.id)
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
function createRow(tableId) {
  if (tableId == 'airports'){
    return document.getElementById('exampleRows').children[0].children[0].cloneNode(true);
  }
  else if (tableId == 'airplanes'){
    return document.getElementById('exampleRows').children[0].children[1].cloneNode(true);
  }
  else if (tableId == 'flights'){
    return document.getElementById('exampleRows').children[0].children[2].cloneNode(true);
  }
  return;
}
