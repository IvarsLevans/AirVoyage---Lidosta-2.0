
isEditing = false;
document.addEventListener('click', (e) =>{
  button = e.target;
  if(button.classList.contains('edit')){
    if(isEditing){
      alert('Already editing a row.');
      return;
    }
    row = button.parentElement.parentElement;
    row.style['display'] = 'none';
    tbody = row.parentElement;
    template = tbody.getElementsByClassName('editTemplate')[0].cloneNode(true);
    template.style['display'] = 'table-row';
    template.classList = [];
    // -2 to ignore apply, cancel button
    for(let i = 0; i < template.children.length - 2; i++){
      td = template.children[i];
      if(td.classList.contains('uneditable')){
        td.textContent = row.children[i].textContent;
      }
      else{
        input = td.children[0];
        if(input.type == 'datetime-local'){
          let temp = row.children[i].textContent.split(' ');
          let dateTemp = temp[0].split('.');
          input.value = dateTemp[2] + '-' + dateTemp[1] + '-' + dateTemp[0] + 'T' + temp[1];
        }
        else{
          input.value = row.children[i].textContent;
        }
      }
    }
    tbody.insertBefore(template, row);
    isEditing = true;
  }
  else if(button.classList.contains('apply')){
    row = button.parentElement.parentElement;
    url = '/data';
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.onload = function() {
      
      if(request.responseText == "success"){
        location.reload()
      }
      else{
        alert(request.responseText);
        console.log("error" + request.responseText);
      }
    };
    formData = new FormData();
    if (row.getAttribute('mode') == 'add'){
      formData.append('action', 'addRow');
    }
    else{
      formData.append('action', 'editRow');
    }
    formData.append('table', row.parentElement.parentElement.getAttribute('name'));
    let length = 0;
    // -2 to ignore apply, cancel button
    for(let i = 0; i < row.children.length - 2; i++){
      if(!row.children[i].classList.contains('uneditable')){
        formData.append('fieldName' + (i).toString(), row.children[i].getAttribute('fieldName'));
        formData.append('value' + i.toString(), row.children[i].children[0].value);
        length += 1;
      }
      if(row.children[i].classList.contains('key')){
        formData.append('key', row.nextElementSibling.children[i].textContent);
        formData.append('keyFieldName', row.children[i].getAttribute('fieldName'));
      }
    }
    formData.append('fieldCount', length);
    request.send(formData);
  }
  else if (button.classList.contains('addRow')){
    if(isEditing){
      alert('Already editing a row.');
      return;
    }
    let tbody = button.previousElementSibling.children[0];
    template = tbody.getElementsByClassName('editTemplate')[0].cloneNode(true);
    template.style['display'] = 'table-row';
    template.setAttribute('mode', 'add')
    tbody.insertBefore(template, tbody.getElementsByClassName('editTemplate')[0])
    isEditing = true;
  }
  else if (button.classList.contains('delete')){
    row = button.parentElement.parentElement;
    table = row.parentElement.parentElement;
    key = '';
    template = row.parentElement.getElementsByClassName('editTemplate')[0];
    for(let i = 0; i < template.children.length - 2; i++){
      if(template.children[i].classList.contains('key')){
        key = row.children[i].textContent;
      }
    }
    url = '/data';
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.onload = function() {
      
      if(request.responseText == "success"){
        location.reload()
      }
      else{
        console.log("error" + request.responseText + '.');
      }
    };
    formData = new FormData();
    formData.append('action', 'delete');
    formData.append('table', table.getAttribute('name'));
    formData.append('key', key);
    request.send(formData);
  }
  else if (button.classList.contains('cancel')){
    location.reload();
  }
})
