document
  .getElementById('add-post-button')
  .addEventListener('click', function () {
    window.location.href = this.getAttribute('data-href');
  });
