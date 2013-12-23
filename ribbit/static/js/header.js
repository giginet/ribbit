$(function() {
  return $('.logout a').on('click', function(e) {
    var $form;
    $form = $(this).find('form');
    return $form.submit();
  });
});
