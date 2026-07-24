<?php

require_once "../../includes/auth.php";
require_once "../../config/database.php";

// Ensure request is POST
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    header("Location: ../dashboard.php");
    exit;
}

// Check if file exists
if (!isset($_FILES["document"])) {
    $_SESSION["error"] = "Please choose a file.";
    header("Location: ../dashboard.php");
    exit;
}

$file = $_FILES["document"];

// Check upload error
if ($file["error"] !== UPLOAD_ERR_OK) {
    $_SESSION["error"] = "File upload failed.";
    header("Location: ../dashboard.php");
    exit;
}

// Allowed file types
$allowedExtensions = [
    "pdf",
    "doc",
    "docx",
    "txt"
];

$extension = strtolower(pathinfo($file["name"], PATHINFO_EXTENSION));

if (!in_array($extension, $allowedExtensions)) {
    $_SESSION["error"] = "Invalid file type.";
    header("Location: ../dashboard.php");
    exit;
}

// Maximum file size = 10 MB
$maxSize = 10 * 1024 * 1024;

if ($file["size"] > $maxSize) {
    $_SESSION["error"] = "File is too large.";
    header("Location: ../dashboard.php");
    exit;
}

// Generate unique filename
$storedFileName = uniqid("doc_", true) . "." . $extension;

// Upload folder
$uploadDirectory = __DIR__ . "/../../uploads/";
$destination = $uploadDirectory . $storedFileName;

// Move uploaded file
if (!move_uploaded_file($file["tmp_name"], $destination)) {
    $_SESSION["error"] = "Failed to save uploaded file.";
    header("Location: ../dashboard.php");
    exit;
}

// Make all previously uploaded documents inactive

$deactivateSql = "
UPDATE uploaded_files
SET is_active = FALSE
WHERE user_id = :user_id
";

$deactivateStmt = $pdo->prepare($deactivateSql);

$deactivateStmt->execute([
    "user_id" => $_SESSION["user_id"]
]);

// Save metadata in database
$sql = "
INSERT INTO uploaded_files
(
    user_id,
    original_filename,
    stored_filename,
    file_size,
    file_type,
    status,
    is_active
)
VALUES
(
    :user_id,
    :original_filename,
    :stored_filename,
    :file_size,
    :file_type,
    :status,
    :is_active
)
";

$stmt = $pdo->prepare($sql);

$stmt->execute([
    "user_id"           => $_SESSION["user_id"],
    "original_filename" => $file["name"],
    "stored_filename"   => $storedFileName,
    "file_size"         => $file["size"],
    "file_type"         => strtoupper($extension),
    "status"            => "Ready",
    "is_active"         => true
]);

$_SESSION["success"] = "Document uploaded successfully.";

header("Location: ../dashboard.php");
exit;