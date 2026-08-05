<?php

require_once "../../includes/auth.php";
require_once "../../config/database.php";

/*
|--------------------------------------------------------------------------
| Delete latest conversation
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

if ($conversation) {

    $stmt = $pdo->prepare("
        DELETE
        FROM conversations
        WHERE id = ?
    ");

    $stmt->execute([
        $conversation["id"]
    ]);

}

header("Location: ../dashboard.php");

exit();