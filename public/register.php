<?php

session_start();

$error = "";
$success = "";
$oldName = $_SESSION["old_name"] ?? "";
$oldEmail = $_SESSION["old_email"] ?? "";

unset($_SESSION["old_name"]);
unset($_SESSION["old_email"]);

if (isset($_SESSION["error"])) {
    $error = $_SESSION["error"];
    unset($_SESSION["error"]);
}

if (isset($_SESSION["success"])) {
    $success = $_SESSION["success"];
    unset($_SESSION["success"]);
}

?>

<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Register | RAG Chatbot</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">

    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="assets/css/style.css">

    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">

</head>

<body class="login-page">

<div class="login-card">

    <h1>RAG CHATBOT</h1>

    <p>Create a new account</p>

    <?php if (!empty($error)): ?>
        <div class="alert alert-error">
            <?= htmlspecialchars($error) ?>
        </div>
    <?php endif; ?>

    <?php if (!empty($success)): ?>
        <div class="alert alert-success">
            <?= htmlspecialchars($success) ?>
    </div>
    <?php endif; ?>

    <form action="actions/register_action.php" method="POST">

        <!-- Name -->

        <div class="input-group">

            <input
                id="name"
                type="text"
                name="name"
                placeholder="Full Name"
                value="<?= htmlspecialchars($oldName) ?>"
                required>

            <small id="nameMessage" class="validation-message"></small>

        </div>

        <!-- Email -->

        <div class="input-group">

            <input
                id="email"
                type="email"
                name="email"
                placeholder="Email Address"
                value="<?= htmlspecialchars($oldEmail) ?>"
                required>

            <small id="emailMessage" class="validation-message"></small>

        </div>

        <!-- Password -->

        <div class="input-group">

            <div class="input-wrapper">

                <input
                    id="password"
                    type="password"
                    name="password"
                    placeholder="Password"
                    required>

                <i
                    id="togglePassword"
                    class="fa-solid fa-eye toggle-password">
                </i>

            </div>

        </div>

        <div id="passwordChecklist" class="password-checklist">

            <div id="length">❌ At least 8 characters</div>

            <div id="upper">❌ One uppercase letter</div>

            <div id="lower">❌ One lowercase letter</div>

            <div id="number">❌ One number</div>

            <div id="special">❌ One special character</div>

        </div>

        <!-- Confirm Password -->

        <div class="input-group">

            <div class="input-wrapper">

                <input
                    id="confirmPassword"
                    type="password"
                    name="confirm_password"
                    placeholder="Confirm Password"
                    required>

                <i
                    id="toggleConfirmPassword"
                    class="fa-solid fa-eye toggle-password">
                </i>

            </div>

            <small id="confirmMessage" class="validation-message"></small>

        </div>

        <button
            id="registerBtn"
            type="submit"
            disabled>
            Register
        </button>

    </form>

    <p style="margin-top:20px;">

        Already have an account?

        <a href="login.php">Login Here</a>

    </p>

</div>

<script src="assets/js/register.js"></script>

</body>

</html>