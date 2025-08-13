// Minimal content script that adds a floating button on LinkedIn pages.
// It gathers visible messages, asks your local backend for a draft reply, and inserts it.
// It does NOT auto-send.

(function() {
  function ensureButton() {
    if (document.getElementById("ai-draft-btn")) return;
    const btn = document.createElement("div");
    btn.id = "ai-draft-btn";
    btn.innerText = "Draft with AI";
    document.body.appendChild(btn);
    btn.addEventListener("click", onDraftClick);
  }

  async function collectConversation() {
    // Try to collect visible message bubbles text. LinkedIn DOM is complex and may change.
    // We fallback to grabbing text from typical message bubble containers.
    const selectors = [
      '[data-test-conversation-container]',
      '.msg-s-message-list__event',     // older
      '.msg-s-message-list__entity-lockup',
      '.msg-conversation-listitem__message-snippet',
      '[role="dialog"] .msg-conversation-content', // popout
      '.msg-conversation-container__convo-scroller'
    ];
    let text = "";
    for (const sel of selectors) {
      document.querySelectorAll(sel).forEach(node => {
        const t = node.innerText;
        if (t && t.length > 0) {
          text += t + "\n";
        }
      });
      if (text.length > 0) break;
    }
    // If nothing found, fallback to the entire page text (last resort)
    if (!text) {
      text = document.body.innerText.slice(-4000); // last ~4000 chars
    }
    return text.trim();
  }

  function findComposeBox() {
    // Try common selectors for the message compose editable area
    const candidates = [
      '[contenteditable="true"][role="textbox"]',
      'div.msg-form__contenteditable',
      'div[aria-label="Write a message…"]'
    ];
    for (const sel of candidates) {
      const el = document.querySelector(sel);
      if (el) return el;
    }
    return null;
  }

  async function onDraftClick() {
    const backend = "http://localhost:8000";
    const convo = await collectConversation();
    if (!convo) {
      alert("Could not read conversation. Try selecting messages and copy-paste into the Streamlit app.");
      return;
    }

    try {
      const res = await fetch(`${backend}/suggest_reply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation: convo,
          tone: "friendly",
          language: "English",
          max_words: 120
        })
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt);
      }
      const data = await res.json();
      const draft = data.reply_text || "";
      const box = findComposeBox();
      if (box) {
        // Insert draft into compose
        box.focus();
        // Clear current content if any:
        if (box.innerText) {
          // Try to clear via selection
          const range = document.createRange();
          range.selectNodeContents(box);
          const sel = window.getSelection();
          sel.removeAllRanges();
          sel.addRange(range);
          document.execCommand("delete");
        }
        // Insert text
        document.execCommand("insertText", false, draft);
      } else {
        // Fallback: copy to clipboard
        await navigator.clipboard.writeText(draft);
        alert("Draft copied to clipboard. Paste it into the message box.");
      }
    } catch (e) {
      console.error(e);
      alert("Draft failed: " + e.message);
    }
  }

  // Initialize
  const observer = new MutationObserver(() => ensureButton());
  observer.observe(document.documentElement, { childList: true, subtree: true });
  ensureButton();
})();