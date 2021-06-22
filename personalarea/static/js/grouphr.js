$(function () {

  $(".js-create-grouphr").click(function () {
    $.ajax({
      url: 'grouphr_create/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  });

});