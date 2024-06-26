function togglePasswordVisibility() {
  var passwordInput = document.getElementById('password');
  var eyePasswordShow = document.getElementById('eye-password-show');
  var eyePasswordHide = document.getElementById('eye-password-hide');

  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    eyePasswordShow.style.display = 'none';
    eyePasswordHide.style.display = 'inline-block';
  } else {
    passwordInput.type = 'password';
    eyePasswordShow.style.display = 'inline-block';
    eyePasswordHide.style.display = 'none';
  }
}

function togglePasswordConfirmVisibility() {
  var confirmInput = document.getElementById('password-confirm');
  var eyePasswordConfirmShow = document.getElementById(
    'eye-password-confirm-show'
  );
  var eyePasswordConfirmHide = document.getElementById(
    'eye-password-confirm-hide'
  );

  if (confirmInput.type === 'password') {
    confirmInput.type = 'text';
    eyePasswordConfirmShow.style.display = 'none';
    eyePasswordConfirmHide.style.display = 'inline-block';
  } else {
    confirmInput.type = 'password';
    eyePasswordConfirmShow.style.display = 'inline-block';
    eyePasswordConfirmHide.style.display = 'none';
  }
}

function updatePasswordStrength(password) {
  const result = zxcvbn(password);
  const guessesLog10 = result.guesses_log10;
  const score = result.score;

  const strengthMeter = document.getElementById('password-strength-meter');
  const strengthBar = strengthMeter.querySelector('.strength-bar');
  const strengthText = strengthMeter.querySelector('.strength-text');

  let color = '';
  let text = '';

  switch (score) {
    case 0:
      color = 'red';
      text = 'Password is too guessable!';
      break;
    case 1:
      color = 'orange';
      text = 'Password is very guessable!';
      break;
    case 2:
      color = 'yellow';
      text = 'Password is somewhat guessable!';
      break;
    case 3:
      color = 'greenyellow';
      text = 'Password is safely unguessable!';
      break;
    case 4:
      color = 'green';
      text = 'Password is very unguessable!';
      strengthBar.style.width = '100%';
      break;
    default:
      color = 'gray';
      text = 'Password Strength';
  }

  if (score < 4) {
    strengthBar.style.width = `${(guessesLog10 / 10) * 100}%`;
  }
  strengthBar.style.backgroundColor = color;
  strengthText.textContent = text;
}

function onPasswordChange() {
  const passwordInput = document.getElementById('password');

  if (passwordInput) {
    const password = passwordInput.value;
    updatePasswordStrength(password);
  }
}

const passwordInput = document.getElementById('password');
if (passwordInput) {
  passwordInput.addEventListener('input', onPasswordChange);
}
