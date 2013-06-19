$(document).ready(function() {
  // Header menu
  $(document).on('mouseover', 'header .menu', function() {
    $(this).addClass('menuShow');
    $('#menu').show();
    return false;
  });
  $(document).on('mouseover', '#menu', function() {
    return false;
  });
  $(document).on('mouseover', function() {
    $('header .menu').removeClass('menuShow');
    $('#menu').hide();
  });
});