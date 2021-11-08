window.addEventListener("load",function() {
    const form = document.getElementById("loginForm");

    // Get the myForm element and assign it to a variable
    const loginPOST = () => {
        const XHR = new XMLHttpRequest();

        // Bind the FormData object and the form element
        const FD = new FormData(form);

        // On a successful submission, it gets an AJAX request to refresh the contents of the table
        XHR.addEventListener("load", function () {
            location.reload()
        });

        // Define what happens in case of error
        XHR.addEventListener("error", function () {
            console.log('POST request was not successful.');
        });

        // Set up our request
        XHR.open("POST", "/login");

        // The data sent is what the user provided in the form
        XHR.send(FD);
    };
// Replace the submit event with our sendData function
    document.getElementById('loginForm').addEventListener("submit", function (event) {
        event.preventDefault();
        loginPOST();
        form.reset();
    });
});