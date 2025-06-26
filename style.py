import streamlit as st


def load_style():
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
        </style>
    """, unsafe_allow_html=True)

# # Footer function to display at the bottom of the app
# def footer():
#     st.markdown('<div class="footer">Developed by Your Company Name © 2025</div>', unsafe_allow_html=True)

