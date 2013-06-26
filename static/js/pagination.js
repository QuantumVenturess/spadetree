$(document).ready(function() {
  $(window).scroll(function() {
    var next = $('.endlessPagination .next').attr('href');
    if (next && $(window).scrollTop() >
      $(document).height() - ($(window).height() + 500)) {
      $('.endlessPagination').remove();
      $.ajax({
        type: 'GET',
        url: next,
        success: function(response) {
          $(response.selector).append(response.results);
          $('.content').append('<span class="endlessPagination">' + 
            response.pagination + '</span>');
          // Masonry
          $('.tutorReviews').masonry('reload');
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
  });
});