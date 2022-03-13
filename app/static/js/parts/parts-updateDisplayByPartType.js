$(function(){
  // Path to update van list
  const getPath = '/table/part_type_list/' + window.location.pathname.split('/')[3];
  ns.updatePart(getPath);
});