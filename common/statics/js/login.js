let isPasswordVisible = false;

function togglePasswordVisibility() {
  const passwordField = document.getElementById('password');
  const eyeIcon = document.getElementById('eye-password-show');
  const eyeSlashIcon = document.getElementById('eye-password-hide');

  if (isPasswordVisible) {
    passwordField.setAttribute('type', 'password');
    eyeIcon.style.display = 'block';
    eyeSlashIcon.style.display = 'none';
  } else {
    passwordField.setAttribute('type', 'text');
    eyeIcon.style.display = 'none';
    eyeSlashIcon.style.display = 'block';
  }
  isPasswordVisible = !isPasswordVisible;
}
