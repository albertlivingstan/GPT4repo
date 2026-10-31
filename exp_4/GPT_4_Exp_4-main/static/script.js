/**
 * PathFinder AI — Recommendation Studio Client Engine
 */

let currentProfile = null;
let currentRecommendations = [];
let personas = [];

document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/personas")
        .then(r => r.json())
        .then(data => { personas = data.personas || []; })
        .catch(() => {});
});

function loadPersona(idx) {
    if (!personas[idx]) return;
    const p = personas[idx];
    document.getElementById("name").value = p.name;
    document.getElementById("age").value = p.age;
    document.getElementById("background").value = p.background;
    document.getElementById("interests").value = p.interests;
    document.getElementById("skill_level").value = p.skill_level;
    document.getElementById("preference").value = p.preference;
    document.getElementById("goal").value = p.goal;
    document.getElementById("num_items").value = p.num_items;
    showToast(`Loaded "${p.title}" persona`);
}

async function handleRecommend(e) {
    if (e) e.preventDefault();

    const btn = document.getElementById("generateBtn");
    btn.querySelector(".btn-text").style.display = "none";
    btn.querySelector(".btn-spinner").style.display = "inline-flex";
    btn.disabled = true;

    currentProfile = {
        name: document.getElementById("name").value.trim(),
        age: document.getElementById("age").value.trim(),
        background: document.getElementById("background").value.trim(),
        interests: document.getElementById("interests").value.trim(),
        skill_level: document.getElementById("skill_level").value,
        preference: document.getElementById("preference").value.trim(),
        goal: document.getElementById("goal").value.trim(),
        num_items: parseInt(document.getElementById("num_items").value, 10)
    };

    try {
        const res = await fetch("/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(currentProfile)
        });

        const data = await res.json();
        if (!res.ok || !data.success) {
            throw new Error(data.error || "Recommendation error");
        }

        currentRecommendations = data.recommendations || [];
        renderRecommendations(currentRecommendations);
        showToast("Learning pathway synthesized successfully!");
    } catch (err) {
        alert("Recommendation generation failed: " + err.message);
    } finally {
        btn.querySelector(".btn-text").style.display = "inline-flex";
        btn.querySelector(".btn-spinner").style.display = "none";
        btn.disabled = false;
    }
}

function renderRecommendations(items) {
    const emptyState = document.getElementById("emptyState");
    const container = document.getElementById("resultsContent");
    const list = document.getElementById("recList");

    emptyState.style.display = "none";
    container.style.display = "block";
    list.innerHTML = "";

    if (!items || items.length === 0) {
        list.innerHTML = "<p class='no-recs'>No recommendations returned. Please retry.</p>";
        return;
    }

    items.forEach((item, index) => {
        const score = item.score || 90;
        const card = document.createElement("div");
        card.className = "rec-card";

        const difficultyClass = (item.difficulty || "Intermediate").toLowerCase();

        card.innerHTML = `
            <div class="rec-card-top">
                <div class="rec-rank-badge">#${index + 1}</div>
                <div class="rec-title-wrap">
                    <h4>${escapeHtml(item.name || "Resource")}</h4>
                    <div class="rec-tags">
                        <span class="tag-type">${escapeHtml(item.type || "Course")}</span>
                        <span class="tag-diff diff-${difficultyClass}">${escapeHtml(item.difficulty || "Intermediate")}</span>
                    </div>
                </div>
                <div class="rec-score-badge">
                    <span class="score-number">${score}%</span>
                    <span class="score-sub">Match</span>
                </div>
            </div>

            <div class="score-meter">
                <div class="score-bar" style="width: ${score}%;"></div>
            </div>

            <div class="rec-reason-box">
                <span class="reason-label">XAI RATIONALE:</span>
                <p>${escapeHtml(item.reason || "Curated based on your background and target career milestones.")}</p>
            </div>
        `;
        list.appendChild(card);
    });
}

function openRefineModal() {
    document.getElementById("refineModal").classList.add("open");
    document.getElementById("feedbackText").focus();
}

function closeRefineModal() {
    document.getElementById("refineModal").classList.remove("open");
}

async function submitRefinement() {
    const feedback = document.getElementById("feedbackText").value.trim();
    if (!feedback) {
        alert("Please enter feedback before submitting.");
        return;
    }

    const btn = document.getElementById("submitRefineBtn");
    btn.disabled = true;
    btn.textContent = "Refining...";

    try {
        const res = await fetch("/refine", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                profile: currentProfile,
                feedback: feedback
            })
        });

        const data = await res.json();
        if (!res.ok || !data.success) {
            throw new Error(data.error || "Refinement failed");
        }

        currentRecommendations = data.recommendations || [];
        renderRecommendations(currentRecommendations);
        closeRefineModal();
        document.getElementById("feedbackText").value = "";
        showToast("Curriculum refined based on your critique!");
    } catch (err) {
        alert("Refinement failed: " + err.message);
    } finally {
        btn.disabled = false;
        btn.textContent = "Apply Refinement";
    }
}

async function saveToSyllabus() {
    if (!currentRecommendations || currentRecommendations.length === 0) {
        showToast("Please generate recommendations first!");
        return;
    }

    try {
        const res = await fetch("/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ recommendations: currentRecommendations })
        });
        const data = await res.json();
        showToast(data.message || "Saved to recommendations.txt");
    } catch (e) {
        showToast("Error saving recommendations");
    }
}

function showToast(msg) {
    const t = document.getElementById("toast");
    t.textContent = msg;
    t.classList.add("visible");
    setTimeout(() => t.classList.remove("visible"), 2500);
}

function escapeHtml(str) {
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
