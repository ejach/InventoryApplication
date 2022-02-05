$(function() {
    const getPath = '/table/jobs/' + window.location.pathname.split('/jobs/')[1];
    ns.createJob(getPath);
});