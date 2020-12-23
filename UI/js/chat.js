function toggleUserDetails() {
  document.getElementById('container').classList.toggle('disable');
  document.getElementById('popup-user-detail').classList.toggle('hide');
}

function showBorder(element) {
  element.classList.add('border');
}

function hideBorder(element) {
  element.classList.remove('border');
}
