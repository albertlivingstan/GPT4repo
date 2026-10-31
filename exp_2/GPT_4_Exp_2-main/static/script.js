/**
 * BlogStudio Pro — Advanced Client Engine
 */

let currentArticleMarkdown = "";
let currentArticleStats = null;
let currentArticleTitle = "Untitled Article";

document.addEventListener("DOMContentLoaded", () => {
    loadModels();
    loadHistoryCount();
    setupDropdown();
});

// ==========================================
// API & MODEL LOADING
// ==========================================

async function loadModels() {
    try {
        const res = await fetch("/api/models");
        if (res.ok) {
            const data = await res.json();
            const select = document.getElementById("modelSelector");
            select.innerHTML = "";
            (data.models || ["llama3.2"]).forEach(m => {
                const opt = document.createElement("option");
                opt.value = m;
                opt.textContent = m + (m === data.active ? " (Active)" : "");
                if (m === data.active) opt.selected = true;
                select.appendChild(opt);
            });
        }
    } catch (e) {
        console.warn("Could not load model list:", e);
    }
}

async function loadHistoryCount() {
    try {
        const res = await fetch("/api/history");
        if (res.ok) {
            const data = await res.json();
            const count = (data.articles || []).length;
            document.getElementById("historyCount").textContent = count;
        }
    } catch (e) {
        console.warn("Could not load history count:", e);
    }
}

// ==========================================
// TAB & VIEW SWITCHERS
// ==========================================

function switchPanelTab(tab) {
    const builderBtn = document.getElementById("tabBuilderBtn");
    const ideateBtn = document.getElementById("tabIdeateBtn");
    const builderContent = document.getElementById("tabBuilder");
    const ideateContent = document.getElementById("tabIdeate");

    if (tab === "builder") {
        builderBtn.classList.add("active");
        ideateBtn.classList.remove("active");
        builderContent.style.display = "block";
        ideateContent.style.display = "none";
    } else {
        ideateBtn.classList.add("active");
        builderBtn.classList.remove("active");
        builderContent.style.display = "none";
        ideateContent.style.display = "block";
    }
}

function switchView(view) {
    const previewBtn = document.getElementById("viewPreviewBtn");
    const markdownBtn = document.getElementById("viewMarkdownBtn");
    const insightsBtn = document.getElementById("viewInsightsBtn");

    const canvasPreview = document.getElementById("canvasPreview");
    const canvasMarkdown = document.getElementById("canvasMarkdown");
    const canvasInsights = document.getElementById("canvasInsights");

    [previewBtn, markdownBtn, insightsBtn].forEach(b => b.classList.remove("active"));
    [canvasPreview, canvasMarkdown, canvasInsights].forEach(c => c.style.display = "none");

    if (view === "preview") {
        previewBtn.classList.add("active");
        canvasPreview.style.display = "block";
    } else if (view === "markdown") {
        markdownBtn.classList.add("active");
        canvasMarkdown.style.display = "block";
        // Sync editor if user modified markdown
        document.getElementById("markdownEditor").value = currentArticleMarkdown;
    } else if (view === "insights") {
        insightsBtn.classList.add("active");
        canvasInsights.style.display = "block";
        updateInsightsTab();
    }
}

// ==========================================
// ARTICLE GENERATION
// ==========================================

async function handleGenerate(e) {
    if (e) e.preventDefault();

    const topic = document.getElementById("blogTopic").value.trim();
    if (!topic) {
        showToast("Please enter an article topic first.");
        return;
    }

    const payload = {
        topic: topic,
        style: document.getElementById("writingStyle").value,
        tone: document.getElementById("tone").value,
        audience: document.getElementById("audience").value,
        wordCount: parseInt(document.getElementById("wordCount").value, 10),
        keywords: document.getElementById("seoKeywords").value.trim(),
        instructions: document.getElementById("instructions").value.trim(),
        model: document.getElementById("modelSelector").value,
        include_takeaways: document.getElementById("includeTakeaways").checked,
        include_faq: document.getElementById("includeFaq").checked,
        include_toc: document.getElementById("includeToc").checked
    };

    setGenerateLoading(true);

    try {
        const res = await fetch("/generate-blog", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok || data.error) {
            throw new Error(data.error || "Generation error");
        }

        currentArticleMarkdown = data.blog || data.content || data.response || "";
        currentArticleStats = data.stats || {};
        currentArticleTitle = topic;

        displayGeneratedArticle();
        loadHistoryCount();
        showToast("Article generated successfully!");

    } catch (err) {
        alert("Generation failed: " + err.message);
    } finally {
        setGenerateLoading(false);
    }
}

