let currentProfile = null;
let currentRecommendations = [];


async function generateRecommendations() {

    const profile = {
        name: document.getElementById("name").value,
        age: document.getElementById("age").value,
        background: document.getElementById("background").value,
        interests: document.getElementById("interests").value,
        skill_level: document.getElementById("skill_level").value,
        preference: document.getElementById("preference").value,
        goal: document.getElementById("goal").value,
        num_items: document.getElementById("num_items").value
    };

    document.getElementById("loading").style.display = "block";

    try {

        const response = await fetch("/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(profile)
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.error);
            return;
        }

        currentProfile = data.profile;
        currentRecommendations = data.recommendations;

        displayRecommendations(currentRecommendations);

        document.getElementById("recommendationSection")
            .classList.remove("hidden");

        document.getElementById("feedbackSection")
            .classList.remove("hidden");

    } catch (error) {

        alert("Something went wrong: " + error);

    } finally {

        document.getElementById("loading").style.display = "none";
    }
}


function displayRecommendations(recommendations) {

    const container = document.getElementById("recommendations");

    container.innerHTML = "";

    recommendations.sort((a, b) => b.score - a.score);

    recommendations.forEach((item, index) => {

        const card = document.createElement("div");

        card.className = "recommendation";

        card.innerHTML = `
            <h3>${index + 1}. ${item.name}</h3>
            <div class="score">
                Suitability Score: ${item.score}%
            </div>
            <p>
                <strong>Reason:</strong>
                ${item.reason}
            </p>
        `;

        container.appendChild(card);
    });
}


async function refineRecommendations() {

    const feedback = document.getElementById("feedback").value;

    if (!feedback.trim()) {
        alert("Please enter your feedback.");
        return;
    }

    document.getElementById("loading").style.display = "block";

    try {

        const response = await fetch("/refine", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                profile: currentProfile,
                feedback: feedback
            })
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.error);
            return;
        }

        currentRecommendations = data.recommendations;

        displayRecommendations(currentRecommendations);

        document.getElementById("feedback").value = "";

    } catch (error) {

        alert("Something went wrong: " + error);

    } finally {

        document.getElementById("loading").style.display = "none";
    }
}
async function saveRecommendations() {

    if (!currentRecommendations.length) {
        alert("No recommendations available to save.");
        return;
    }

    try {

        const response = await fetch("/save", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                recommendations: currentRecommendations
            })
        });

        const data = await response.json();

        if (data.success) {
            alert("Recommendations saved successfully!");
        } else {
            alert("Error: " + data.error);
        }

    } catch (error) {

        alert("Something went wrong: " + error);

    }s
}
function showProfile() {

    if (!currentProfile) {
        alert("Please generate recommendations first.");
        return;
    }

    const profileDetails = document.getElementById("profileDetails");

    profileDetails.innerHTML = `
        <p><strong>Name:</strong> ${currentProfile.name}</p>
        <p><strong>Age:</strong> ${currentProfile.age}</p>
        <p><strong>Background:</strong> ${currentProfile.background}</p>
        <p><strong>Interests:</strong> ${currentProfile.interests}</p>
        <p><strong>Skill Level:</strong> ${currentProfile.skill_level}</p>
        <p><strong>Preference:</strong> ${currentProfile.preference}</p>
        <p><strong>Goal:</strong> ${currentProfile.goal}</p>
        <p><strong>Number of Recommendations:</strong> ${currentProfile.num_items}</p>
    `;

    document.getElementById("profileSection")
        .classList.remove("hidden");
}
function showExplanations() {

    if (!currentRecommendations.length) {
        alert("Please generate recommendations first.");
        return;
    }

    const container = document.getElementById("explanations");

    container.innerHTML = `
        <h3>💡 Why These Recommendations?</h3>
    `;

    currentRecommendations.forEach((item, index) => {

        const explanation = document.createElement("div");

        explanation.className = "recommendation";

        explanation.innerHTML = `
            <h3>${index + 1}. ${item.name}</h3>

            <p>
                <strong>Suitability Score:</strong>
                ${item.score}%
            </p>

            <p>
                <strong>Why it is suitable:</strong>
                ${item.reason}
            </p>
        `;

        container.appendChild(explanation);
    });

    container.classList.remove("hidden");
}
async function detectUserIntent() {

    const input = document.getElementById("intentInput").value;

    if (!input.trim()) {
        alert("Please enter a command.");
        return;
    }

    try {

        const response = await fetch("/intent", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                input: input
            })
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.error);
            return;
        }

        const detectedIntent = data.intent;

        document.getElementById("intentResult").innerHTML = `
            <p>
                <strong>Detected Intent:</strong>
                ${detectedIntent}
            </p>
        `;


        // Perform action based on detected intent

        if (detectedIntent === "SHOW_PROFILE") {

            showProfile();

        }

        else if (detectedIntent === "EXPLAIN_RECOMMENDATION") {

            showExplanations();

        }

        else if (detectedIntent === "SAVE_RECOMMENDATION") {

            saveRecommendations();

        }

        else if (detectedIntent === "REFINE_RECOMMENDATION") {

            document.getElementById("feedback").focus();

        }

        else if (detectedIntent === "GENERATE_RECOMMENDATION") {

            generateRecommendations();

        }

        else if (detectedIntent === "EXIT") {

            alert("Thank you for using the Personalized Recommendation System!");

        }

        else {

            alert("Sorry, I could not understand that command.");

        }

    } catch (error) {

        alert("Something went wrong: " + error);

    }
}
function resetApplication() {

    // Clear profile variables
    currentProfile = null;
    currentRecommendations = [];

    // Clear form fields
    document.getElementById("name").value = "";
    document.getElementById("age").value = "";
    document.getElementById("background").value = "";
    document.getElementById("interests").value = "";
    document.getElementById("skill_level").value = "";
    document.getElementById("preference").value = "";
    document.getElementById("goal").value = "";
    document.getElementById("num_items").value = "5";

    // Clear feedback
    document.getElementById("feedback").value = "";

    // Clear recommendations
    document.getElementById("recommendations").innerHTML = "";

    // Hide result sections
    document.getElementById("recommendationSection")
        .classList.add("hidden");

    document.getElementById("feedbackSection")
        .classList.add("hidden");

    document.getElementById("profileSection")
        .classList.add("hidden");

    document.getElementById("explanations")
        .classList.add("hidden");

    // Clear intent section
    document.getElementById("intentInput").value = "";
    document.getElementById("intentResult").innerHTML = "";

    // Go back to top
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}