<?php

require_once "../../includes/auth.php";
require_once "../../config/database.php";

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    header("Location: ../dashboard.php");
    exit();
}

$userId = $_SESSION["user_id"];
$documentId = $_POST["document_id"] ?? 0;

/*
|--------------------------------------------------------------------------
| Get the document
|--------------------------------------------------------------------------
*/

$stmt = $pdo->prepare("
    SELECT *
    FROM uploaded_files
    WHERE id = ?
    AND user_id = ?
");

$stmt->execute([$documentId, $userId]);

$document = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$document) {

    $_SESSION["error"] = "Document not found.";

    header("Location: ../dashboard.php");
    exit();
}

/*
|--------------------------------------------------------------------------
| Delete physical file
|--------------------------------------------------------------------------
*/

$filePath = "../../uploads/" . $document["stored_filename"];

if (file_exists($filePath)) {
    unlink($filePath);
}

/*
|--------------------------------------------------------------------------
| Delete database row
|--------------------------------------------------------------------------
*/

$stmt = $pdo->prepare("
    DELETE FROM uploaded_files
    WHERE id = ?
");

$stmt->execute([$documentId]);

/*
|--------------------------------------------------------------------------
| If deleted document was active,
| make the newest remaining document active
|--------------------------------------------------------------------------
*/

if ($document["is_active"]) {

    $stmt = $pdo->prepare("
        SELECT id
        FROM uploaded_files
        WHERE user_id = ?
        ORDER BY upload_time DESC
        LIMIT 1
    ");

    $stmt->execute([$userId]);

    $nextDocument = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($nextDocument) {

        $stmt = $pdo->prepare("
            UPDATE uploaded_files
            SET is_active = TRUE
            WHERE id = ?
        ");

        $stmt->execute([$nextDocument["id"]]);
    }
}

$_SESSION["success"] = "Document deleted successfully.";

header("Location: ../dashboard.php");
exit();