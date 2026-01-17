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
