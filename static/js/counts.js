$(document).ready(function() {
  // Notifications
  $.ajax({
    type: 'GET',
    url: '/n/count.json',
    success: function(response) {
      if (response > 0) {
        $('.notificationCount').text(response);
      }
    }
  });
  // Requests
  $.ajax({
    type: 'GET',
    url: '/c/count.json',
    success: function(response) {
      if (response > 0) {
        $('.choiceCount').text(response);
      }
    }
  });
  // User messages
  $.ajax({
    type: 'GET',
    url: '/m/count.json',
    success: function(response) {
      if (response > 0) {
        $('.messageCount').text(response);
      }
    }
  });
  // Title count
  $.ajax({
    type: 'GET',
    url: '/u/title-count.json',
    success: function(response) {
      if (response > 0) {
        $('title').prepend('(' + response + ') ');
        $('header .menu span').addClass('red');
      }
    }
  });
});