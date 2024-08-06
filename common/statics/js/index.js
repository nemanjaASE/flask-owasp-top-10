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
