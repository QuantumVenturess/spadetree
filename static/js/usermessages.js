$(document).ready(function() {
  // Reply form submission
  $(document).on('submit', '.replyMessageForm form', function() {
    var content = $('.replyMessageForm textarea:last');
    if (content.val().length > 0) {
      $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        success: function(response) {
          // Reload reply message form
          $('.replyMessageForm').html(response.reply_message_form);
          // Append new message at the bottom of user messages
          $('.userMessages').append(response.message_template);
          // Scroll to the bottom of the page
          $('html, body').animate({ scrollTop: $(document).height() }, 0);
          $('.replyMessageForm textarea:last').focus();
        }
      });
    }
    return false;
  });
});