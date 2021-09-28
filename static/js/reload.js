window.onload = function() {
    document.getElementById('refreshBtn').addEventListener("click", function() {
        const request = new XMLHttpRequest()
        const url = '/';
        request.open('GET', url);
        request.send();

        request.onload = (e) => {
            console.log(request.response)
        }
    })
}

// $("#refreshBtn").keyup(function(){
//     var text = $(this).val();
//
//     $.ajax({
//       url: "/",
//       type: "get",
//       data: {jsdata: text},
//       success: function(response) {
//         $("#myDiv").html(response);
//       },
//       error: function(xhr) {
//         //Do Something to handle error
//       }
//     });
// });