import streamlit as st
import re

# --- Function to determine email importance ---
def determine_importance(text):
    keywords_high = ["urgent", "important", "immediate", "action required"]
    keywords_medium = ["reminder", "notice", "pending", "please review"]

    if any(word in text.lower() for word in keywords_high):
        return "🔴 High"
    elif any(word in text.lower() for word in keywords_medium):
        return "🟠 Medium"
    else:
        return "🟢 Low"

# --- Function to detect possible spam or fraudulent email ---
def detect_spam(text):
    spam_keywords = ["winner", "prize", "transfer", "click here", "subscription", "unsolicited", "free", "congratulations"]
    excessive_links = len(re.findall(r"https?://\S+", text)) > 2

    if any(word in text.lower() for word in spam_keywords) or excessive_links:
        return "⚠️ Possible spam or fraudulent email"
    return "✅ Does not seem to be spam"

# --- Function to analyze email content ---
def extract_key_info(text):
    sentences = text.split(". ")

    # Categorize email type
    if "course" in text.lower() or "certification" in text.lower():
        category = "📚 Education / Training"
    elif "discount" in text.lower() or "promotion" in text.lower():
        category = "💰 Offer / Promotion"
    elif "error" in text.lower() or "problem" in text.lower():
        category = "⚠️ Alert / Problem Report"
    elif "urgent" in text.lower() or "attention" in text.lower():
        category = "🚨 Urgent / Action Required"
    else:
        category = "📩 General"

    keywords = ["important", "attention", "notice", "offer", "discount", "error", "problem"]
    key_points = [sent.strip() for sent in sentences if any(word in sent.lower() for word in keywords)]

    return category, key_points[:3] if key_points else sentences[:3]

# --- Streamlit UI ---
st.title("📧 Email Analyzer")

email_info = st.text_area("✉️ Paste the sender and subject of the email")
email_body = st.text_area("📩 Paste the raw content of the email")

if st.button("🔍 Analyze Email"):
    category, key_points = extract_key_info(email_body)
    importance = determine_importance(email_body)
    spam_status = detect_spam(email_body)

    st.markdown(f"**📌 Sender & Subject:** {email_info}")
    st.markdown(f"**🧐 Email Type:** {category}")
    st.markdown(f"**🔥 Importance:** {importance}")
    st.markdown(f"**🚨 Spam / Security Check:** {spam_status}")
    st.markdown("**🔍 Key Points:**")
    
    for point in key_points:
        st.write(f"- {point}")
