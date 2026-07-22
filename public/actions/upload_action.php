<?php

require_once "../../includes/auth.php";
require_once "../../config/database.php";

// Ensure the request is POST
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    header("Location: ../dashboard.php");
    exit;
}

// Check if a file was uploaded
if (!isset($_FILES["document"])) {

    $_SESSION["error"] = "Please choose a file.";

    header("Location: ../dashboard.php");
    exit;
}

$file = $_FILES["document"];

// Check for upload errors
if ($file["error"] !== UPLOAD_ERR_OK) {

    $_SESSION["error"] = "File upload failed.";

    header("Location: ../dashboard.php");
    exit;
}

// Allowed extensions
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

// Maximum size = 10 MB
$maxSize = 10 * 1024 * 1024;

if ($file["size"] > $maxSize) {

    $_SESSION["error"] = "File is too large.";

    header("Location: ../dashboard.php");
    exit;
}

// Generate unique filename
$storedFileName = uniqid("doc_", true) . "." . $extension;

// uploads folder
$uploadDirectory = "../../uploads/";

$destination = $uploadDirectory . $storedFileName;

// Move uploaded file
if (!move_uploaded_file($file["tmp_name"], $destination)) {

    $_SESSION["error"] = "Failed to save uploaded file.";

    header("Location: ../dashboard.php");
    exit;
}

// Save upload details in database
$sql = "INSERT INTO uploaded_files
        (user_id, original_filename, stored_filename)
        VALUES
        (:user_id, :original_filename, :stored_filename)";

$stmt = $pdo->prepare($sql);

$stmt->execute([
    "user_id" => $_SESSION["user_id"],
    "original_filename" => $file["name"],
    "stored_filename" => $storedFileName
]);

$_SESSION["success"] = "Document uploaded successfully.";

header("Location: ../dashboard.php");
exit;