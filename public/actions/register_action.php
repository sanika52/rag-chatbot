<?php

session_start();

require_once "../../config/database.php";

if ($_SERVER["REQUEST_METHOD"] !== "POST") {

    header("Location: ../register.php");
    exit;
}

$name = trim($_POST["name"]);
$email = trim($_POST["email"]);
$password = trim($_POST["password"]);

if (empty($name) || empty($email) || empty($password)) {

    $_SESSION["error"] = "All fields are required.";

    header("Location: ../register.php");
    exit;
}

// Check if email already exists
$sql = "SELECT id FROM users WHERE email = :email";

$stmt = $pdo->prepare($sql);
$stmt->execute([
    "email" => $email
]);

if ($stmt->fetch()) {

    $_SESSION["error"] = "Email already exists.";

    header("Location: ../register.php");
    exit;
}

// Hash password
$passwordHash = password_hash($password, PASSWORD_DEFAULT);

// Insert user
$sql = "INSERT INTO users(name, email, password_hash)
        VALUES(:name, :email, :password_hash)";

$stmt = $pdo->prepare($sql);

$stmt->execute([
    "name" => $name,
    "email" => $email,
    "password_hash" => $passwordHash
]);

$_SESSION["success"] = "Registration successful! Please login.";

header("Location: ../login.php");
exit;