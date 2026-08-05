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
// Track in-flight request (used to warn on refresh/close)
// ============================

let requestInFlight = false;

window.addEventListener("beforeunload", function (event) {

    if (requestInFlight) {

        event.preventDefault();
        event.returnValue = "";

    }

});

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

            if (!sendBtn.disabled) {

                sendMessage();

            }

        }

    });

}

// ============================
// Send Message
// ============================

async function sendMessage() {

    const message = question.value.trim();

    if (message === "") return;
    if (sendBtn.disabled) {
        return;
    }

    sendBtn.disabled = true;
    requestInFlight = true;

    addUserMessage(message);

    question.value = "";

    // Loading message
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "bot-message";
    loadingDiv.innerHTML = "🤖 Thinking...";
    chatBox.appendChild(loadingDiv);
    scrollBottom();

    try {
        console.log("Sending question:", message);
        const response = await fetch(
            "actions/chat_action.php",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: message
                })
            }
        );

        const data = await response.json();
        console.log(data);

        loadingDiv.remove();

        if (!response.ok || data.success === false) {

            addBotMessage(
                "❌ " +
                (data.message || "Something went wrong.")
            );
            sendBtn.disabled = false;
            requestInFlight = false;
            return;
        }

        let html = data.answer;

        if (data.sources && data.sources.length > 0) {
            html += "<br><br><strong>Sources</strong><br>";

            data.sources.forEach(source => {

                const pages = source.pages.join(", ");

                let url =
                    "view_document.php?document_id=" +
                    source.document_id;

                if (source.filename.toLowerCase().endsWith(".pdf")) {
                    url += "#page=" + source.pages[0];
                }

                html += `
                    📄
                    <a href="${url}" target="_blank">
                        ${source.filename}
                    </a>
                    (Pages ${pages})
                    <br>
                `;

            });

        }

        addBotMessage(html);
        sendBtn.disabled = false;
        requestInFlight = false;
    }

    catch (error) {

        loadingDiv.remove();

        addBotMessage(
            "❌ Unable to connect to the AI service."
        );

        console.error(error);
        sendBtn.disabled = false;
        requestInFlight = false;
    }

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

async function toggleDocument(event, documentId, form) {

    event.preventDefault();

    const formData = new FormData();

    formData.append("document_id", documentId);

    try {

        const response = await fetch(
            "actions/toggle_selection.php",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!data.success) {

            alert("Unable to update selection.");

            return;

        }

        const documentCard =
            form.closest(".uploaded-document");

        const label =
            documentCard.querySelector(".selected-label");

        if (data.selected) {

            documentCard.classList.add(
                "selected-document"
            );

            if (!label) {

                const status =
                    documentCard.querySelector(
                        ".document-status"
                    );

                status.insertAdjacentHTML(
                    "beforeend",
                    `
                    <span class="selected-label">
                        Selected
                    </span>
                    `
                );

            }

        }

        else {

            documentCard.classList.remove(
                "selected-document"
            );

            if (label) {

                label.remove();

            }

        }

    }

   catch (error) {

    console.error(error);

    alert(error.stack);

}

}