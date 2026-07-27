<?php

require_once "../../includes/auth.php";
require_once "../../config/database.php";

/*
|--------------------------------------------------------------------------
| Only allow POST requests
|--------------------------------------------------------------------------
*/

if ($_SERVER["REQUEST_METHOD"] !== "POST") {

    header("Location: ../dashboard.php");
    exit();
}

/*
|--------------------------------------------------------------------------
| Validate document ID
|--------------------------------------------------------------------------
*/

if (!isset($_POST["document_id"]) || !is_numeric($_POST["document_id"])) {

    $_SESSION["error"] = "Invalid document.";

    header("Location: ../dashboard.php");
    exit();
}

$documentId = (int) $_POST["document_id"];

/*
|--------------------------------------------------------------------------
| Verify document belongs to logged-in user
|--------------------------------------------------------------------------
*/

$stmt = $pdo->prepare("
    SELECT id
    FROM uploaded_files
    WHERE id = ?
    AND user_id = ?
");

$stmt->execute([
    $documentId,
    $_SESSION["user_id"]
]);

$document = $stmt->fetch();

if (!$document) {

    $_SESSION["error"] = "Document not found.";

    header("Location: ../dashboard.php");
    exit();
}

/*
|--------------------------------------------------------------------------
| Initialize selected documents session
|--------------------------------------------------------------------------
*/

if (!isset($_SESSION["selected_documents"])) {

    $_SESSION["selected_documents"] = [];
}

/*
|--------------------------------------------------------------------------
| Toggle selection
|--------------------------------------------------------------------------
*/

$selectedDocuments = $_SESSION["selected_documents"];

if (in_array($documentId, $selectedDocuments)) {

    // Remove document

    $_SESSION["selected_documents"] = array_values(
        array_diff($selectedDocuments, [$documentId])
    );

} else {

    // Add document

    $selectedDocuments[] = $documentId;

    $_SESSION["selected_documents"] = $selectedDocuments;
}

/*
|--------------------------------------------------------------------------
| Redirect back
|--------------------------------------------------------------------------
*/

header("Location: ../dashboard.php");
exit();