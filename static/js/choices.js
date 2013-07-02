$(document).ready(function() {
  // Clicking on choose tutor will show new choice form
  $(document).on('click', '.userDetail .chooseTutor', function() {
    $('.newChoiceForm').show();
    return false;
  })
  // When clicking on an interest for the form, select it
  $(document).on('click', '.newChoiceForm .skillChoices a', function() {
    $('.skillToLearn h1').removeClass('invalid');
    $('.newChoiceForm .skillChoices a').removeClass('selected');
    $(this).addClass('selected');
    $('.newChoiceForm .skillPk').val($(this).data('value'));
    return false;
  });
  // When clicking on a day for the new choice form, select it
  $(document).on('click', '.newChoiceForm .dayChoices a', function() {
    $('.dayOfWeek h1').removeClass('invalid');
    $('.newChoiceForm .dayChoices a').removeClass('selected');
    $(this).addClass('selected');
    $('.newChoiceForm .dayFreePk').val($(this).data('value'));
    return false;
  });
  // When clicking on a hour for the new choice form, select it
  $(document).on('click', '.newChoiceForm .hourChoices a', function() {
    $('.hourOfDay h1').removeClass('invalid');
    $('.newChoiceForm .hourChoices a').removeClass('selected');
    $(this).addClass('selected');
    $('.newChoiceForm .hourFreePk').val($(this).data('value'));
    return false;
  });
  // Do not submit choice form if no skill, day, and hour selected
  $(document).on('submit', '.newChoiceForm form', function() {
    var skillVal    = $('.newChoiceForm .skillPk').val().length;
    var dayFreeVal  = $('.newChoiceForm .dayFreePk').val().length;
    var hourFreeVal = $('.newChoiceForm .hourFreePk').val().length;
    var messageVal  = $('.newChoiceForm .message textarea').last().val().length;
    if (!skillVal) {
      $('.skillToLearn h1').addClass('invalid');
    }
    if (!dayFreeVal) {
      $('.dayOfWeek h1').addClass('invalid');
    }
    if (!hourFreeVal) {
      $('.hourOfDay h1').addClass('invalid');
    }
    if (skillVal && dayFreeVal && hourFreeVal && !messageVal) {
      $('.newChoiceForm .message textarea').last().focus();
    }
    if (!skillVal || !dayFreeVal || !hourFreeVal || !messageVal) {
      return false
    }
  });
  // Clicking cancel on the new choice form hides it
  $(document).on('click', '.newChoiceForm .action a', function() {
    $('.newChoiceForm').hide();
    return false;
  });
  // Requests page, choice partials, choice actions
  // Clicking accept or deny
  $(document).on('click', '.choice .choiceActionForm button', function() {
    var form = $(this).closest('form');
    var action = $(this).val();
    var formData = form.serialize() + action;
    $.ajax({
      data: formData,
      type: form.attr('method'),
      url: form.attr('action'),
      success: function(response) {
        var pk = response.pk;
        $('#choice_' + pk + ' .choiceActionForm').html(
          response.choice_action_form);
        $('#choice_' + pk + ' .contactNumber').html(
          response.contact_number);
        $('#choice_' + pk + ' .requestStatus').html(
          response.request_status);
        // Update choice count and title count
        var choiceCount  = parseInt(response.choice_count);
        var titleCount   = parseInt(response.title_count);
        var currentTitle = $('title').text();
        if (choiceCount == 0) {
          choiceCount = '';
        }
        if (titleCount == 0) {
          var newTitleCount = currentTitle.replace(/\([\d]+\)/, '');
          $('.header .menu span').removeClass('red');
        }
        else {
          var newTitleCount = currentTitle.replace(/[\d]+/, titleCount);
        }
        $('.header #menu .choiceCount').text(choiceCount);
        $('title').text(newTitleCount);
      }
    });
    return false;
  });
});