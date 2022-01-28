$(function () {
    const getPath = '/table/users/default';
    ns.confirmAccount(getPath);
    ns.denyAccount(getPath);
    ns.deleteAccount(getPath);
    ns.makeUserAdmin(getPath);
});