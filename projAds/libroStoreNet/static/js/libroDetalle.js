$(document).ready(function() {
  $('#cantidad').val('0')
  $('#decremento').click(function() {
    let currentValue = $('#cantidad').val();
    if (currentValue < 1 || isNaN(currentValue)) {
      $('#cantidad').val(0);
    }
      currentValue = parseInt($('#cantidad').val());
      if (currentValue >= 1) {
          $('#cantidad').val(currentValue - 1);
      }
  });

  $('#incremento').click(function() {
    let currentValue = $('#cantidad').val();
    if (currentValue < 1 || isNaN(currentValue)) {
      $('#cantidad').val(0);
    }
    currentValue = parseInt($('#cantidad').val());
      $('#cantidad').val(currentValue + 1);
  });
});