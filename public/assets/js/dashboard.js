// ============================
// Get Elements
// ============================

const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const uploadBtn = document.getElementById("uploadBtn");

const sendBtn = document.getElementById("sendBtn");
const question = document.getElementById("question");
const chatBox = document.getElementById("chatBox");

const profileBtn = document.getElementById("profileBtn");
const profileDropdown = document.getElementById("profileDropdown");

// ============================
// File Selection
// ============================

if (fileInput) {

    fileInput.addEventListener("change", function () {

        if (fileInput.files.length > 0) {

            fileName.innerHTML = "📄 " + fileInput.files[0].name;

        }

        else {

            fileName.innerHTML = "No file selected";

        }

    });

}

// ============================
// Send Button
// ============================

if (sendBtn) {

    sendBtn.addEventListener("click", sendMessage);

}

// ============================
// Enter Key
// ============================

if (question) {

    question.addEventListener("keypress", function (event) {

        if (event.key === "Enter" && !event.shiftKey) {

            event.preventDefault();

            sendMessage();

        }

    });

}

// ============================
// Send Message
// ============================

function sendMessage() {

    const message = question.value.trim();

    if (message === "") return;

    addUserMessage(message);

    question.value = "";

    setTimeout(function () {

        addBotMessage(
            "🤖 <strong>AI backend is not connected yet.</strong><br><br>" +
            "Once the Python RAG service is integrated, I'll answer questions from your uploaded document."
        );

    }, 600);

}

// ============================
// User Message
// ============================

function addUserMessage(message) {

    const div = document.createElement("div");

    div.className = "user-message";

    div.innerHTML = message;

    chatBox.appendChild(div);

    scrollBottom();

}

// ============================
// Bot Message
// ============================

function addBotMessage(message) {

    const div = document.createElement("div");

    div.className = "bot-message";

    div.innerHTML = message;

    chatBox.appendChild(div);

    scrollBottom();

}

// ============================
// Profile Dropdown
// ============================

if (profileBtn && profileDropdown) {

    profileBtn.addEventListener("click", function (event) {

        event.stopPropagation();

        profileDropdown.classList.toggle("show");

    });

    document.addEventListener("click", function (event) {

        if (
            !profileBtn.contains(event.target) &&
            !profileDropdown.contains(event.target)
        ) {

            profileDropdown.classList.remove("show");

        }

    });

}

// ============================
// Auto Scroll
// ============================

function scrollBottom() {

    chatBox.scrollTop = chatBox.scrollHeight;

}