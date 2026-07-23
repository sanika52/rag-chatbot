// ============================
// Get Elements
// ============================

const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirmPassword");

const nameMessage = document.getElementById("nameMessage");
const emailMessage = document.getElementById("emailMessage");
const confirmMessage = document.getElementById("confirmMessage");

const registerBtn = document.getElementById("registerBtn");

const togglePassword = document.getElementById("togglePassword");
const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");

// Password checklist
const lengthCheck = document.getElementById("length");
const upperCheck = document.getElementById("upper");
const lowerCheck = document.getElementById("lower");
const numberCheck = document.getElementById("number");
const specialCheck = document.getElementById("special");

// ============================
// Validation Flags
// ============================

let validName = false;
let validEmail = false;
let validPassword = false;
let passwordsMatch = false;

// ============================
// Enable / Disable Register
// ============================

function updateRegisterButton() {

    registerBtn.disabled = !(
        validName &&
        validEmail &&
        validPassword &&
        passwordsMatch
    );

}

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

toggleConfirmPassword.addEventListener("click", function () {

    if (confirmPasswordInput.type === "password") {
        confirmPasswordInput.type = "text";
        this.classList.replace("fa-eye", "fa-eye-slash");
    }
    else {
        confirmPasswordInput.type = "password";
        this.classList.replace("fa-eye-slash", "fa-eye");
    }

});

// ============================
// Name Validation
// ============================

nameInput.addEventListener("input", function () {

    const name = this.value.trim();

    const regex = /^[A-Za-z][A-Za-z '-]*$/;

    if (name.length < 2) {

        validName = false;

        nameMessage.innerHTML =
"<span class='validation-error'>Name must be at least 2 characters.</span>";

    }
    else if (!regex.test(name)) {

        validName = false;

        nameMessage.innerHTML =
"<span class='validation-error'>Only letters, spaces, hyphens and apostrophes allowed.</span>";
    }
    else {

        validName = true;

        nameMessage.innerHTML =
"<span class='validation-success'>✓ Name looks good.</span>";
    }

    updateRegisterButton();

});

// ============================
// Email Validation
// ============================

emailInput.addEventListener("input", function () {

    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (regex.test(this.value.trim())) {

        validEmail = true;

        emailMessage.innerHTML =
"<span class='validation-success'>✓ Valid email.</span>";
    }
    else {

        validEmail = false;

        emailMessage.innerHTML =
"<span class='validation-error'>Invalid email address.</span>";
    }

    updateRegisterButton();

});

// ============================
// Password Validation
// ============================

passwordInput.addEventListener("input", function () {

    const password = this.value;

    const hasLength = password.length >= 8;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[^A-Za-z0-9]/.test(password);

    lengthCheck.className = hasLength ? "valid" : "invalid";
lengthCheck.innerHTML =
(hasLength ? "✅" : "❌") + " At least 8 characters";
    upperCheck.className = hasUpper ? "valid" : "invalid";
upperCheck.innerHTML =
(hasUpper ? "✅" : "❌") + " One uppercase letter";
    lowerCheck.className = hasLower ? "valid" : "invalid";
lowerCheck.innerHTML =
(hasLower ? "✅" : "❌") + " One lowercase letter";
    numberCheck.className = hasNumber ? "valid" : "invalid";
numberCheck.innerHTML =
(hasNumber ? "✅" : "❌") + " One number";
    specialCheck.className = hasSpecial ? "valid" : "invalid";
specialCheck.innerHTML =
(hasSpecial ? "✅" : "❌") + " One special character";
    validPassword =
        hasLength &&
        hasUpper &&
        hasLower &&
        hasNumber &&
        hasSpecial;

    checkPasswordsMatch();

    updateRegisterButton();

});

// ============================
// Confirm Password Validation
// ============================

confirmPasswordInput.addEventListener("input", function () {

    checkPasswordsMatch();

    updateRegisterButton();

});

// ============================
// Check Password Match
// ============================

function checkPasswordsMatch() {

    if (confirmPasswordInput.value === "") {

        passwordsMatch = false;

        confirmMessage.innerHTML = "";

        return;

    }

    if (passwordInput.value === confirmPasswordInput.value) {

        passwordsMatch = true;

        confirmMessage.innerHTML =
"<span class='validation-success'>✓ Passwords match.</span>";
    }
    else {

        passwordsMatch = false;

        confirmMessage.innerHTML =
"<span class='validation-error'>Passwords do not match.</span>";
    }

}

// ============================
// Initial State
// ============================

updateRegisterButton();