function setGenerateLoading(isLoading) {
    const btn = document.getElementById("generateBtn");
    const idleSpan = btn.querySelector(".btn-idle");
    const loadSpan = btn.querySelector(".btn-loading");

    if (isLoading) {
        idleSpan.style.display = "none";
        loadSpan.style.display = "inline-flex";
        btn.disabled = true;
    } else {
        idleSpan.style.display = "inline-flex";
        loadSpan.style.display = "none";
        btn.disabled = false;
    }
}

function displayGeneratedArticle() {
    const emptyState = document.getElementById("emptyState");
    const rendered = document.getElementById("renderedArticle");
    const editor = document.getElementById("markdownEditor");
    const metricsBar = document.getElementById("metricsBar");
    const inlineAiBar = document.getElementById("inlineAiBar");

    emptyState.style.display = "none";
    rendered.style.display = "block";
    metricsBar.style.display = "flex";
    inlineAiBar.style.display = "flex";

    // Convert markdown to clean HTML
    rendered.innerHTML = parseMarkdownToHTML(currentArticleMarkdown);
    editor.value = currentArticleMarkdown;

    // Update Stats Bar
    if (currentArticleStats) {
        document.getElementById("statWords").textContent = currentArticleStats.word_count || 0;
        document.getElementById("statReadingTime").textContent = (currentArticleStats.reading_time_min || 1) + " min";
        document.getElementById("statFleschScore").textContent = (currentArticleStats.flesch_score || 0) + "/100";
        document.getElementById("statTime").textContent = (currentArticleStats.generation_time_sec || 0) + "s";
    }

    switchView("preview");
}

// Sync markdown editor changes back to preview
document.getElementById("markdownEditor").addEventListener("input", function() {
    currentArticleMarkdown = this.value;
    document.getElementById("renderedArticle").innerHTML = parseMarkdownToHTML(currentArticleMarkdown);
});

// ==========================================
// INLINE AI TOOLS & REFINEMENT
// ==========================================

async function refineArticle(action) {
    if (!currentArticleMarkdown) {
        showToast("No generated text to polish yet!");
        return;
    }

    showToast(`Polishing article (${action})...`);

    try {
        const res = await fetch("/api/refine", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: currentArticleMarkdown,
                action: action,
                model: document.getElementById("modelSelector").value
            })
        });

        const data = await res.json();
        if (data.success && data.revised) {
            currentArticleMarkdown = data.revised;
            displayGeneratedArticle();
            showToast("Article updated with AI revision!");
        } else {
            showToast("Revision failed: " + (data.error || "Unknown error"));
        }
    } catch (e) {
        showToast("Error during AI polishing: " + e.message);
    }
}

// ==========================================
// AI IDEATOR / BRAINSTORMER
// ==========================================

async function runQuickAssist(type) {
    const input = document.getElementById("assistInput").value.trim() || document.getElementById("blogTopic").value.trim();
    if (!input) {
        showToast("Please enter a subject or niche first!");
        document.getElementById("assistInput").focus();
        return;
    }

    const outputBox = document.getElementById("ideateOutput");
    const outputText = document.getElementById("ideateText");
    const outputLabel = document.getElementById("outputTypeLabel");

    outputBox.style.display = "block";
    outputText.textContent = "AI is thinking...";
    outputLabel.textContent = `IDEATING: ${type.toUpperCase()}`;

    try {
        const res = await fetch("/api/quick-assist", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                type: type,
                input: input,
                model: document.getElementById("modelSelector").value
            })
        });

        const data = await res.json();
        if (data.success) {
            outputText.textContent = data.response;
        } else {
            outputText.textContent = "Error: " + (data.error || "Failed to generate suggestions");
        }
    } catch (e) {
        outputText.textContent = "Request error: " + e.message;
    }
}

function copyIdeateOutput() {
    const text = document.getElementById("ideateText").textContent;
    navigator.clipboard.writeText(text);
    showToast("Copied brainstorm output!");
}

// ==========================================
// SAMPLE DATA & UTILS
// ==========================================

