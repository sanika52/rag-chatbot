<?php

session_start();

$error = "";
$success = "";

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

    <title>Login | RAG Chatbot</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">

    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="assets/css/auth.css">

    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">

</head>

<body class="login-page">

<div class="login-card">

    <h1>RAG CHATBOT</h1>

    <p>Login to continue</p>

    <?php if (!empty($error)): ?>
        <p class="validation-error">
            <?= htmlspecialchars($error) ?>
        </p>
    <?php endif; ?>

    <?php if (!empty($success)): ?>
        <p class="validation-success">
            <?= htmlspecialchars($success) ?>
        </p>
    <?php endif; ?>

    <form action="actions/login_action.php" method="POST">

        <!-- Email -->

        <div class="input-group">

            <input
                id="email"
                type="email"
                name="email"
                placeholder="Email Address"
                required>

            <small
                id="emailMessage"
                class="validation-message">
            </small>

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

            <small
                id="passwordMessage"
                class="validation-message">
            </small>

        </div>

        <button
            id="loginBtn"
            type="submit"
            disabled>

            Login

        </button>

    </form>

    <p style="margin-top:20px;">

        New User?

        <a href="register.php">
            Register Here
        </a>

    </p>

</div>

<script src="assets/js/login.js"></script>

</body>

</html>