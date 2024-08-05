document.addEventListener('DOMContentLoaded', function () {
  const inputs = document.querySelectorAll('.otp-input');
  inputs.forEach((input, index) => {
    input.addEventListener('input', () => {
      if (input.value.length === 1 && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }
    });
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Backspace' && input.value === '' && index > 0) {
        inputs[index - 1].focus();
      }
    });
  });

  // Countdown timer logic
  const otpGeneratedTimeStr =
    document.querySelector('.container').dataset.otpGeneratedTime;
  const otpGeneratedTime = new Date(otpGeneratedTimeStr);
  console.log(otpGeneratedTime);
  const loginUrl = document.querySelector('.container').dataset.loginUrl;
  const otpValidityPeriod = 60;
  const countdown = document.getElementById('time-left');
  let countdownInterval;

  function updateCountdown() {
    const now = new Date();
    const timeElapsed = (now - otpGeneratedTime) / 1000;
    const timeLeft = Math.max(0, otpValidityPeriod - timeElapsed);
    countdown.textContent = Math.floor(timeLeft);

    if (timeLeft <= 0) {
      clearInterval(countdownInterval);
      window.location.href = loginUrl;
    }
  }
  updateCountdown();
  countdownInterval = setInterval(updateCountdown, 1000);
});
