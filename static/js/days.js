$(document).ready(function() {
  // User edit, when clicking on a day
  $(document).on('submit', '.userEdit .dayHourBox form', function() {
    $(this).find('button').toggleClass('selected');
    $.ajax({
      data: $(this).serialize(),
      type: $(this).attr('method'),
      url: $(this).attr('action')
    });
    return false;
  });
});