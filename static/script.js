// ==========================================
// 1. DYNAMIC CONTENT LOADING (Bikers, Railway, etc.)
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    // Ye check karega ki URL mein kaunsi ID hai (e.g., detail.html?id=bikers)
    const urlParams = new URLSearchParams(window.location.search);
    const catId = urlParams.get('id');

    // Agar legalData available hai aur catId match hota hai
    if (typeof legalData !== 'undefined' && legalData[catId]) {
        const titleElement = document.getElementById('main-title');
        const contentElement = document.getElementById('main-content');
        
        if (titleElement && contentElement) {
            titleElement.innerText = legalData[catId].title;
            contentElement.innerHTML = `<ul>${legalData[catId].content}</ul>`;
        }
    }
});

// ==========================================
// 2. AI CHAT WINDOW TOGGLE
// ==========================================
function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    const displayStatus = window.getComputedStyle(chatWindow).display;
    chatWindow.style.display = (displayStatus === 'none') ? 'flex' : 'none';
}

// ==========================================
// 3. SEND MESSAGE TO BACKEND (Fixed for Render)
// ==========================================
async function sendChatMessage() {
    const inputField = document.getElementById('chat-input');
    const chatDisplay = document.getElementById('chat-display');
    const userMessage = inputField.value.trim();

    if (userMessage !== "") {
        // User message UI mein add karein
        addMessageToUI(userMessage, 'user');
        inputField.value = ""; 

        // Thinking indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'msg bot';
        loadingDiv.innerText = "NyayaShield AI soch raha hai...";
        loadingDiv.id = "temp-loader";
        chatDisplay.appendChild(loadingDiv);
        chatDisplay.scrollTop = chatDisplay.scrollHeight;

        try {
            // ✅ FIX: 'http://localhost:3000/chat' hata kar sirf '/chat' kiya hai
            // Isse Render apne aap sahi address pakad lega
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage })
            });

            if (!response.ok) {
                throw new Error("Server response was not ok");
            }

            const data = await response.json();

            // Loader remove karein
            const loader = document.getElementById('temp-loader');
            if(loader) loader.remove();

            // AI Response
            if (data.reply) {
                addMessageToUI(data.reply, 'bot');
            } else {
                addMessageToUI("Maaf kijiye, response nahi mil pa raha.", 'bot');
            }

        } catch (error) {
            console.error("Error:", error);
            const loader = document.getElementById('temp-loader');
            if(loader) loader.remove();
            // User-friendly message for Render's cold start
            addMessageToUI("Connection error! Server jagne mein 30-60 seconds le sakta hai, please thodi der mein dobara try karein.", 'bot');
        }
    }
}

// ==========================================
// 4. UI HELPER & FORMATTING
// ==========================================
function addMessageToUI(text, sender) {
    const chatDisplay = document.getElementById('chat-display');
    const div = document.createElement('div');
    div.className = `msg ${sender}`;
    div.style.whiteSpace = "pre-wrap"; 
    div.innerHTML = text.replace(/\n/g, '<br>'); 
    
    chatDisplay.appendChild(div);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

// WhatsApp Share Function
function shareToWhatsApp() {
    const title = document.getElementById('main-title')?.innerText || "NyayaShield Legal Info";
    const content = document.getElementById('main-content')?.innerText || "";
    const message = `*NyayaShield Legal Info*%0A%0A*${title}*%0A%0A${content}`;
    window.open(`https://api.whatsapp.com/send?text=${message}`, '_blank');
}