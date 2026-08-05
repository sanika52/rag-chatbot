<?php

require_once "../../includes/auth.php";
require_once "../../config/app.php";
require_once "../../config/database.php";

/*
|--------------------------------------------------------------------------
| Keep running this script to completion even if the browser
| disconnects, refreshes, or navigates away mid-request.
| This prevents the "user message saved, assistant answer never
| written" bug caused by PHP killing execution on client disconnect.
|--------------------------------------------------------------------------
*/

ignore_user_abort(true);

header("Content-Type: application/json");

/*
|--------------------------------------------------------------------------
| Only allow POST requests
|--------------------------------------------------------------------------
*/

if ($_SERVER["REQUEST_METHOD"] !== "POST") {

    http_response_code(405);

    echo json_encode([
        "success" => false,
        "message" => "Method not allowed."
    ]);

    exit();
}

/*
|--------------------------------------------------------------------------
| Read request body
|--------------------------------------------------------------------------
*/

$requestData = json_decode(file_get_contents("php://input"), true);

/*
|--------------------------------------------------------------------------
| Validate question
|--------------------------------------------------------------------------
*/

$question = trim($requestData["question"] ?? "");

if ($question === "") {

    echo json_encode([
        "success" => false,
        "message" => "Question cannot be empty."
    ]);

    exit();
}

/*
|--------------------------------------------------------------------------
| Ensure at least one document is selected
|--------------------------------------------------------------------------
*/

if (
    !isset($_SESSION["selected_documents"]) ||
    empty($_SESSION["selected_documents"])
) {

    echo json_encode([
        "success" => false,
        "message" => "Please select at least one document."
    ]);

    exit();
}

/*
|--------------------------------------------------------------------------
| Get or create conversation
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

    $conversationId = (int) $conversation["id"];

} else {

    $stmt = $pdo->prepare("
        INSERT INTO conversations (user_id)
        VALUES (?)
    ");

    $stmt->execute([
        $_SESSION["user_id"]
    ]);

    $conversationId = (int) $pdo->lastInsertId();

}

/*
|--------------------------------------------------------------------------
| Prevent duplicate submission of the same question in quick
| succession (e.g. accidental double Enter/click, or a retried
| request). If the very last message in this conversation is a
| user message with the exact same text, reject this one instead
| of inserting a second copy.
|--------------------------------------------------------------------------
*/

$stmt = $pdo->prepare("
    SELECT role, message
    FROM chat_messages
    WHERE conversation_id = ?
    ORDER BY id DESC
    LIMIT 1
");

$stmt->execute([$conversationId]);

$lastMessage = $stmt->fetch();

if (
    $lastMessage &&
    $lastMessage["role"] === "user" &&
    $lastMessage["message"] === $question
) {

    echo json_encode([
        "success" => false,
        "message" => "This question is already being processed."
    ]);

    exit();

}

/*
|--------------------------------------------------------------------------
| Prepare payload for FastAPI
|--------------------------------------------------------------------------
*/

$payload = [
    "question" => $question,
    "user_id" => (int)$_SESSION["user_id"],
    "document_ids" => array_values($_SESSION["selected_documents"])
];

/*
|--------------------------------------------------------------------------
| Call FastAPI using cURL
|--------------------------------------------------------------------------
*/

$ch = curl_init();

curl_setopt_array($ch, [

    CURLOPT_URL => FASTAPI_URL . "/chat",

    CURLOPT_POST => true,

    CURLOPT_RETURNTRANSFER => true,

    CURLOPT_HTTPHEADER => [
        "Content-Type: application/json"
    ],

    CURLOPT_POSTFIELDS => json_encode($payload),

    CURLOPT_TIMEOUT => 30,

    CURLOPT_CONNECTTIMEOUT => 10

]);

$response = curl_exec($ch);

if ($response === false) {

    echo json_encode([
        "success" => false,
        "message" => "Unable to connect to the AI service.",
        "error" => curl_error($ch)
    ]);

    curl_close($ch);

    exit();
}

$httpStatus = curl_getinfo($ch, CURLINFO_HTTP_CODE);

curl_close($ch);

if ($httpStatus !== 200) {

    http_response_code($httpStatus);

    echo json_encode([
        "success" => false,
        "message" => "FastAPI returned an error.",
        "response" => json_decode($response, true)
    ]);

    exit();
}

/*
|--------------------------------------------------------------------------
| Decode FastAPI response
|--------------------------------------------------------------------------
*/

$responseData = json_decode($response, true);

/*
|--------------------------------------------------------------------------
| Validate that FastAPI actually returned an answer before writing
| anything to the DB. Prevents saving a user question with no
| matching assistant reply if FastAPI sends 200 with a malformed body.
|--------------------------------------------------------------------------
*/

if (!isset($responseData["answer"])) {

    echo json_encode([
        "success" => false,
        "message" => "The AI service did not return a valid answer."
    ]);

    exit();

}

/*
|--------------------------------------------------------------------------
| Save user message
|--------------------------------------------------------------------------
*/

$stmt = $pdo->prepare("
    INSERT INTO chat_messages
    (
        conversation_id,
        role,
        message,
        sources
    )
    VALUES
    (
        ?,
        ?,
        ?,
        ?
    )
");

$stmt->execute([
    $conversationId,
    "user",
    $question,
    null
]);

/*
|--------------------------------------------------------------------------
| Save assistant message
|--------------------------------------------------------------------------
*/

$stmt->execute([
    $conversationId,
    "assistant",
    $responseData["answer"],
    json_encode($responseData["sources"] ?? [])
]);

/*
|--------------------------------------------------------------------------
| Return response to JavaScript
|--------------------------------------------------------------------------
*/

echo json_encode($responseData);

exit();