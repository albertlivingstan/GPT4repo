/* =====================================================
   BLOG BOT - FRONTEND JAVASCRIPT
===================================================== */


/* =====================================================
   ELEMENTS
===================================================== */

const topicInput =
    document.getElementById("blogTopic");

const styleInput =
    document.getElementById("writingStyle");

const toneInput =
    document.getElementById("tone");

const audienceInput =
    document.getElementById("audience");

const wordCountInput =
    document.getElementById("wordCount");

const instructionsInput =
    document.getElementById("instructions");

const generateBtn =
    document.getElementById("generateBtn");

const articleResult =
    document.getElementById("articleResult");

const loadingOverlay =
    document.getElementById("loadingOverlay");

const copyBtn =
    document.getElementById("copyBtn");

const downloadBtn =
    document.getElementById("downloadBtn");

const newChatBtn =
    document.getElementById("newChatBtn");

const assistantInput =
    document.getElementById("assistantInput");

const assistantSend =
    document.getElementById("assistantSend");

const assistantResponse =
    document.getElementById("assistantResponse");


/* =====================================================
   SHOW LOADING
===================================================== */

function showLoading() {

    loadingOverlay.classList.add("show");

    generateBtn.disabled = true;

}


/* =====================================================
   HIDE LOADING
===================================================== */

function hideLoading() {

    loadingOverlay.classList.remove("show");

    generateBtn.disabled = false;

}


/* =====================================================
   FORMAT GENERATED CONTENT
===================================================== */

function formatBlog(content) {

    if (!content) {
        return "";
    }


    let html = content;


    /*
        Convert escaped HTML characters
    */

    html = html
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");


    /*
        Headings
    */

    html = html.replace(
        /^### (.*)$/gm,
        "<h3>$1</h3>"
    );


    html = html.replace(
        /^## (.*)$/gm,
        "<h2>$1</h2>"
    );


    html = html.replace(
        /^# (.*)$/gm,
        "<h1>$1</h1>"
    );


    /*
        Bold
    */

    html = html.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );


    /*
        Bullet points
    */

    html = html.replace(
        /^\s*[-*]\s+(.*)$/gm,
        "<li>$1</li>"
    );


    /*
        Numbered lists
    */

    html = html.replace(
        /^\s*\d+\.\s+(.*)$/gm,
        "<li>$1</li>"
    );


    /*
        Line breaks
    */

    html = html.replace(
        /\n\n+/g,
        "</p><p>"
    );


    html = html.replace(
        /\n/g,
        "<br>"
    );


    /*
        Avoid wrapping headings
    */

    html =
        "<p>" +
        html +
        "</p>";


    html = html.replace(
        /<p>\s*(<h[1-3]>)/g,
        "$1"
    );


    html = html.replace(
        /(<\/h[1-3]>)\s*<\/p>/g,
        "$1"
    );


    return html;

}


/* =====================================================
   GENERATE BLOG
===================================================== */

async function generateBlog() {

    const topic =
        topicInput.value.trim();


    if (!topic) {

        topicInput.focus();

        topicInput.style.borderColor =
            "#d95d39";

        setTimeout(() => {

            topicInput.style.borderColor =
                "";

        }, 1500);

        return;

    }


    const data = {

        topic: topic,

        writing_style:
            styleInput.value,

        tone:
            toneInput.value,

        target_audience:
            audienceInput.value,

        word_count:
            wordCountInput.value,

        additional_instructions:
            instructionsInput.value.trim()

    };


    showLoading();


    try {

        /*
         * Flask endpoint
         *
         * Change /generate-blog only if
         * your Python route uses another URL.
         */

        const response =
            await fetch("/generate-blog", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(data)

            });


        if (!response.ok) {

            throw new Error(
                "Server returned an error."
            );

        }


        const result =
            await response.json();


        /*
         * Support common response names.
         */

        const content =
            result.blog ||
            result.content ||
            result.response ||
            result.generated_blog ||
            result.message;


        if (!content) {

            throw new Error(
                "No generated content received."
            );

        }


        articleResult.innerHTML = `

            <div class="generated-blog">

                ${formatBlog(content)}

            </div>

        `;


        /*
         * Scroll to result
         */

        articleResult.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


    }

    catch (error) {

        console.error(error);


        articleResult.innerHTML = `

            <div class="empty-result">

                <div class="empty-icon">
                    !
                </div>

                <h3>
                    Something went wrong
                </h3>

                <p>
                    ${error.message}
                </p>

            </div>

        `;

    }

    finally {

        hideLoading();

    }

}


