document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("resumeform");

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
