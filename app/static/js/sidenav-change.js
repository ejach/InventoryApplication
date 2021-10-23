window.onload = function() {
  // Implementation to make the 'hamburger' menu animation fire upon clicking
  document.getElementById("container").addEventListener("click", function() {
      let x = document.getElementById('container');
      x.classList.toggle("change");
  });
}