/* =====================================================
   GENERATE BUTTON
===================================================== */

generateBtn.addEventListener(
    "click",
    generateBlog
);


/* =====================================================
   ENTER KEY
===================================================== */

topicInput.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter"
        ) {

            event.preventDefault();

            generateBlog();

        }

    }
);


/* =====================================================
   COPY ARTICLE
===================================================== */

copyBtn.addEventListener(
    "click",
    async function () {

        const blog =
            document.querySelector(
                ".generated-blog"
            );


        if (!blog) {

            return;

        }


        try {

            await navigator.clipboard.writeText(
                blog.innerText
            );


            const original =
                copyBtn.textContent;


            copyBtn.textContent =
                "Copied ✓";


            setTimeout(() => {

                copyBtn.textContent =
                    original;

            }, 1500);

        }

        catch (error) {

            console.error(error);

        }

    }
);


/* =====================================================
   DOWNLOAD ARTICLE
===================================================== */

downloadBtn.addEventListener(
    "click",
    function () {

        const blog =
            document.querySelector(
                ".generated-blog"
            );


        if (!blog) {

            return;

        }


        const title =
            topicInput.value.trim() ||
            "BlogBot Article";


        const content = `

            <!DOCTYPE html>

            <html>

            <head>

                <meta charset="UTF-8">

                <title>${title}</title>

            </head>

            <body>

                ${blog.innerHTML}

            </body>

            </html>

        `;


        const blob =
            new Blob(
                [content],
                {
                    type:
                        "text/html"
                }
            );


        const url =
            URL.createObjectURL(blob);


        const link =
            document.createElement("a");


        link.href = url;

        link.download =
            `${title.replace(
                /[^a-z0-9]/gi,
                "_"
            )}.html`;


        document.body.appendChild(link);

        link.click();

        link.remove();


        URL.revokeObjectURL(url);

    }
);


/* =====================================================
   NEW ARTICLE
===================================================== */

newChatBtn.addEventListener(
    "click",
    function () {

        topicInput.value = "";

        instructionsInput.value = "";

        styleInput.value =
            "Professional";

        toneInput.value =
            "Friendly";

        audienceInput.value =
            "Engineering Students";

        wordCountInput.value =
            "500";


        articleResult.innerHTML = `

            <div class="empty-result">

                <div class="empty-icon">
                    ✦
                </div>

                <h3>
                    Your article will appear here
                </h3>

                <p>
                    Enter your topic above and click
                    <strong>Generate Article</strong>.
                </p>

            </div>

        `;


        topicInput.focus();


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }
);


/* =====================================================
   QUICK ASSISTANT
===================================================== */

document
    .querySelectorAll(
        ".quick-actions button"
    )
    .forEach(button => {

        button.addEventListener(
            "click",
            function () {

                assistantInput.value =
                    this.dataset.prompt;

                assistantInput.focus();

            }
        );

    });


/* =====================================================
   ASSISTANT REQUEST
===================================================== */

async function sendAssistantMessage() {

    const message =
        assistantInput.value.trim();


    if (!message) {

        assistantInput.focus();

        return;

    }


    assistantResponse.style.display =
        "block";


    assistantResponse.innerHTML = `
        <strong>BlogBot</strong>
        <br>
        Thinking...
    `;


    try {

        /*
         * If your Flask backend has a separate
         * assistant route, use it here.
         */

        const response =
            await fetch("/chat", {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body:
                    JSON.stringify({
                        message: message
                    })

            });


        if (!response.ok) {

            throw new Error(
                "Unable to contact BlogBot."
            );

        }


        const result =
            await response.json();


        const answer =
            result.response ||
            result.message ||
            result.content;


        assistantResponse.innerHTML = `

            <strong>BlogBot</strong>

            <br><br>

            ${answer
                ? formatBlog(answer)
                : "No response received."
            }

        `;

    }

    catch (error) {

        assistantResponse.innerHTML = `

            <strong>BlogBot</strong>

            <br><br>

            I couldn't process that request.
            Please try again.

        `;

        console.error(error);

    }

}


assistantSend.addEventListener(
    "click",
    sendAssistantMessage
);


assistantInput.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter"
        ) {

            event.preventDefault();

            sendAssistantMessage();

        }

    }
);