function suggestRandomTopic() {
    const sampleTopics = [
        "Autonomous AI Agents: How They Are Reshaping Software Engineering",
        "Building Resilient Event-Driven Microservices with Kafka and Go",
        "The Definitive Guide to Vector Embeddings and Hybrid RAG Search",
        "Zero-Trust Cloud Security Architecture for Modern Kubernetes Clusters",
        "Designing Scalable GraphQL APIs: Best Practices and Pitfalls",
        "How Quantum Computing Will Impact Public Key Cryptography"
    ];
    const picked = sampleTopics[Math.floor(Math.random() * sampleTopics.length)];
    document.getElementById("blogTopic").value = picked;
    showToast("Loaded topic suggestion!");
}

function loadSampleTopic(topic) {
    document.getElementById("blogTopic").value = topic;
    switchPanelTab("builder");
    document.getElementById("blogTopic").scrollIntoView({ behavior: "smooth" });
}

// ==========================================
// INSIGHTS TAB UPDATE
// ==========================================

function updateInsightsTab() {
    if (!currentArticleStats) return;

    document.getElementById("insightWords").textContent = currentArticleStats.word_count || 0;
    document.getElementById("insightSentences").textContent = currentArticleStats.sentence_count || 0;
    document.getElementById("insightChars").textContent = currentArticleStats.character_count || 0;
    document.getElementById("insightGrade").textContent = currentArticleStats.grade || "--";

    // Checklist tests
    const md = currentArticleMarkdown;
    document.getElementById("checkH1").textContent = /^#\s+.+/m.test(md) ? "✓ H1 Primary Title Present" : "✗ H1 Title Missing";
    document.getElementById("checkSubheads").textContent = /^##\s+.+/m.test(md) ? "✓ H2/H3 Architecture Implemented" : "✗ Needs H2 Subheadings";
    document.getElementById("checkTakeaways").textContent = md.includes("Takeaways") || md.includes(">") ? "✓ Key Takeaways Callout Included" : "✗ No Takeaways Callout";
    document.getElementById("checkFAQ").textContent = md.includes("Frequently Asked") || md.includes("FAQ") ? "✓ FAQ Section Included" : "✗ FAQ Missing";
    document.getElementById("checkLength").textContent = (currentArticleStats.word_count >= 400) ? "✓ Optimal Word Count (400+ words)" : "✗ Short Article (< 400 words)";
}

// ==========================================
// EXPORT & CLIPBOARD
// ==========================================

function copyArticle() {
    if (!currentArticleMarkdown) {
        showToast("Nothing to copy yet!");
        return;
    }
    navigator.clipboard.writeText(currentArticleMarkdown);
    showToast("Markdown copied to clipboard!");
}

