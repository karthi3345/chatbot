const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");

async function sendMessage() {

    const message = chatInput.value.trim();

    if (!message) return;

    const response = await fetch("/chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    console.log(data.reply);

    chatInput.value = "";
}

sendBtn.addEventListener("click", sendMessage);