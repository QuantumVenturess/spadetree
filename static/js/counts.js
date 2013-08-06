$(document).ready(function() {
  // Notifications
  $.ajax({
    type: 'GET',
    url: '/n/count.json',
    success: function(response) {
      var count = parseInt(response.count);
      if (count > 0) {
        $('.notificationCount').text(count);
      }
    }
  });
  // Requests
  $.ajax({
    type: 'GET',
    url: '/c/count.json',
    success: function(response) {
      var count = parseInt(response.count);
      if (count > 0) {
        $('.choiceCount').text(count);
      }
    }
  });
  // User messages
  $.ajax({
    type: 'GET',
    url: '/m/count.json',
    success: function(response) {
      var count = parseInt(response.count);
      if (count > 0) {
        $('.messageCount').text(count);
      }
    }
  });
  // Title count
  $.ajax({
    type: 'GET',
    url: '/u/title-count.json',
    success: function(response) {
      var count = parseInt(response.count);
      if (count > 0) {
        $('title').prepend('(' + count + ') ');
        $('header .menu span').addClass('red');
      }
    }
  });
});