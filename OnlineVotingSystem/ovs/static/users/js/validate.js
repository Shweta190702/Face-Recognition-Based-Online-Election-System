$(document).ready(function () {
  $("#vid").keyup(function () {
    let vidNo = $("#vid").val();
    if (vidNo.length < 10) {
      $("#vidCheck").show();
    } else {
      $("#vidCheck").hide();
    }
  });

  $("#username").keyup(function () {
    let userName = $("#username").val();
    if (userName.length < 10) {
      $("#usernameCheck").show();
    } else {
      $("#usernameCheck").hide();
    }
  });

  $("#age").keyup(function () {
    var Age = $("#age").val();
    if (Age < 18) {
      $("#ageCheck").show();
    } else {
      $("#ageCheck").hide();
    }
  });

  $("#pass2").keyup(function () {
    let Paswd1 = $("#pass1").val();
    let Paswd2 = $("#pass2").val();
    if (Paswd1 != Paswd2) {
      $("#paswdCheck").show();
    } else {
      $("#paswdCheck").hide();
    }
  });

  $("#phone").keyup(function () {
    let Phone = $("#phone").val();
    if (Phone.length != 10) {
      $("#phoneCheck").show();
    } else {
      $("#phoneCheck").hide();
    }
  });
});
