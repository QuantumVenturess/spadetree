$(document).ready(function() {
  // Adding a skill
  $(document).on('click', '.userEdit .addSkillButton', function() {
    var form = $(this).closest('.userEdit .addSkill form');
    var interestName = $('.userEdit .addSkillInput');
    if (interestName.val().length > 0) {
      submitAddSkill(form);
    }
    return false;
  });
  // Deleting a skill
  $(document).on('submit', '.userEdit .skillDeleteForm form', function() {
    $.ajax({
      data: $(this).serialize(),
      type: $(this).attr('method'),
      url: $(this).attr('action'),
      success: function(response) {
        $('#skillDeleteForm_' + response.skill_pk).remove();
      }
    });
    return false;
  });
});

// Function for adding a skill
function submitAddSkill(form) {
  $.ajax({
    data: form.serialize(),
    type: form.attr('method'),
    url: form.attr('action'),
    success: function(response) {
      $('.userEdit .skillBox span').append(response.skill_delete_form);
      $('.userEdit .addSkill').html(response.skill_add_form);
      $('.userEdit .addSkillInput').focus();
    }
  });
}