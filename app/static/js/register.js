window.addEventListener("load",function() {
    const newURL = '/login';
    const form = document.getElementById("registerForm");

    // Get the myForm element and assign it to a variable
    function registerPOST() {
        const XHR = new XMLHttpRequest();

        // Bind the FormData object and the form element
        const FD = new FormData(form);

        // On a successful submission, it gets an AJAX request to refresh the contents of the table
        XHR.addEventListener("load", function () {
            location.replace(newURL);
        });

        // Define what happens in case of error
        XHR.addEventListener("error", function () {
            console.log('POST request was not successful.');
        });

        // Set up our request
        XHR.open("POST", "/register");

        // The data sent is what the user provided in the form
        XHR.send(FD);
    }
// Replace the submit event with our sendData function
    document.getElementById('registerForm').addEventListener("submit", function (event) {
        let password = document.getElementById('password').value;
        let confPass = document.getElementById('confPassword').value;
        event.preventDefault();
        if (password === confPass && password && confPass) {
            registerPOST();
            form.reset();
        } else if (password !== confPass || !password || !confPass) {
            document.getElementById('error').innerHTML = 'Passwords do not match or are empty'
        }
    });
});