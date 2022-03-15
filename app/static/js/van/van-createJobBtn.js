$(function() {
    let createJobBtn = $('#createJobBtn');
    let vanNum = window.location.pathname.split('/')[2];
    $(createJobBtn).click(function () {
       window.location.replace('/jobs/' + vanNum);
    });
});