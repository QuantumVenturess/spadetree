$(document).ready(function() {
  // User edit page
  // state name field
  $('.userEdit .stateName').autocomplete({
    source: $('.userEdit .stateName').data('autocomplete-source')
  });
  // city name field
  $('.userEdit .cityName').autocomplete({
    source: $('.userEdit .cityName').data('autocomplete-source')
  });
});