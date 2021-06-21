function onSubmit() {
  doInitMessage();
  // if (!isFile()) {
  //   doFileMessage();
  //   return false;
  // } else if (isFile() & !isModified()) {
  //   doModifiedMessage();
  //   return false;
  // }
  doProgressbar();
}

function doInitMessage() {
  var message = document.getElementById('validate-message');
  message.style.display = 'none';
  message.innerText = '';
}

function isModified() {
  if (!document.getElementById('ismodified')) {
    return false;
  }
  return JSON.parse(document.getElementById('ismodified').value.toLowerCase())
    ? true
    : false;
}

function doModifiedMessage() {
  var message = document.getElementById('validate-message');
  message.style.display = 'block';
  message.innerText = message.getAttribute('data-modified');
}

function isFile() {
  if (!document.querySelector('input[type=file]')) {
    return false;
  }
  return document.querySelector('input[type=file]').value.length ? true : false;
}

function doFileMessage() {
  var message = document.getElementById('validate-message');
  message.style.display = 'block';
  message.innerText = message.getAttribute('data-uploaded');
}

function onInput(element) {
  element.setAttribute('value', element.value);
  document.getElementById('isModified').value =
    element.value === element.getAttribute('data-older') ? 'False' : 'True';
}

function onFileInput(element) {
  document.getElementById('isModified').value = element.value.length
    ? 'True'
    : 'False';
}

function doProgressbar() {
  if (document.getElementById('p2')) {
    document.getElementById('p2').style.display = 'block';
  }
}
