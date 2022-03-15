$(function() {
    let createJobBtn = $('#createJobBtn');
    let vanNum = window.location.pathname.split('/')[2];
    $('form').off().on('click', createJobBtn, function () {
       window.location.replace('/jobs/' + vanNum);
    });
});