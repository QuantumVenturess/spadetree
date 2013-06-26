$(document).ready(function() {
  // Masonry
  var container = $('.tutorReviews');
  container.show();
  // Initialize
  container.masonry({
    gutterWidth: 20,
    isAnimated: false,
    itemSelector: '.review'
  });
  // Clicking on a thumb will make it selected
  $(document).on('click', '.newReviewForm .action span', function() {
    $('.newReviewForm .action span').removeClass('selected');
    $(this).addClass('selected');
    if ($(this).hasClass('thumbsUp')) {
      $('.newReviewForm .positive').val(1);
    }
    else {
      $('.newReviewForm .positive').val(0);
    }
    return false;
  });
  // When key upping on the textarea, re-position reviews
  $(document).on('keyup', '.newReviewForm textarea', function() {
    container.masonry();
  });
  // Submitting the form via ajax
  $(document).on('submit', '.newReviewForm form', function() {
    var content = $('.newReviewForm .newReviewFormContent:last');
    if (content.val().length > 0) {
      var url = js_url($(this).attr('action'));
      $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: url,
        success: function(response) {
          // Refresh review form
          $('.newReviewForm').html(response.new_review_form);
          // Prepend review
          $('.tutorReviews .prepend').prepend(response.review_template);
          container.masonry('reload');
          // Autoresize
          $('textarea').autoResize();
          // Lazy load
          $('.lazy').lazyload({
            event: 'load',
            failure_limit: 50
          });
        }
      });
    }
    return false;
  });
});