$(document).ready(function(){
    const getPath = '/table/vans_list/all';
  $(document).on('click', '.deleteMe', function(){
      if (window.confirm('Are you sure you want to delete?')) {
          let id = this.dataset.value;
          $.ajax({
           url: '/delete/van/',
           type: 'POST',
           data: 'Delete=' + id,
           success: function() {
               $("#mySpan").load(getPath);
           }
        });
      }
  });
});