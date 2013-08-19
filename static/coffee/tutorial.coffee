$(document).ready ->
  animateBorder = (e) ->
    e.animate
      borderColor: 'rgb(255, 26, 0)'
      1000
  animateBorderBack = (e) ->
    e.animate
      borderColor: 'transparent'
      1000
  resizeInsideBlockerHeightForSlide1 = ->
    $('.tutorial .insideBlocker').height $('.slide1 .inside').height()
  resizeInsideBlockerHeightForSlide2 = ->
    $('.tutorial .insideBlocker').height $('.slide2 .inside').height()
  resizeInsideBlockerHeightForSlide3 = ->
    $('.tutorial .insideBlocker').height $('.slide3 .inside').height()
  # clicking next on slide 1
  $(document).on 'click', '.tutorial .slide1 .next', ->
    user = $('.tutorial #tutorialUserType').attr 'class'
    if user == 'tutee'
      animateBorderBack $('.tutorial header .browse, 
        .tutorial .search .field input')
    else
      animateBorderBack $('.tutorial .slide1 input, 
        .tutorial .aboutTutorTutorial')
    $('.slide1').fadeOut 100, ->
      $('.slide2').fadeIn 100, ->
        if user == 'tutee'
          animateBorder $('.tutorial .userDetail .top .chooseTutor')
        else
          animateBorder $('.tutorial header .browse, 
            .tutorial .search .field input')
        resizeInsideBlockerHeightForSlide2()
    no

  # Choose Tutor button
  $(document).on 'click', '.tutorial .slide2 .back', ->
    user = $('.tutorial #tutorialUserType').attr 'class'
    if user == 'tutee'
      animateBorderBack $('.tutorial .userDetail .top .chooseTutor')
    else
      animateBorderBack $('.tutorial header .browse, 
        .tutorial .search .field input')
    $('.slide2').fadeOut 100, ->
      $('.slide1').fadeIn 100, ->
        if user == 'tutee'
          animateBorder $('.tutorial header .browse, 
            .tutorial .search .field input')
        else
          animateBorder $('.tutorial .slide1 input, 
            .tutorial .aboutTutorTutorial')
        resizeInsideBlockerHeightForSlide1()
    no
  $(document).on 'click', '.tutorial .slide2 .next', ->
    user = $('.tutorial #tutorialUserType').attr 'class'
    if user == 'tutee'
      animateBorderBack $('.tutorial .userDetail .top .chooseTutor')
    else
      animateBorderBack $('.tutorial header .browse, 
        .tutorial .search .field input')
    $('.slide2').fadeOut 100, ->
      $('.slide3').fadeIn 100, ->
        if user == 'tutee'
          animateBorder $('.tutorial .slide3 input')
        else
          animateBorder $('.tutorial .choices button')
        resizeInsideBlockerHeightForSlide3()
    no

  # Set date and place
  $(document).on 'click', '.tutorial .slide3 .back', ->
    user = $('.tutorial #tutorialUserType').attr 'class'
    if user == 'tutee'
      animateBorderBack $('.tutorial .slide3 input')
    else
      animateBorderBack $('.tutorial .choices button')
    $('.slide3').fadeOut 100, ->
      $('.slide2').fadeIn 100, ->
        if user == 'tutee'
          animateBorder $('.tutorial .userDetail .top .chooseTutor')
        else
          animateBorder $('.tutorial header .browse, 
            .tutorial .search .field input')
        resizeInsideBlockerHeightForSlide2()
    no
  $(document).on 'click', '.tutorial .slide3 .next', ->
    $('.tutorial').fadeOut 100
    redirect = $('.tutorial #redirect').attr 'class'
    if not redirect
      redirect = ''
    window.location.href = redirect
    no