$ ->
  $('.logout a').on('click', (e) ->
    $form = $(@).find('form')
    $form.submit()
  )