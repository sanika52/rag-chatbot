<?php

session_start();

// Remove all session variables
$_SESSION = [];

// Destroy the session
session_destroy();

// Redirect to login
header("Location: /login.php");
exit;