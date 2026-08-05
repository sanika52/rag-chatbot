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


/*
|--------------------------------------------------------------------------
| Load latest conversation
|--------------------------------------------------------------------------
*/

$stmt = $pdo->prepare("
    SELECT id
    FROM conversations
    WHERE user_id = ?
    ORDER BY created_at DESC
    LIMIT 1
");

$stmt->execute([
    $_SESSION["user_id"]
]);

$conversation = $stmt->fetch();

$chatHistory = [];

if ($conversation) {

    $stmt = $pdo->prepare("
    SELECT
        id,
        role,
        message,
        sources
    FROM chat_messages
    WHERE conversation_id = ?
    ORDER BY id ASC
");

    $stmt->execute([
        $conversation["id"]
    ]);

    $chatHistory = $stmt->fetchAll(PDO::FETCH_ASSOC);

}

foreach ($chatHistory as &$message) {

    if (!empty($message["sources"])) {

        $message["sources"] = json_decode(
            $message["sources"],
            true
        );

    } else {

        $message["sources"] = [];

    }

}

/*
|--------------------------------------------------------------------------
| Selected documents (Session)
|--------------------------------------------------------------------------
*/

if (!isset($_SESSION["selected_documents"])) {
    $_SESSION["selected_documents"] = [];
}

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

                Upload your PDF, DOCX or TXT documents and ask questions from them.

            </p>

        </div>
<?php if (!empty($documents)): ?>

<div class="uploaded-documents">

    <h2>Uploaded Documents</h2>

    <?php foreach ($documents as $document): ?>

        <div class="uploaded-document <?= in_array($document["id"], $_SESSION["selected_documents"]) ? 'selected-document' : '' ?>">

            <!-- Make document active -->
            <form
    class="document-form"
    onsubmit="toggleDocument(event, <?= $document["id"] ?>, this)">

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

                            <?php if (in_array($document["id"], $_SESSION["selected_documents"])): ?>

                               <span class="selected-label">

                                  Selected

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

                <h2>Chat with Documents</h2>

                <p>

                    Ask anything related to your uploaded documents.

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

            <?php if (!empty($chatHistory)): ?>

    <?php foreach ($chatHistory as $message): ?>

        <?php if ($message["role"] === "user"): ?>

            <div class="user-message">

                <?= htmlspecialchars($message["message"]) ?>

            </div>

        <?php else: ?>

            <div class="bot-message">

                <?= nl2br(htmlspecialchars($message["message"])) ?>

                <?php if (!empty($message["sources"])): ?>

                    <br><br>

                    <strong>Sources</strong><br>

                    <?php foreach ($message["sources"] as $source): ?>

                        <?php
                        $pages = !empty($source["pages"])
                            ? implode(", ", $source["pages"])
                            : "";
                        ?>

                        📄

                        <a
                            href="view_document.php?document_id=<?= $source["document_id"] ?>"
                            target="_blank"
                        >
                            <?= htmlspecialchars($source["filename"]) ?>
                        </a>

                        <?php if ($pages): ?>

                            (Pages <?= $pages ?>)

                        <?php endif; ?>

                        <br>

                    <?php endforeach; ?>

                <?php endif; ?>

            </div>

        <?php endif; ?>

    <?php endforeach; ?>

<?php endif; ?>

            <?php if (empty($chatHistory)): ?>

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

        Select one or more documents and start asking questions.

    <?php else: ?>

        Upload your first document.

        <br><br>

        Then ask me questions related to that document.

    <?php endif; ?>

</div>

<?php endif; ?>

        </div>

        <div class="chat-input">

            <textarea
                id="question"
                placeholder="Type your question here..."></textarea>

            <a
    href="actions/clear_chat.php"
    class="clear-chat-btn"
    title="Clear Chat"
    onclick="return confirm('Clear the current conversation?');"
>
    <i class="fa-solid fa-trash"></i>
</a>
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