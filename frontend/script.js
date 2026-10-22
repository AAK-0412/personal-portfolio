
// =====================================
// PERSONAL PORTFOLIO - FRONTEND LOGIC
// =====================================

const API_BASE_URL = "http://127.0.0.1:8000";


// =====================================
// LOAD PROJECTS FROM FASTAPI
// =====================================

async function loadProjects() {
    const projectsContainer = document.getElementById(
        "projects-container"
    );

    if (!projectsContainer) {
        return;
    }

    projectsContainer.textContent = "Loading projects...";

    try {
        const response = await fetch(
            `${API_BASE_URL}/projects`
        );

        if (!response.ok) {
            throw new Error("Unable to retrieve projects.");
        }

        const projects = await response.json();

        projectsContainer.replaceChildren();

        if (projects.length === 0) {
            projectsContainer.textContent =
                "No projects are available right now.";

            return;
        }

        projects.forEach((project) => {
            const card = createProjectCard(project);
            projectsContainer.appendChild(card);
        });

    } catch (error) {
        console.error("Project loading failed:", error);

        projectsContainer.textContent =
            "Projects could not be loaded. Please try again later.";
    }
}


// =====================================
// CREATE A PROJECT CARD
// =====================================

function createProjectCard(project) {
    const card = document.createElement("article");
    card.className = "project-card";

    const top = document.createElement("div");
    top.className = "project-top";

    const number = document.createElement("span");
    number.className = "project-number";
    number.textContent = `PROJECT / ${String(project.id).padStart(2, "0")}`;

    const status = document.createElement("span");
    status.className = "project-status";
    status.textContent = project.status;

    top.append(number, status);

    const title = document.createElement("h3");
    title.textContent = project.title;

    const description = document.createElement("p");
    description.textContent = project.description;

    const tags = document.createElement("div");
    tags.className = "tech-tags";

    const technologies = project.technologies
        .split(",")
        .map((technology) => technology.trim())
        .filter(Boolean);

    technologies.forEach((technology) => {
        const tag = document.createElement("span");
        tag.textContent = technology;
        tags.appendChild(tag);
    });

    card.append(top, title, description, tags);

    if (project.github_url) {
        const githubLink = document.createElement("a");

        githubLink.href = project.github_url;
        githubLink.target = "_blank";
        githubLink.rel = "noopener noreferrer";
        githubLink.className = "project-link";
        githubLink.textContent = "View on GitHub ↗";

        card.appendChild(githubLink);
    }

    if (project.demo_url) {
        const demoLink = document.createElement("a");

        demoLink.href = project.demo_url;
        demoLink.target = "_blank";
        demoLink.rel = "noopener noreferrer";
        demoLink.className = "project-link";
        demoLink.textContent = "Live Demo ↗";

        card.appendChild(demoLink);
    }

    if (!project.github_url && !project.demo_url) {
        const note = document.createElement("p");

        note.className = "project-link";
        note.textContent = "Deployment coming soon";

        card.appendChild(note);
    }

    return card;
}


// Load projects when the page is ready.
document.addEventListener("DOMContentLoaded", loadProjects);


// =====================================
// CONTACT FORM - TEMPORARY PROTOTYPE
// =====================================

const contactForm = document.getElementById("contact-form");
const formStatus = document.getElementById("form-status");

if (contactForm && formStatus) {
    contactForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        if (!contactForm.reportValidity()) {
            return;
        }

        const submitButton = contactForm.querySelector(
            'button[type="submit"]'
        );

        const formData = new FormData(contactForm);

        const payload = {
            name: formData.get("name").trim(),
            email: formData.get("email").trim(),
            subject: formData.get("subject").trim(),
            message: formData.get("message").trim()
        };

        submitButton.disabled = true;
        formStatus.textContent = "Sending your message...";

        try {
            const response = await fetch("http://127.0.0.1:8000/contact", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (!response.ok) {
                const detail = result.detail;

                throw new Error(
                    typeof detail === "string"
                        ? detail
                        : "Please check your details and try again."
                );
            }

            formStatus.textContent = result.message;
            contactForm.reset();

        } catch (error) {
            console.error("Contact form submission failed:", error);

            formStatus.textContent =
                error.message === "Failed to fetch"
                    ? "Unable to connect to the server. Please try again later."
                    : error.message || "Something went wrong. Please try again.";

        } finally {
            submitButton.disabled = false;
        }
    });
}

