<?php

session_start();

require_once "../../config/database.php";

// Allow only POST requests
if ($_SERVER["REQUEST_METHOD"] !== "POST") {

    header("Location: ../login.php");
    exit;
}

// Get form data
$email = trim($_POST["email"]);
$password = trim($_POST["password"]);

// Validate input
if (empty($email) || empty($password)) {

    $_SESSION["error"] = "Please enter email and password.";

    header("Location: ../login.php");
    exit;
}

// Find the user by email
$sql = "SELECT * FROM users WHERE email = :email";

$stmt = $pdo->prepare($sql);
$stmt->execute([
    "email" => $email
]);

$user = $stmt->fetch();

// Check if user exists
if (!$user) {

    $_SESSION["error"] = "Invalid email or password.";

    header("Location: ../login.php");
    exit;
}

// Verify password
if (!password_verify($password, $user["password_hash"])) {

    $_SESSION["error"] = "Invalid email or password.";

    header("Location: ../login.php");
    exit;
}

// Login successful
$_SESSION["user_id"] = $user["id"];
$_SESSION["user_name"] = $user["name"];
$_SESSION["user_email"] = $user["email"];

header("Location: ../dashboard.php");
exit;