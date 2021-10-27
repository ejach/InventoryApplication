// Implementation to make the 'hamburger' slide animation fire when sidenav-change is executed
$(document).ready(function() {
  $("#addVan").click(function() {
    $("#formElement").slideToggle(300, "swing");
  });
});