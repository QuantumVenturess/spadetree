$(document).ready(function() {
  // When typing in the state name field, update the city name source
  $(document).on('keyup', '.userEdit .stateName', function() {
    var url = $('.userEdit .cityName').data('original-source');
    var state = $(this).val().toLowerCase().replace(' ', '-');
    var newUrl = url + state;
    $('.userEdit .cityName').attr('data-autocomplete-source', newUrl);
    $('.userEdit .cityName').autocomplete({
      source: newUrl
    });
  });
});