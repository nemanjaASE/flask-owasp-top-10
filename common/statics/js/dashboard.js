document.addEventListener('DOMContentLoaded', function () {
  var tabs = document.querySelectorAll('.tab');
  var tabContents = document.querySelectorAll('.tab-content');
  console.log('Remove');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      tabs.forEach(function (t) {
        t.classList.remove('active');
      });

      tab.classList.add('active');

      tabContents.forEach(function (tc) {
        tc.classList.remove('active');
      });

      var contentId = tab.getAttribute('data-tab');
      document.getElementById(contentId).classList.add('active');
    });
  });
});
