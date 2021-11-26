// Implementation to make the 'hamburger' slide animation fire when sidenav-change is executed
$(function() {
  $(".container").click(function() {
    $("#sidenav").slideToggle(300, "swing");
  });
});