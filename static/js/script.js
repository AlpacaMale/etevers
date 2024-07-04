// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll(".register-needs-validation");

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        var password = document.getElementById("password").value;
        var confirmPassword = document.getElementById("password-confirm").value;
        var passwordFeedback = document.getElementById("password-feedback");
        var passwordMismatch = document.getElementById("password-mismatch");

        // 초기화
        passwordFeedback.style.display = "none";
        passwordMismatch.style.display = "none";

        // 비밀번호가 입력되지 않은 경우
        if (!password) {
          passwordFeedback.style.display = "block";
          event.preventDefault();
          event.stopPropagation();
        }
        // 비밀번호가 일치하지 않는 경우
        else if (password !== confirmPassword && confirmPassword) {
          passwordMismatch.style.display = "block";
          event.preventDefault();
          event.stopPropagation();
        }

        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();

(function () {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();
