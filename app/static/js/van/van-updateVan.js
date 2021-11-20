$(document).ready(function(){
  // Path to update van list
  const getPath = '/table/vans_list/all';
  // On click, execute the following
  $(document).on('click', '.updateMe', function(){
    let text;
    // ID to be updated
    let id = this.dataset.value;
    let vanNumber = prompt("Please enter the new van number:", "vanNumber");
    if (vanNumber == null || vanNumber === "") {
      alert('Blank input will not be accepted.');
    } else {
      text = 'id=' + id + '&van_number=' + vanNumber;
    }
    // Send our POST request
    $.ajax({
      url: '/update/van/',
      type: 'POST',
      data: text,
      success: function() {
        $("#mySpan").load(getPath);
      }
    });
  });
});