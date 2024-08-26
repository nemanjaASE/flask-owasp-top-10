document.addEventListener('DOMContentLoaded', function () {
  const addPostButton = document.getElementById('add-post-button');
  const requestAuthorButton = document.getElementById('request-author-button');

  if (addPostButton) {
    addPostButton.addEventListener('click', function () {
      window.location.href = this.getAttribute('data-href');
    });
  }

  if (requestAuthorButton) {
    requestAuthorButton.addEventListener('click', function () {
      window.location.href = this.getAttribute('data-href');
    });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  var flashMessages = document.querySelectorAll('.flash-message');
  flashMessages.forEach(function (msg) {
    alert(msg.textContent);
  });
});
