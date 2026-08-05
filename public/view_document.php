<?php

require_once "../includes/auth.php";
require_once "../config/database.php";

/*
|--------------------------------------------------------------------------
| Validate request
|--------------------------------------------------------------------------
*/

if (!isset($_GET["document_id"]) || !is_numeric($_GET["document_id"])) {

    die("Invalid document.");

}

$documentId = (int) $_GET["document_id"];

/*
|--------------------------------------------------------------------------
| Verify ownership
|--------------------------------------------------------------------------
*/

$stmt = $pdo->prepare("
    SELECT *
    FROM uploaded_files
    WHERE id = ?
    AND user_id = ?
");

$stmt->execute([
    $documentId,
    $_SESSION["user_id"]
]);

$file = $stmt->fetch();

if (!$file) {

    die("Document not found.");

}

/*
|--------------------------------------------------------------------------
| Locate file
|--------------------------------------------------------------------------
*/

$path = "../uploads/" . $file["stored_filename"];

if (!file_exists($path)) {

    die("File not found.");

}

/*
|--------------------------------------------------------------------------
| Determine MIME type
|--------------------------------------------------------------------------
*/

$mime = mime_content_type($path);

if ($mime === false) {

    $mime = "application/octet-stream";

}

/*
|--------------------------------------------------------------------------
| Send file
|--------------------------------------------------------------------------
*/

header("Content-Type: " . $mime);

header("Content-Length: " . filesize($path));

header(
    'Content-Disposition: inline; filename="' .
    basename($file["original_filename"]) .
    '"'
);

header("Cache-Control: private");

readfile($path);

exit;