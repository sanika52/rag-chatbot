<?php

require_once "../../includes/auth.php";
require_once "../../config/database.php";

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    header("Location: ../dashboard.php");
    exit;
}

if (!isset($_POST["document_id"])) {
    header("Location: ../dashboard.php");
    exit;
}

$documentId = (int) $_POST["document_id"];
$userId = $_SESSION["user_id"];

// Check if the document belongs to the logged-in user
$checkSql = "
SELECT id
FROM uploaded_files
WHERE id = :id
AND user_id = :user_id
";

$checkStmt = $pdo->prepare($checkSql);

$checkStmt->execute([
    "id" => $documentId,
    "user_id" => $userId
]);

if (!$checkStmt->fetch()) {
    $_SESSION["error"] = "Invalid document.";
    header("Location: ../dashboard.php");
    exit;
}

// Make all user's documents inactive
$pdo->prepare("
UPDATE uploaded_files
SET is_active = FALSE
WHERE user_id = ?
")->execute([$userId]);

// Activate selected document
$pdo->prepare("
UPDATE uploaded_files
SET is_active = TRUE
WHERE id = ?
")->execute([$documentId]);

header("Location: ../dashboard.php");
exit;