function exportArticle(format) {
    if (!currentArticleMarkdown) {
        showToast("Generate an article first!");
        return;
    }

    const safeTitle = (currentArticleTitle || "article").replace(/[^a-z0-9]/gi, "_").toLowerCase();
    let content = "";
    let mime = "";
    let ext = "";

    if (format === "markdown") {
        content = currentArticleMarkdown;
        mime = "text/markdown";
        ext = "md";
    } else if (format === "text") {
        // Strip markdown tags
        content = currentArticleMarkdown.replace(/#+\s/g, "").replace(/\*\*/g, "").replace(/>\s/g, "");
        mime = "text/plain";
        ext = "txt";
    } else if (format === "html") {
        content = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>${currentArticleTitle}</title><style>body{font-family:sans-serif;line-height:1.6;max-width:800px;margin:40px auto;padding:0 20px;}blockquote{border-left:4px solid #6366f1;padding-left:16px;color:#4b5563;background:#f3f4f6;margin:16px 0;}</style></head><body>${parseMarkdownToHTML(currentArticleMarkdown)}</body></html>`;
        mime = "text/html";
        ext = "html";
    }

    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${safeTitle}.${ext}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`Exported as .${ext}`);
}

// ==========================================
// HISTORY DRAWER
// ==========================================

document.getElementById("historyModalBtn").addEventListener("click", openHistoryModal);
document.getElementById("newArticleBtn").addEventListener("click", () => {
    document.getElementById("blogTopic").value = "";
    document.getElementById("seoKeywords").value = "";
    document.getElementById("instructions").value = "";
    currentArticleMarkdown = "";
    currentArticleStats = null;
    document.getElementById("emptyState").style.display = "block";
    document.getElementById("renderedArticle").style.display = "none";
    document.getElementById("metricsBar").style.display = "none";
    document.getElementById("inlineAiBar").style.display = "none";
    showToast("Cleared for a fresh draft.");
});

async function openHistoryModal() {
    const modal = document.getElementById("historyModal");
    const list = document.getElementById("historyList");
    modal.classList.add("open");
    list.innerHTML = "<p class='history-empty'>Loading past articles...</p>";

    try {
        const res = await fetch("/api/history");
        const data = await res.json();
        const articles = data.articles || [];

        if (articles.length === 0) {
            list.innerHTML = "<p class='history-empty'>No articles saved yet. Generate an article to see it here!</p>";
            return;
        }

        list.innerHTML = "";
        articles.forEach(art => {
            const item = document.createElement("div");
            item.className = "history-item";
            const dateStr = art.created_at ? new Date(art.created_at).toLocaleString() : "";
            item.innerHTML = `
                <div class="history-item-info">
                    <h4>${escapeHtml(art.topic || "Untitled")}</h4>
                    <span class="history-meta">${dateStr} • ${art.stats?.word_count || 0} words • ${art.params?.model || "AI"}</span>
                </div>
                <button class="load-btn" onclick="loadHistoricalArticle('${art.id}')">Load ↗</button>
            `;
            list.appendChild(item);
        });
    } catch (e) {
        list.innerHTML = "<p class='history-empty'>Could not load history: " + e.message + "</p>";
    }
}

function closeHistoryModal() {
    document.getElementById("historyModal").classList.remove("open");
}

async function loadHistoricalArticle(articleId) {
    try {
        const res = await fetch(`/api/article/${articleId}`);
        const data = await res.json();
        if (data.content) {
            currentArticleMarkdown = data.content;
            currentArticleStats = data.meta?.stats || {};
            currentArticleTitle = data.meta?.topic || "Saved Article";
            document.getElementById("blogTopic").value = currentArticleTitle;
            displayGeneratedArticle();
            closeHistoryModal();
            showToast("Loaded saved article!");
        }
    } catch (e) {
        showToast("Error loading article: " + e.message);
    }
}

// ==========================================
// TOAST & DROPDOWNS
// ==========================================

function showToast(msg) {
    const t = document.getElementById("toast");
    t.textContent = msg;
    t.classList.add("visible");
    setTimeout(() => t.classList.remove("visible"), 2500);
}

function setupDropdown() {
    const dropdown = document.querySelector(".dropdown");
    if (!dropdown) return;
    const btn = dropdown.querySelector(".dropdown-btn");
    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        dropdown.classList.toggle("open");
    });
    document.addEventListener("click", () => dropdown.classList.remove("open"));
}

// ==========================================
// MARKDOWN PARSER UTILITY
// ==========================================

function parseMarkdownToHTML(md) {
    if (!md) return "";

    let html = escapeHtml(md);

    // Code blocks
    html = html.replace(/```([a-z0-9]*)\n([\s\S]*?)```/gm, (match, lang, code) => {
        return `<pre class="code-block"><code class="lang-${lang}">${code.trim()}</code></pre>`;
    });

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');

    // Headings
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Blockquotes
    html = html.replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>');

    // Bold & Italics
    html = html.replace(/\*\*\*(.*?)\*\*\*/gim, '<b><i>$1</i></b>');
    html = html.replace(/\*\*(.*?)\*\*/gim, '<b>$1</b>');
    html = html.replace(/\*(.*?)\*/gim, '<i>$1</i>');

    // Unordered lists
    html = html.replace(/^\s*[\-\*]\s+(.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>[\s\S]*?<\/li>)/gm, '<ul>$1</ul>');
    // Deduplicate nested <ul> tags
    html = html.replace(/<\/ul>\s*<ul>/g, '');

    // Paragraphs: separate by empty lines
    const paragraphs = html.split(/\n{2,}/);
    html = paragraphs.map(p => {
        p = p.trim();
        if (!p) return "";
        if (p.startsWith("<h") || p.startsWith("<ul") || p.startsWith("<pre") || p.startsWith("<blockquote")) {
            return p;
        }
        return `<p>${p.replace(/\n/g, "<br>")}</p>`;
    }).join("\n");

    return html;
}

function escapeHtml(str) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}
