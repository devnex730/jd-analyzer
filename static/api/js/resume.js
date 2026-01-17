document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("resumeform");
    const addBtn = document.getElementById("add-experience-btn");
    const container = document.getElementById("experience-container");

    addBtn.addEventListener("click", function () {
        const div = document.createElement("div");
        div.classList.add("experience-block");
        div.style.marginTop = "0.8rem";

        div.innerHTML = `
            <input type="text" name="job_title[]" placeholder="Job Title">
            <input type="text" name="company[]" placeholder="Company Name">
            <textarea name="experience_desc[]" placeholder="Responsibilities & achievements"></textarea>
            <button type="button" class="btn7 remove-exp">Remove</button>
        `;

        container.appendChild(div);
    });

    container.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-exp")) {
            e.target.parentElement.remove();
        }
    });

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch("/build_resume/", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                window.location.href = data.redirect_url;
            } else {
                alert("Failed to build resume");
            }
        })
        .catch(err => {
            console.error(err);
            alert("Server error");
        });
    });

});
