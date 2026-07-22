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

    <link rel="stylesheet" href="assets/css/style.css">

</head>

<body class="login-page">

    <div class="login-card">

        <h1>RAG CHATBOT</h1>

        <p>Login to continue</p>

        <?php if (!empty($error)): ?>
            <p style="color:red; text-align:center; margin-bottom:15px;">
                <?= htmlspecialchars($error) ?>
            </p>
        <?php endif; ?>

        <?php if (!empty($success)): ?>
            <p style="color:green; text-align:center; margin-bottom:15px;">
                <?= htmlspecialchars($success) ?>
            </p>
        <?php endif; ?>

        <!-- Login Form -->
        <form action="actions/login_action.php" method="POST">

            <input
                type="email"
                name="email"
                placeholder="Email Address"
                required>

            <input
                type="password"
                name="password"
                placeholder="Password"
                required>

            <button type="submit">
                Login
            </button>

        </form>

        <p style="margin-top:15px; text-align:center;">
            New User?
            <a href="register.php">Register Here</a>
        </p>

    </div>

</body>

</html>