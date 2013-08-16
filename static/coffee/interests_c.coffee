$(document).ready ->
  $('.interestList .search input').keyup ->
    clearSearch = $('.interestList .search .cancel')
    text = $(@).val()
    if text.length > 0
      clearSearch.show()
    else
      clearSearch.hide()
  $(document).on 'click', '.interestList .search .cancel', ->
    form        = $('.interestList .search form')
    searchField = $('.interestList .search input')
    $.ajax
      type: form.attr('method')
      url : js_url form.attr('action')
      success: (response) ->
        $('.interestList .results').html response.browse_results
    searchField.val('')
    searchField.focus()
    $(@).hide()
    no