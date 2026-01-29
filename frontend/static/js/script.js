const API_URL = "http://127.0.0.1:8000";

$(document).ready(function() {
    
    // --- @Mention Autocomplete Logic ---
    function splitCurrent(val) {
        return val.split(/ \s*/);
    }
    function extractLast(term) {
        return splitCurrent(term).pop();
    }

    $("#user-input")
        .on("keydown", function(event) {
            // Prevent navigating out if menu is active
            if (event.keyCode === $.ui.keyCode.TAB && $(this).autocomplete("instance").menu.active) {
                event.preventDefault();
            }
            // Send on Enter key
            if (event.keyCode === 13 && !$(this).autocomplete("instance").menu.active) {
                sendMessage();
            }
        })
        .autocomplete({
            source: function(request, response) {
                var term = extractLast(request.term);
                // Trigger only if term starts with @ and has at least 1 char after it
                if (term.length >= 2 && term.startsWith("@")) {
                    var query = term.substring(1); // Remove @
                    $.getJSON(API_URL + "/suggest_names", { prefix: query }, response);
                } else {
                    response([]);
                }
            },
            search: function() {
                var term = extractLast(this.value);
                if (term.length < 2 || !term.startsWith("@")) {
                    return false;
                }
            },
            focus: function() { return false; },
            select: function(event, ui) {
                var terms = splitCurrent(this.value);
                terms.pop(); // remove current input
                terms.push(ui.item.value); // add selected
                terms.push(""); // add space
                this.value = terms.join(" ");
                return false;
            }
        });

    // --- Chat Logic ---
    window.sendMessage = function() {
        const input = document.getElementById("user-input");
        const msg = input.value.trim();
        if (!msg) return;

        // 1. Add User Message to UI
        $("#chat-box").append(`<div class="message user-msg">${escapeHtml(msg)}</div>`);
        input.value = "";
        scrollToBottom();

        // 2. Show Loading Indicator (Optional)
        const loadingId = "loading-" + Date.now();
        $("#chat-box").append(`<div class="message bot-msg text-muted" id="${loadingId}">Typing...</div>`);
        scrollToBottom();

        // 3. Call Backend API
        fetch(API_URL + "/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg, session_id: "user-123" }) // Simple session ID
        })
        .then(res => res.json())
        .then(data => {
            // Remove loading
            $(`#${loadingId}`).remove();
            
            // Build Bot Response
            let content = `<strong>AI:</strong> ${data.response}`;
            
            // Append Charts
            if (data.charts && data.charts.length > 0) {
                data.charts.forEach(img => {
                    content += `<br><img src="data:image/png;base64,${img}" class="chart-img">`;
                });
            }

            // Append Debug SQL (Optional, good for MVP)
            if (data.sql_debug) {
                content += `<div class="mt-2 text-muted" style="font-size:0.8em; border-top:1px solid #ccc; padding-top:5px;">
                                <em>Executed: ${data.sql_debug}</em>
                            </div>`;
            }

            $("#chat-box").append(`<div class="message bot-msg">${content}</div>`);
            scrollToBottom();
        })
        .catch(err => {
            $(`#${loadingId}`).remove();
            $("#chat-box").append(`<div class="message bot-msg text-danger">Error: Could not connect to backend.</div>`);
        });
    };

    function scrollToBottom() {
        const chatBox = document.getElementById("chat-box");
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Basic XSS prevention
    function escapeHtml(text) {
        if (!text) return text;
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});