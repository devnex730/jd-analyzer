document.getElementById("analyzeBtn").addEventListener("click", () => {
    const jdText = document.getElementById("jdInput").value.trim();

    if (!jdText) {
        alert("Please paste Job Description");
        return;
    }

    // Remove placeholder if exists
    const placeholder = document.getElementById("skills-p");
    if (placeholder) placeholder.remove();

    fetch("/get_jd/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ jd: jdText }),
    })
        .then(res => {
            if (!res.ok) throw new Error("Server error");
            return res.json();
        })
        .then(data => {
            console.log("JD Response:", data);
            renderResult(data);
        })
        .catch(err => {
            console.error("JS Error:", err);
            alert("Something went wrong while analyzing JD");
        });
});

function renderResult(data) {

    /* ---------- SKILLS ---------- */
    const skillsBox = document.getElementById("skills");
    skillsBox.querySelectorAll(".skill-btn").forEach(btn => btn.remove());

    (data.required_skills || []).forEach(skill => {
        const btn = document.createElement("button");
        btn.textContent = skill;
        btn.className = "skill-btn";
        skillsBox.appendChild(btn);
    });

    /* ---------- EXPERIENCE ---------- */
    const expBox = document.getElementById("experience");
    expBox.innerHTML = "<h2>Experience Needed</h2>";

    const expP = document.createElement("p");
    expP.textContent = data.required_experience || "Not specified";
    expBox.appendChild(expP);

    /* ---------- EDUCATION ---------- */
    const eduBox = document.getElementById("education");
    if (eduBox) {
        eduBox.innerHTML = "<h2>Education Required</h2>";

        if ((data.required_education || []).length === 0) {
            eduBox.innerHTML += "<p>Not specified</p>";
        } else {
            data.required_education.forEach(deg => {
                const p = document.createElement("p");
                p.textContent = deg;
                eduBox.appendChild(p);
            });
        }
    }

    /* ---------- KEYWORDS ---------- */
    const keywordBox = document.getElementById("keywords");
    if (keywordBox) {
        keywordBox.innerHTML = "<h2>Important Keywords</h2>";

        (data.important_keywords || []).forEach(word => {
            const span = document.createElement("span");
            span.textContent = word;
            span.className = "keyword-tag";
            keywordBox.appendChild(span);
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {

    const icon = document.getElementById("chat-icon");
    const panel = document.getElementById("chat-panel");
    const closeBtn = document.getElementById("close-chat");

    icon.addEventListener("click", () => {
        panel.classList.add("open");
        document.body.classList.add("chat-open");
    });

    closeBtn.addEventListener("click", () => {
        panel.classList.remove("open");
        document.body.classList.remove("chat-open");
    });

    const ws = new WebSocket(
        (location.protocol === "https:" ? "wss://" : "ws://") +
        location.host +
        "/ws/chat/"
    );

    const chatBody = document.getElementById("chat-body");
    const input = document.querySelector("#chat-input-box input");
    const sendBtn = document.querySelector("#chat-input-box button");

    function addMessage(text, sender) {
        const msg = document.createElement("div");
        msg.className = `msg ${sender}`;

        let cleaned = text
            .replace(/\*/g, "")
            .replace(/\s{2,}/g, " ")
            .replace(/(\)|\.)\s*/g, "$1\n")
            .trim();

        msg.innerText = cleaned;
        chatBody.appendChild(msg);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        addMessage(data.reply, "bot");
    };

    ws.onerror = () => {
        addMessage("Connection error. Please refresh.", "bot");
    };

    function sendMessage() {
        const text = input.value.trim();
        if (!text || ws.readyState !== WebSocket.OPEN) return;

        addMessage(text, "user");
        ws.send(JSON.stringify({ message: text }));
        input.value = "";
    }

    sendBtn.addEventListener("click", sendMessage);

    input.addEventListener("keydown", e => {
        if (e.key === "Enter") sendMessage();
    });

});
