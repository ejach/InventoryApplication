$(function (){
   let createJobBtn = $('.createJobBtn');
   let pathName = window.location.pathname.split('/vans/')[1];
   $(createJobBtn).off().click(function (e) {
      e.preventDefault();
      // Redirect to the jobs page according to the van that is currently selected
      window.location.replace('/jobs/' + pathName);
   });
});