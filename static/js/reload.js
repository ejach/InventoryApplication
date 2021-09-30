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