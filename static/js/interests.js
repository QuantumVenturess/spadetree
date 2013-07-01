$(document).ready(function() {
  // Browse
  $(document).on('keyup', '.interestList .search input', function(event) {
    if ($.inArray(event.keyCode, [13, 37, 38, 39, 40]) == -1) {
      var form = $(this).closest('form');
      $.ajax({
        data: { q: $(this).val() },
        type: form.attr('method'),
        url: js_url(form.attr('action')),
        success: function(response) {
          $('.interestList .results').html(response.browse_results);
        }
      });
    }
  });
  // Browse submit does nothing
  $(document).on('submit', '.interestList .search form', function() {
    $.ajax({
      data: $(this).serialize(),
      type: $(this).attr('method'),
      url: js_url($(this).attr('action')),
      success: function(response) {
        $('.interestList .results').html(response.browse_results);
      }
    });
    return false;
  });
  // When clicking on a browse result, ajax interest detail tutors
  $(document).on('click', '.interestList .group .interestNameLink', function() {
    var tutorsInsert = $(this).siblings('.tutorsInsert');
    if ($(this).hasClass('show')) {
      $(this).removeClass('show');
      tutorsInsert.hide();
    }
    else {
      $(this).addClass('show');
      tutorsInsert.show();
      // If there is nothing
      if (tutorsInsert.children().length == 0) {
        // Add spinner
        var browseSpinner = $(this).children('.browseSpinner');
        var spinner = new Spinner().spin();
        browseSpinner.prepend(spinner.el);
        // Ajax tutors into interest
        $.ajax({
          type: 'GET',
          url: $(this).attr('href'),
          success: function(response) {
            var pk = response.pk;
            $('.interestList #interest_' + pk + ' .tutorsInsert').html(
              response.tutors);
            // Remove spinner
            browseSpinner.remove();
            // Lazy load
            $('.lazy').lazyload({
              event: 'load',
              failure_limit: 50
            });
          }
        });
      }
    }
    return false;
  });
  // Search
  $(document).on('keyup', '.userEdit .addSkillInput', function(event) {
    if ($.inArray(event.keyCode, [13, 37, 38, 39, 40]) == -1) {
      $('.userEdit .interestResults').show();
      $.ajax({
        data: { q: $(this).val() },
        type: 'GET',
        url: $(this).data('autocomplete-source'),
        success: function(response) {
          $('.userEdit .interestResults').html(response.results);
          chosen = '';
        }
      });
    }
  });
  // When hovering over an autocomplete result, add selected class
  $(document).on('mouseover', '.userEdit .interestResults a', function() {
    var i = $(this).index();
    $('.userEdit .interestResults a').removeClass('selected');
    $(this).addClass('selected');
    chosen = i;
  });
  // Clicking the document will hide autocomplete results
  $(document).on('click', document, function(event) {
    $('.userEdit .interestResults').hide();
  });
  // Clicking on the add skill input will return false and show results
  $(document).on('click', '.userEdit .addSkillInput', function() {
    if ($('.userEdit .interestResults li').length > 0) {
      $('.userEdit .interestResults').show();
    }
    return false;
  });
  // Submitting the form will return false
  $(document).on('submit', '.userEdit .addSkill form', function() {
    return false;
  });
  // Clicking on an autocomplete result will submit the form
  $(document).on('click', '.userEdit .interestResults a', function() {
    var form = $(this).closest('.addSkill form');
    var name = $.trim($(this).text());
    $('.userEdit .addSkillInput').val(name);
    $('.userEdit .interestResults').hide();
    // Submit the form
    submitAddSkill(form);
    return false;
  });
  // Pressing enter while an autocomplete result is selected will submit form
  $(document).on('keyup', '.userEdit .addSkillInput', function(event) {
    if (event.keyCode == 13) {
      var form = $(this).closest('.addSkill form');
      var selected = $('.userEdit .interestResults .selected');
      var addSkillInput = $('.userEdit .addSkillInput');
      if (addSkillInput.val().match(/^[0-9A-Za-z _-]+$/)) {
        // If there is one result that is selected
        if (selected.length == 1) {
          addSkillInput.val($.trim(selected.text()));
        }
        submitAddSkill(form);
      }
      return false;
    }
  });
  // Keyboard navigation for search results
  $(document).on('keydown', '.userEdit .addSkillInput', function(event) {
    if ($('.userEdit .interestResults').is(':visible')) {
      if ($.inArray(event.keyCode, [38, 40]) != -1) {
        // If arrow up is pressed
        if (event.keyCode == 38) {
          if (chosen === '') {
            chosen = 0;
          }
          else if (chosen > 0) {
            chosen--;
          }
        }
        // If arrow down is pressed
        if (event.keyCode == 40) {
          if (chosen === '') {
            chosen = 0;
          }
          else if ((chosen + 1) < $('.userEdit .interestResults li').length) {
            chosen++;
          }
        }
        $('.userEdit .interestResults a').removeClass('selected');
        $('.userEdit .interestResults a:eq(' + chosen + ')').addClass(
          'selected');
        return false;
      }
    }
  });
});