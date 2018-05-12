$(document).ready(function() {
  $(".datetimepicker").datetimepicker({
    format: "m/d/Y g:i A",
    formatTime: "g:i A",
    ampm: true,
    step: 30,
    defaultSelect: false,
    allowBlank: false,
    validateOnBlur: false
  });
});
