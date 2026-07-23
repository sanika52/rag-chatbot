<?php

session_start();

require_once "../../config/database.php";

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    header("Location: ../register.php");
    exit;
}

$name = trim($_POST["name"]);
$email = trim($_POST["email"]);
$password = $_POST["password"];
$confirmPassword = $_POST["confirm_password"];
/**
 * Redirect back to register page with an error message
 * while preserving the entered name and email.
 */
function redirectWithError($message, $name, $email)
{
    $_SESSION["error"] = $message;
    $_SESSION["old_name"] = $name;
    $_SESSION["old_email"] = $email;

    header("Location: ../register.php");
    exit;
}

// Check for empty fields
if (empty($name) || empty($email) || empty($password) || empty($confirmPassword)) {
    redirectWithError("All fields are required.", $name, $email);
}

// Check if passwords match
if ($password !== $confirmPassword) {
    redirectWithError("Passwords do not match.", $name, $email);
}

// Validate name length
if (strlen($name) < 2 || strlen($name) > 100) {
    redirectWithError("Name must be between 2 and 100 characters.", $name, $email);
}

// Validate name characters
if (!preg_match("/^[A-Za-z][A-Za-z '-]*$/", $name)) {
    redirectWithError(
        "Name can only contain letters, spaces, hyphens and apostrophes.",
        $name,
        $email
    );
}

// Validate email
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    redirectWithError("Please enter a valid email address.", $name, $email);
}

// Validate password length
if (strlen($password) < 8 || strlen($password) > 64) {
    redirectWithError("Password must be between 8 and 64 characters.", $name, $email);
}

// Password must contain uppercase letter
if (!preg_match("/[A-Z]/", $password)) {
    redirectWithError("Password must contain at least one uppercase letter.", $name, $email);
}

// Password must contain lowercase letter
if (!preg_match("/[a-z]/", $password)) {
    redirectWithError("Password must contain at least one lowercase letter.", $name, $email);
}

// Password must contain a number
if (!preg_match("/[0-9]/", $password)) {
    redirectWithError("Password must contain at least one number.", $name, $email);
}

// Password must contain a special character
if (!preg_match('/[^a-zA-Z0-9]/', $password)) {
    redirectWithError("Password must contain at least one special character.", $name, $email);
}

// Check if email already exists
$sql = "SELECT id FROM users WHERE email = :email";

$stmt = $pdo->prepare($sql);
$stmt->execute([
    "email" => $email
]);

if ($stmt->fetch()) {
    redirectWithError("Email already exists.", $name, $email);
}

// Hash password
$passwordHash = password_hash($password, PASSWORD_DEFAULT);

// Insert user
$sql = "INSERT INTO users (name, email, password_hash)
        VALUES (:name, :email, :password_hash)";

$stmt = $pdo->prepare($sql);

$stmt->execute([
    "name" => $name,
    "email" => $email,
    "password_hash" => $passwordHash
]);

$_SESSION["success"] = "Registration successful! Please login.";

header("Location: ../login.php");
exit;