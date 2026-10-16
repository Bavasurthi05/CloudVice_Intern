
$(document).ready(function () {

    $("#registrationForm").submit(function (event) {

        event.preventDefault();

        let fullname = $("#fullname").val().trim();
        let email = $("#email").val().trim();
        let age = $("#age").val().trim();
        let gender = $("#gender").val();
        let course = $("#course").val();
        let password = $("#password").val();

        $("#message").removeAttr("style").text("");

        if (fullname === "") {
            showError("Please enter your full name!");
            return;
        }

        if (email === "") {
            showError("Please enter your email!");
            return;
        }

        let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            showError("Please enter a valid email address!");
            return;
        }

        if (age === "") {
            showError("Please enter your age!");
            return;
        }

        if (isNaN(Number(age)) || Number(age) <= 0) {
            showError("Age must be a valid positive number!");
            return;
        }

        if (!gender) {
            showError("Please select your gender!");
            return;
        }

        if (!course) {
            showError("Please select your course!");
            return;
        }

        if (password === "") {
            showError("Please enter your password!");
            return;
        }

        if (password.length < 6) {
            showError("Password must contain at least 6 characters!");
            return;
        }

        $("#message").css({
            "color": "green",
            "background-color": "#d4edda",
            "padding": "12px",
            "margin-top": "15px",
            "border-radius": "5px",
            "text-align": "center",
            "font-weight": "bold"
        }).text("✅ Registered successfully! 👍");

        this.reset();

    });

    function showError(message) {
        $("#message").css({
            "color": "red",
            "background-color": "#f8d7da",
            "padding": "12px",
            "margin-top": "15px",
            "border-radius": "5px",
            "text-align": "center",
            "font-weight": "bold"
        }).text("❌ " + message);
    }

});
