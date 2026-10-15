
        document.getElementById("myForm").addEventListener("submit", function(event) {

            event.preventDefault();

            let name = document.getElementById("name").value.trim();
            let email = document.getElementById("email").value.trim();
            let age = document.getElementById("age").value;
            let password = document.getElementById("pass").value;
            if (name === "" || email === "" || age === "" || password === "") {
        alert("Please fill all fields!");
        return;
    }

            if (name === "") {
                alert("Please enter your name!");
                document.getElementById("name").focus();
                return;
            }

            if (!/^[A-Za-z0-9]+$/.test(name)) {
                alert("Name must contain only letters and numbers!");
                document.getElementById("name").focus();
                return;
            }

          
            let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailPattern.test(email)) {
                alert("Please enter a valid email address!");
                document.getElementById("email").focus();
                return;
            }

            
            if (age === "" || Number(age) < 18 || Number(age) > 100) {
                alert("Age must be between 18 and 100!");
                document.getElementById("age").focus();
                return;
            }

            
            if (password.length < 8) {
                alert("Password must contain at least 8 characters!");
                document.getElementById("pass").focus();
                return;
            }

            if (!/[A-Z]/.test(password)) {
                alert("Password must contain an uppercase letter!");
                document.getElementById("pass").focus();
                return;
            }

            if (!/[a-z]/.test(password)) {
                alert("Password must contain a lowercase letter!");
                document.getElementById("pass").focus();
                return;
            }

            if (!/[0-9]/.test(password)) {
                alert("Password must contain at least one number!");
                document.getElementById("pass").focus();
                return;
            }

            alert("All fields are valid!");

            document.getElementById("message").textContent =
        "Logged in successfully, " + name + "!";

        document.getElementById("message").style.color = "green";

        });