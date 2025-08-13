document.getElementById("draft").addEventListener("click", async () => {
  const backend = document.getElementById("backend").value || "http://localhost:8000";

  // Run a script in the active tab to get page text and try to insert the reply
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.id) return;

  // Inject a function to collect conversation
  const [{ result: convo }] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => document.body.innerText.slice(-4000), // naive fallback
  });

  try {
    const res = await fetch(`${backend}/suggest_reply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        conversation: convo || "",
        tone: "friendly",
        language: "English",
        max_words: 120
      })
    });
    const data = await res.json();
    const draft = data.reply_text || "";

    // Try to insert draft into compose textbox
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (text) => {
        const candidates = [
          '[contenteditable="true"][role="textbox"]',
          'div.msg-form__contenteditable',
          'div[aria-label="Write a message…"]'
        ];
        let box = null;
        for (const sel of candidates) {
          const el = document.querySelector(sel);
          if (el) { box = el; break; }
        }
        if (box) {
          box.focus();
          document.execCommand("insertText", false, text);
          alert("Draft inserted. Review and click Send.");
        } else {
          navigator.clipboard.writeText(text);
          alert("Draft copied. Paste it into the message box.");
        }
      },
      args: [draft]
    });
  } catch (e) {
    alert("Draft failed: " + e.message);
  }
});