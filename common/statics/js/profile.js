document.addEventListener('DOMContentLoaded', function () {
  const editButton = document.getElementById('edit-button');
  const saveButton = document.getElementById('save-button');
  const cancelButton = document.getElementById('cancel-button');
  const inputs = document.querySelectorAll('#profile-form input');

  editButton.addEventListener('click', function () {
    inputs.forEach((input) => (input.readOnly = false));
    editButton.style.display = 'none';
    saveButton.style.display = 'inline-block';
    cancelButton.style.display = 'inline-block';
  });

  cancelButton.addEventListener('click', function () {
    inputs.forEach((input) => (input.readOnly = true));
    editButton.style.display = 'inline-block';
    saveButton.style.display = 'none';
    cancelButton.style.display = 'none';
  });
});
