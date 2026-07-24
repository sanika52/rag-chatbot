<?php

require_once "../includes/auth.php";
require_once "../config/database.php";

$error = "";
$success = "";

$userName = $_SESSION["user_name"];
$userInitial = strtoupper(substr($userName, 0, 1));

if (isset($_SESSION["error"])) {
    $error = $_SESSION["error"];
    unset($_SESSION["error"]);
}

if (isset($_SESSION["success"])) {
    $success = $_SESSION["success"];
    unset($_SESSION["success"]);
}

/*
|--------------------------------------------------------------------------
| Fetch uploaded documents
|--------------------------------------------------------------------------
*/

$stmt = $pdo->prepare("
    SELECT *
    FROM uploaded_files
    WHERE user_id = ?
    ORDER BY upload_time DESC
");

$stmt->execute([$_SESSION["user_id"]]);

$documents = $stmt->fetchAll(PDO::FETCH_ASSOC);

?>

<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0">

    <title>RAG Chatbot</title>

    <!-- Google Font -->

    <link
        rel="preconnect"
        href="https://fonts.googleapis.com">

    <link
        rel="preconnect"
        href="https://fonts.gstatic.com"
        crossorigin>

    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
        rel="stylesheet">

    <!-- Font Awesome -->

    <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">

    <!-- CSS -->

    <link
        rel="stylesheet"
        href="assets/css/style.css">

</head>

<body>

<div class="container">

    <!-- ================= LEFT PANEL ================= -->

    <div class="left-panel">

        <div class="logo">

            <h1>RAG Chatbot</h1>

            <p>

                Welcome,

                <strong>

                    <?= htmlspecialchars($_SESSION["user_name"]) ?>

                </strong>

            </p>

            <p>

                Upload your PDF, DOCX or TXT document and ask questions from it.

            </p>

        </div>
<?php if (!empty($documents)): ?>

<div class="uploaded-documents">

    <h2>Uploaded Documents</h2>

    <?php foreach ($documents as $document): ?>

        <div class="uploaded-document <?= $document["is_active"] ? 'active-document' : '' ?>">

            <!-- Make document active -->
            <form
                action="actions/set_active_document.php"
                method="POST"
                class="document-form">

                <input
                    type="hidden"
                    name="document_id"
                    value="<?= $document["id"] ?>">

                <button
                    type="submit"
                    class="document-button">

                    <div class="document-icon">

                        <i class="fa-solid fa-file-lines"></i>

                    </div>

                    <div class="document-info">

                        <div class="document-name">

                            <?= htmlspecialchars($document["original_filename"]) ?>

                        </div>

                        <div class="document-meta">

                            <?php

                            $size = $document["file_size"];
                            $type = strtoupper($document["file_type"]);

                            if ($size >= 1024 * 1024) {
                                echo $type . " • " . round($size / (1024 * 1024), 1) . " MB";
                            } else {
                                echo $type . " • " . round($size / 1024, 1) . " KB";
                            }

                            ?>

                        </div>

                        <div class="document-status">

                            <i class="fa-solid fa-circle-check"></i>

                            <?= htmlspecialchars($document["status"]) ?>

                            <?php if ($document["is_active"]): ?>

                                <span class="active-label">

                                    Active

                                </span>

                            <?php endif; ?>

                        </div>

                    </div>

                </button>

            </form>

            <!-- Delete document -->

            <form
                action="actions/delete_document.php"
                method="POST"
                class="delete-form"
                onsubmit="return confirm('Delete this document?');">

                <input
                    type="hidden"
                    name="document_id"
                    value="<?= $document["id"] ?>">

                <button
                    type="submit"
                    class="delete-btn"
                    title="Delete Document">

                    <i class="fa-solid fa-trash"></i>

                </button>

            </form>

        </div>

    <?php endforeach; ?>

</div>

<?php endif; ?>


<?php if (!empty($error)): ?>

<p
    style="color:#dc2626;text-align:center;margin-bottom:15px;">

    <?= htmlspecialchars($error) ?>

</p>

<?php endif; ?>

<?php if (!empty($success)): ?>

<p
    style="
        color:#16a34a;
        text-align:center;
        margin-bottom:15px;
        font-weight:600;
    ">

    <?= htmlspecialchars($success) ?>

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

                <h3>

                    Browse Document

                </h3>

                <p>

                    PDF • DOCX • TXT

                </p>

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

                <?php if (!empty($documents)): ?>

                    <?= count($documents) ?> document(s) uploaded

                <?php else: ?>

                    No file selected

                <?php endif; ?>

            </div>

            <button
                type="submit"
                id="uploadBtn">

                <?php if (!empty($documents)): ?>

                    Upload Another Document

                <?php else: ?>

                    Upload File

                <?php endif; ?>

            </button>

        </div>

    </form>

</div>

</div>

    <!-- ================= RIGHT PANEL ================= -->

    <div class="right-panel">

        <div class="chat-header">

            <div class="header-left">

                <h2>Document Chat</h2>

                <p>

                    Ask anything related to your uploaded document.

                </p>

            </div>

            <div class="profile-menu">

                <button
                    id="profileBtn"
                    class="profile-btn">

                    <?= htmlspecialchars($userInitial) ?>

                </button>

                <div
                    id="profileDropdown"
                    class="profile-dropdown">

                    <div class="profile-header">

                        <div class="profile-avatar">

                            <?= htmlspecialchars($userInitial) ?>

                        </div>

                        <div class="profile-name">

                            <?= htmlspecialchars($userName) ?>

                        </div>

                        <div class="profile-email">

                            <?= htmlspecialchars($_SESSION["user_email"]) ?>

                        </div>

                    </div>

                    <hr>

                    <a href="actions/logout_action.php">

                        <i class="fa-solid fa-right-from-bracket"></i>

                        Logout

                    </a>

                </div>

            </div>

        </div>

        <div
            class="chat-box"
            id="chatBox">

            <div class="bot-message">

                Hello,

                <strong>

                    <?= htmlspecialchars($_SESSION["user_name"]) ?>

                </strong>

                👋

                <br><br>

                <?php if (!empty($documents)): ?>

                    Your documents are ready!

                    <br><br>

                    Select the active document (if needed) and start asking questions.

                <?php else: ?>

                    Upload your first document.

                    <br><br>

                    Then ask me questions related to that document.

                <?php endif; ?>

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

<script src="assets/js/dashboard.js"></script>

</body>

</html>