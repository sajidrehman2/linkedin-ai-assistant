import streamlit as st
import requests

st.set_page_config(page_title="LinkedIn AI Assistant", page_icon="🤖")

st.title("LinkedIn AI Assistant (Local)")
st.caption("Paste conversation, pick a tone, generate a human-quality draft. No auto-sending.")

backend_url = st.text_input(
    "Backend URL",
    value="https://linkedin-ai-assistant-backend.onrender.com"
)

with st.form("gen_form"):
    conversation = st.text_area(
        "Paste conversation or last message", 
        height=240, 
        help="Copy from LinkedIn and paste here."
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

    submitted = st.form_submit_button("Generate Reply")

if submitted:
    if not conversation.strip():
        st.error("Please paste some conversation text.")
    else:
        try:
            # ✅ Wake up backend
            st.info("Waking up backend, please wait...")
            try:
                requests.get(f"{backend_url}/health", timeout=30)
            except:
                pass

            # ✅ Send main request with spinner
            with st.spinner("Generating reply..."):
                resp = requests.post(
                    f"{backend_url}/suggest_reply",
                    json={
                        "conversation": conversation,
                        "tone": tone,
                        "language": language,
                        "max_words": max_words
                    },
                    timeout=120
                )
            
            # CORRECTED INDENTATION LEVEL
            if resp.ok:
                reply = resp.json().get("reply_text", "")
                st.text_area("Draft Reply", value=reply, height=180)
                st.info("Select the text above and copy using Ctrl/Cmd+C")
            else:
                st.error(f"Error: {resp.status_code} - {resp.text}")

        except requests.exceptions.ReadTimeout:
            st.error("Request timed out. The backend may be waking up. Please try again in a few seconds.")
        except Exception as e:
            st.error(f"Request failed: {e}")

