$(document).ready(function() {
  // Clicking on choose tutor will show new choice form
  $(document).on('click', '.userDetail .chooseTutor', function() {
    $('.newChoiceForm').show();
    return false;
  })
  // When clicking on an interest for the form, select it
  $(document).on('click', '.newChoiceForm .skillChoices a', function() {
    $('.newChoiceForm .skillChoices a').removeClass('selected');
    $(this).addClass('selected');
    $('.newChoiceForm .skillPk').val($(this).data('value'));
    $('.newChoiceForm .message textarea').focus();
    return false;
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