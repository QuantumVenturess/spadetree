$(document).ready ->
  $(document).on 'click', '.pick button', ->
    form = 
      $(@).closest 'form'
    $.ajax 
      data: form.serialize()
      type: form.attr 'method'
      url : form.attr 'action'
      success: (response) ->
        $.ajax
          type: 'GET'
          url : '/u/tutorial'
          success: (response) ->
            $('.pick').remove()
            $('.content').html response.tutorial
            $('.tutorial #redirect').attr 'class', response.redirect
            $('.tutorial').fadeIn 100, ->
              $('.tutorial .insideBlocker').height $('.slide1 .inside').height()
              user = $('.tutorial #tutorialUserType').attr 'class'
              if user == 'tutee'
                $('.tutorial header .browse, 
                  .tutorial .search .field input').animate
                  borderColor: 'rgb(255, 26, 0)'
                  1000
              else
                $('.tutorial .slide1 input, 
                  .tutorial .aboutTutorTutorial').animate
                  borderColor: 'rgb(255, 26, 0)'
                  1000
    no