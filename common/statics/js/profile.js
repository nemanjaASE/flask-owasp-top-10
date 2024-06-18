document.getElementById('edit-button').onclick = function () {
  var inputs = document.querySelectorAll('#profile-form input');
  inputs.forEach((input) => (input.readOnly = false));
  document.getElementById('edit-button').style.display = 'none';
  document.getElementById('save-button').style.display = 'inline-block';
  document.getElementById('cancel-button').style.display = 'inline-block';
};

document.getElementById('cancel-button').onclick = function () {
  var inputs = document.querySelectorAll('#profile-form input');
  inputs.forEach((input) => (input.readOnly = true));
  document.getElementById('edit-button').style.display = 'inline-block';
  document.getElementById('save-button').style.display = 'none';
  document.getElementById('cancel-button').style.display = 'none';
};
