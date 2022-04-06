$(function() {
    const getPath = '/table/part_store_list/' + window.location.pathname.split('/')[3];
    ns.addPart(getPath);
});