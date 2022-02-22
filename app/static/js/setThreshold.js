$(function () {
    let getPath = '/table/display_part/' + window.location.pathname.split('/').pop();
    ns.updateThresh(getPath);
});