import streamlit as st
import requests

st.set_page_config(page_title="LinkedIn AI Assistant", page_icon="🤖")

st.title("LinkedIn AI Assistant")
st.caption("Paste conversation, pick a tone, generate a human-quality draft. No auto-sending.")

backend_url = st.text_input(
    "Backend URL",
    value="https://linkedin-ai-assistant-backend.onrender.com"
)

with st.form("gen_form"):
    conversation = st.text_area(
        "Paste conversation or last message", 
        height=240, 
        help="Copy from LinkedIn and paste here.",
        placeholder="e.g., Hi! I saw your profile and was impressed with your experience..."
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        tone = st.selectbox(
            "Tone", 
            ["friendly", "formal", "concise", "enthusiastic", "empathetic", "neutral"], 
            index=0
        )
    with col2:
        language = st.selectbox("Language", ["English", "Urdu", "Hindi", "Arabic"], index=0)
    with col3:
        max_words = st.slider("Max words", 60, 300, value=120, step=10)

    submitted = st.form_submit_button("Generate Reply", type="primary")

if submitted:
    if not conversation.strip():
        st.error("Please paste some conversation text.")
    else:
        try:
            # Wake up backend with proper error handling
            with st.spinner("Waking up backend..."):
                try:
                    health_resp = requests.get(
                        f"{backend_url}/health", 
                        timeout=10
                    )
                    if not health_resp.ok:
                        st.warning("Backend is slow to respond. This might take a moment...")
                except:
                    pass  # It's okay if health check fails

            # Send main request with spinner
            with st.spinner("Crafting your reply..."):
                resp = requests.post(
                    f"{backend_url}/suggest_reply",
                    json={
                        "conversation": conversation,
                        "tone": tone,
                        "language": language,
                        "max_words": max_words
                    },
                    timeout=90  # Reduced timeout
                )
            
            # Simplified response handling
            if resp.status_code == 200:
                reply = resp.json().get("reply_text", "")
                st.text_area("Suggested Reply", value=reply, height=180)
                st.success("✅ Ready to copy! (Ctrl/Cmd+C)")
            else:
                st.error(f"Backend error ({resp.status_code}): {resp.text[:200]}...")

        except requests.exceptions.Timeout:
            st.error("Request timed out. The backend might be overloaded. Please try again.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
