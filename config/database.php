<?php

$host = "127.0.0.1";
$dbname = "rag_chatbot";
$username = "root";
$password = "sanika123";

try {

    $pdo = new PDO(
        "mysql:host=$host;dbname=$dbname;charset=utf8mb4",
        $username,
        $password
    );

    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);  // By default, PDO often reports errors quietly. We tell it : "If something goes wrong, throw an exception."

} catch (PDOException $e) {

    die("Database Connection Failed: " . $e->getMessage());

}

?>