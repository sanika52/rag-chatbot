// ============================
// Get Elements
// ============================

const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const uploadBtn = document.getElementById("uploadBtn");

const sendBtn = document.getElementById("sendBtn");
const question = document.getElementById("question");
const chatBox = document.getElementById("chatBox");

// ============================
// Variables
// ============================

let uploadedFile = null;
let uploaded = false;

// ============================
// File Selection
// ============================

fileInput.addEventListener("change", function () {

    if (fileInput.files.length > 0) {

        uploadedFile = fileInput.files[0];

        fileName.innerHTML = "📄 " + uploadedFile.name;

    } else {

        uploadedFile = null;

        fileName.innerHTML = "No file selected";

    }

});

// ============================
// Upload Button
// ============================

uploadBtn.addEventListener("click", function () {

    if (!uploadedFile) {

        alert("Please choose a document first.");

        return;

    }

    uploaded = true;

    addBotMessage("✅ <b>" + uploadedFile.name + "</b> uploaded successfully.");

});

// ============================
// Send Button
// ============================

sendBtn.addEventListener("click", sendMessage);

// ============================
// Enter Key
// ============================

question.addEventListener("keypress", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

});

// ============================
// Send Message
// ============================

function sendMessage() {

    const message = question.value.trim();

    if (message === "") return;

    addUserMessage(message);

    question.value = "";

    setTimeout(function () {

        if (!uploaded) {

            addBotMessage("⚠ Please upload your document first.");

        }

        else {

            addBotMessage("🤖 Backend not connected yet.<br><br>After Python integration I'll answer only from your uploaded document.");

        }

    },600);

}

// ============================
// User Message
// ============================

function addUserMessage(message){

    const div=document.createElement("div");

    div.className="user-message";

    div.innerHTML=message;

    chatBox.appendChild(div);

    scrollBottom();

}

// ============================
// Bot Message
// ============================

function addBotMessage(message){

    const div=document.createElement("div");

    div.className="bot-message";

    div.innerHTML=message;

    chatBox.appendChild(div);

    scrollBottom();

}

// ============================
// Auto Scroll
// ============================

function scrollBottom(){

    chatBox.scrollTop=chatBox.scrollHeight;

}