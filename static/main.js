const sendBtn = document.getElementById("send");
const queryBox = document.getElementById("query");
const chatBox = document.getElementById("chat");

// Utility to escape HTML safely
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// Render LLM response nicely
function renderLLMResponse(text) {
    // Convert line breaks to <br> and bold headings using **Heading**
    let html = escapeHtml(text)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");
    return html;
}

// Create a spinner element
function createSpinner() {
    const spinner = document.createElement("div");
    spinner.className = "spinner my-2";
    spinner.innerHTML = `
        <div class="flex items-center space-x-2">
            <div class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-blue-500"></div>
            <span class="text-gray-500">LLM is thinking...</span>
        </div>`;
    return spinner;
}

sendBtn.addEventListener("click", async () => {
    const query = queryBox.value.trim();
    if (!query) return;

    // Display user query
    chatBox.innerHTML += `<div class="text-right mb-2"><strong>You:</strong> ${escapeHtml(query)}</div>`;
    queryBox.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Add spinner
    const spinner = createSpinner();
    chatBox.appendChild(spinner);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send to backend
    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({query})
        });
        const data = await response.json();

        // Remove spinner
        spinner.remove();

        if (data.answer) {
            chatBox.innerHTML += `<div class="text-left mb-2 bg-blue-50 p-2 rounded">${renderLLMResponse(data.answer)}</div>`;
        } else if (data.error) {
            chatBox.innerHTML += `<div class="text-left text-red-500 mb-2">Error: ${escapeHtml(data.error)}</div>`;
        }
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
        spinner.remove();
        chatBox.innerHTML += `<div class="text-left text-red-500 mb-2">Error: ${escapeHtml(err)}</div>`;
    }
});
