<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
        content="width=device-width, initial-scale=1.0">

    <title>RAG Chatbot</title>

    <!-- Google Font -->

    <link rel="preconnect"
        href="https://fonts.googleapis.com">

    <link rel="preconnect"
        href="https://fonts.gstatic.com"
        crossorigin>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
        rel="stylesheet">

    <!-- Icons -->

    <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">

    <!-- CSS -->

    <link rel="stylesheet"
        href="/assests/css/style.css">

</head>

<body>

<div class="container">

<!-- ================= LEFT PANEL ================= -->

<div class="left-panel">

<div class="logo">

<h1>RAG Chatbot</h1>

<p>

Upload your PDF, DOCX or TXT document and ask questions from it.

</p>

</div>

<div class="upload-wrapper">

<h2>

Upload Document

</h2>

<div class="upload-card">

<label
for="fileInput"
class="upload-box">

<i class="fa-solid fa-cloud-arrow-up"></i>

<h3>

Browse Document

</h3>

<p>

PDF • DOCX • TXT

</p>

</label>

<input
type="file"
id="fileInput"
accept=".pdf,.doc,.docx,.txt"
hidden>

<div
id="fileName"
class="selected-file">

No file selected

</div>

<button
id="uploadBtn">

Upload File

</button>

</div>

</div>

</div>

<!-- ================= RIGHT PANEL ================= -->

<div class="right-panel">

<div class="chat-header">

<div>

<h2>

Document Chat

</h2>

<p>

Ask anything related to your uploaded document.

</p>

</div>

</div>

<div
class="chat-box"
id="chatBox">

<div class="bot-message">

Hello 👋

<br><br>

Upload your document first.

Then ask me questions related to that document.

</div>

</div>

<div class="chat-input">

<textarea
id="question"
placeholder="Type your question here..."></textarea>

<button
id="sendBtn">

<i class="fa-solid fa-paper-plane"></i>

Send

</button>

</div>

</div>

</div>

<script src="/assests/js/script.js"></script>

</body>

</html>