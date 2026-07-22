<?php

require_once "../includes/auth.php";
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

    <meta name="viewport"
        content="width=device-width, initial-scale=1.0">

    <title>RAG Chatbot</title>

    <!-- Google Font -->
    <link rel="preconnect"
        href="https://fonts.googleapis.com">

    <link rel="preconnect"
        href="https://fonts.gstatic.com"
        crossorigin>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
        rel="stylesheet">

    <!-- Icons -->
    <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">

    <!-- CSS -->
    <link rel="stylesheet" href="assets/css/style.css">

</head>

<body>

<div class="container">

    <!-- ================= LEFT PANEL ================= -->

    <div class="left-panel">

        <div class="logo">

            <h1>RAG Chatbot</h1>

            <p>
                Welcome,
                <strong><?= htmlspecialchars($_SESSION["user_name"]) ?></strong>
            </p>

            <p>
                Upload your PDF, DOCX or TXT document and ask questions from it.
            </p>

        </div>
        <?php if (!empty($success)): ?>
    <p style="color:green; text-align:center; margin-bottom:15px;">
        <?= htmlspecialchars($success) ?>
    </p>
<?php endif; ?>

<?php if (!empty($error)): ?>
    <p style="color:red; text-align:center; margin-bottom:15px;">
        <?= htmlspecialchars($error) ?>
    </p>
<?php endif; ?>


        <div class="upload-wrapper">

            <h2>
                Upload Document
            </h2>

            <form
    action="actions/upload_action.php"
    method="POST"
    enctype="multipart/form-data">

    <div class="upload-card">

        <label
            for="fileInput"
            class="upload-box">

            <i class="fa-solid fa-cloud-arrow-up"></i>

            <h3>Browse Document</h3>

            <p>PDF • DOCX • TXT</p>

        </label>

        <input
            type="file"
            id="fileInput"
            name="document"
            accept=".pdf,.doc,.docx,.txt"
            hidden
            required>

        <div
            id="fileName"
            class="selected-file">

            No file selected

        </div>

        <button
            type="submit"
            id="uploadBtn">

            Upload File

        </button>

    </div>

</form>

        </div>

        <br>

        <a href="logout.php">
            <button style="width:100%;">
                Logout
            </button>
        </a>

    </div>

    <!-- ================= RIGHT PANEL ================= -->

    <div class="right-panel">

        <div class="chat-header">

            <div>

                <h2>
                    Document Chat
                </h2>

                <p>
                    Ask anything related to your uploaded document.
                </p>

            </div>

        </div>

        <div
            class="chat-box"
            id="chatBox">

            <div class="bot-message">

                Hello,
                <strong><?= htmlspecialchars($_SESSION["user_name"]) ?></strong> 👋

                <br><br>

                Upload your document first.

                Then ask me questions related to that document.

            </div>

        </div>

        <div class="chat-input">

            <textarea
                id="question"
                placeholder="Type your question here..."></textarea>

            <button
                id="sendBtn">

                <i class="fa-solid fa-paper-plane"></i>

                Send

            </button>

        </div>

    </div>

</div>

<script src="assets/js/script.js"></script>

</body>

</html>