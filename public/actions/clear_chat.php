<?php

require_once "../../includes/auth.php";

unset($_SESSION["chat_history"]);

header("Location: ../dashboard.php");

exit();