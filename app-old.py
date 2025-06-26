import streamlit as st
from PIL import Image
import io
from modules import ai_bot, schemes
from modules.crop_disease_detector import predict_crop_disease

# Set page config (works in v1.42.0)
st.set_page_config(page_title="Agricultural Assistance", layout="wide")

# Inject custom CSS for a modern, professional look
st.markdown("""
    <style>
        /* Overall app background */
        .stApp {
            background-color: #f8f9fa;
        }
        /* Button styling */
        .stButton > button {
            background-color: #0e6655;
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #117a65;
            color: white;
        }
        /* Header styling */
        .main-title {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #0e6655;
        }
        /* Header margin adjustments */
        h1, h2, h3, h4, h5, h6 {
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        /* Footer styling */
        .footer {
            font-size: 0.8rem;
            text-align: center;
            color: #888888;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #eaeaea;
        }
        /* Marquee styling */
        .marquee {
            white-space: nowrap;
            overflow: hidden;
            position: relative;
            background-color: #f8b400;
            color: white;
            padding: 10px 0;
        }
        .marquee div {
            display: inline-block;
            padding-left: 100%;
            animation: marquee 10s linear infinite;
        }
        @keyframes marquee {
            from { transform: translateX(0); }
            to { transform: translateX(-100%); }
        }
    </style>
    <script>
        function scrollToSection() {
            document.getElementById("section4").scrollIntoView({ behavior: 'smooth' });
        }
    </script>
""", unsafe_allow_html=True)

# Display Marquee only if not in Agricultural News section
if st.session_state.get("current_section") != "Agricultural News":
    st.markdown(
        """
        <div class="marquee">
            <a href="#" onclick="scrollToSection(); return false;" style="text-decoration: none; color: white;">
                <div>🚀 Click here to go to Agricultural News! 🚀</div>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Footer function to display at the bottom of the app
def footer():
    st.markdown('<div class="footer">Developed by Your Company Name © 2025</div>', unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["AI Chatbot", "Crop Disease Detection", "Government Schemes", "Agricultural News"])
st.session_state["current_section"] = section

# --- 1. AI Chatbot Section ---
if section == "AI Chatbot":
    st.markdown("<h1 class='main-title'>Agricultural Assistant Chatbot</h1>", unsafe_allow_html=True)
    ai_bot.chatbot_ui()

# --- 2. Crop Disease Detection Section ---
elif section == "Crop Disease Detection":
    st.markdown("<h1 class='main-title'>🌿 Crop Disease Detection</h1>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("📤 Upload Crop Image", type=["jpg", "jpeg", "png"], key="crop_upload")
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Crop Image", width=300)
        if st.button("🔍 Detect Disease"):
            with st.spinner("Analyzing the image... Please wait."):
                try:
                    results = predict_crop_disease(image)
                    st.subheader("🩺 Prediction Results")
                    st.write(f"**Disease:** {results['disease']}")
                    st.write(f"**Confidence:** {results['confidence'] * 100:.1f}%")
                    if "remedy" in results:
                        st.markdown("### 💊 Treatment Recommendation")
                        st.write(results["remedy"])
                    else:
                        st.write("The plant appears to be healthy. No treatment necessary.")
                except Exception as e:
                    st.error(f"🚨 An error occurred while processing the image: {e}")

# --- 3. Government Schemes Section ---
elif section == "Government Schemes":
    st.markdown("<h1 class='main-title'>Government Schemes Assistant Chatbot</h1>", unsafe_allow_html=True)
    schemes.chatbot_ui()

# --- 4. Agricultural News Section ---
elif section == "Agricultural News":
    st.markdown("<h1 id='section4' class='main-title'>Agricultural News</h1>", unsafe_allow_html=True)
    category = st.selectbox("Select news category", options=["All", "Policies", "Crop Prices", "Trends"])
    page = st.number_input("Page Number", min_value=1, step=1, value=1)
    
    sample_articles = [
        {"title": "New Irrigation Policy Announced", "summary": "The government has unveiled a new irrigation policy...", "source": "AgriNews", "url": "https://example.com/news1"},
        {"title": "Crop Prices on the Rise", "summary": "Farmers are witnessing a steady rise in crop prices...", "source": "FarmToday", "url": "https://example.com/news2"},
        {"title": "Organic Farming Trends", "summary": "Organic farming is gaining momentum...", "source": "EcoAgri", "url": "https://example.com/news3"}
    ]
    
    for article in sample_articles:
        st.markdown(f"### {article['title']}")
        st.write(article["summary"])
        st.write(f"*Source: {article['source']}*")
        st.markdown(f"[Read more]({article['url']})")
        st.markdown("---")

# Display footer at the end of the app
footer()
