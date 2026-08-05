<?php

require_once "../../includes/auth.php";
require_once "../../config/app.php";

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

$data = json_decode(file_get_contents("php://input"), true);

/*
|--------------------------------------------------------------------------
| Validate question
|--------------------------------------------------------------------------
*/

$question = trim($data["question"] ?? "");

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

$data = json_decode($response, true);

/*
|--------------------------------------------------------------------------
| Store chat history in session
|--------------------------------------------------------------------------
*/

if (!isset($_SESSION["chat_history"])) {

    $_SESSION["chat_history"] = [];

}

$_SESSION["chat_history"][] = [
    "role" => "user",
    "message" => $question
];

$_SESSION["chat_history"][] = [
    "role" => "assistant",
    "message" => $data["answer"],
    "sources" => $data["sources"]
];

/*
|--------------------------------------------------------------------------
| Return response to JavaScript
|--------------------------------------------------------------------------
*/

echo json_encode($data);