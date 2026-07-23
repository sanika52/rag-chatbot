// ============================
// Get Elements
// ============================

const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

const emailMessage = document.getElementById("emailMessage");
const passwordMessage = document.getElementById("passwordMessage");

const togglePassword = document.getElementById("togglePassword");

const loginBtn = document.getElementById("loginBtn");

// ============================
// Validation Flags
// ============================

let validEmail = false;
let validPassword = false;

// ============================
// Enable / Disable Login Button
// ============================

function updateLoginButton() {

    loginBtn.disabled = !(validEmail && validPassword);

}

// ============================
// Email Validation
// ============================

emailInput.addEventListener("input", function () {

    const email = this.value.trim();

    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (email === "") {

        validEmail = false;

        emailMessage.innerHTML = "";

    }
    else if (regex.test(email)) {

        validEmail = true;

        emailMessage.innerHTML =
            "<span class='validation-success'>✓ Valid email address.</span>";

    }
    else {

        validEmail = false;

        emailMessage.innerHTML =
            "<span class='validation-error'>Invalid email address.</span>";

    }

    updateLoginButton();

});

// ============================
// Password Validation
// ============================

passwordInput.addEventListener("input", function () {

    if (this.value.length > 0) {

        validPassword = true;

        passwordMessage.innerHTML = "";

    }
    else {

        validPassword = false;

        passwordMessage.innerHTML =
            "<span class='validation-error'>Password cannot be empty.</span>";

    }

    updateLoginButton();

});

// ============================
// Toggle Password Visibility
// ============================

togglePassword.addEventListener("click", function () {

    if (passwordInput.type === "password") {

        passwordInput.type = "text";
        this.classList.replace("fa-eye", "fa-eye-slash");

    }
    else {

        passwordInput.type = "password";
        this.classList.replace("fa-eye-slash", "fa-eye");

    }

});

// ============================
// Initial State
// ============================

updateLoginButton();