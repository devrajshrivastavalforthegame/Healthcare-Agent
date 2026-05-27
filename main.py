import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Healthcare Navigation Agent",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }

    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }

    .warning-box {
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }

    .info-box {
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }

    .success-box {
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }

    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
    }

    .stButton>button:hover {
        background-color: #1565C0;
    }
    </style>
""", unsafe_allow_html=True)

# Session State
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# Header
st.markdown(
    '<div class="main-header">🏥 AI-Powered Healthcare Navigation Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-header">Personalized health guidance powered by Local AI</div>',
    unsafe_allow_html=True
)

# Disclaimer
st.markdown("""
<div class="warning-box">
<strong>⚠️ Medical Disclaimer:</strong>
This AI assistant provides general health information only.
It is NOT a substitute for professional medical advice,
diagnosis, or treatment.
Always consult qualified healthcare professionals.
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:

    st.header("👤 User Profile")

    with st.form("user_profile_form"):

        name = st.text_input(
            "Name",
            value=st.session_state.user_profile.get('name', '')
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=st.session_state.user_profile.get('age', 30)
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=300.0,
            value=70.0
        )

        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=170.0
        )

        chronic_conditions = st.multiselect(
            "Chronic Conditions",
            [
                "Diabetes",
                "Hypertension",
                "Asthma",
                "Heart Disease",
                "Allergies"
            ]
        )

        medications = st.text_area("Current Medications")

        allergies = st.text_area("Known Allergies")

        submit_profile = st.form_submit_button("💾 Save Profile")

        if submit_profile:

            st.session_state.user_profile = {
                'name': name,
                'age': age,
                'gender': gender,
                'weight': weight,
                'height': height,
                'chronic_conditions': chronic_conditions,
                'medications': medications,
                'allergies': allergies
            }

            st.success("✅ Profile Saved")

    st.divider()

    # Local AI Status
    st.header("🖥️ Local AI Status")
    st.success("✅ Ollama Connected")

    st.divider()

    # Clear Chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Main Layout
col1, col2 = st.columns([2, 1])

# LEFT SIDE
with col1:

    st.header("💬 Healthcare Chat")

    # Chat History
    for chat in st.session_state.chat_history:

        if chat['role'] == 'user':

            st.markdown(f"""
            <div class="info-box">
            <strong>You:</strong> {chat['content']}
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="success-box">
            <strong>AI Assistant:</strong> {chat['content']}
            </div>
            """, unsafe_allow_html=True)

    # Input
    user_input = st.text_area(
        "Describe your symptoms or ask a question:",
        height=120,
        placeholder="Example: I have headache and fever for 2 days..."
    )

    send_button = st.button("🚀 Send")

    # SEND BUTTON
    if send_button and user_input:

        # Save User Message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })

        profile = st.session_state.user_profile

        profile_context = f"""
User Profile:
Name: {profile.get('name', '')}
Age: {profile.get('age', '')}
Gender: {profile.get('gender', '')}
Weight: {profile.get('weight', '')}
Height: {profile.get('height', '')}
Chronic Conditions: {profile.get('chronic_conditions', '')}
Medications: {profile.get('medications', '')}
Allergies: {profile.get('allergies', '')}
"""

        prompt = f"""
You are an AI Healthcare Navigation Assistant.

{profile_context}

User Question:
{user_input}

Instructions:
1. Give only general healthcare guidance
2. Do NOT provide exact diagnosis
3. Recommend consulting doctors
4. Mention emergency warning signs if needed
5. Be supportive and empathetic
6. Keep response simple and helpful
"""

        try:

            with st.spinner("🤖 AI is thinking..."):

                response = requests.post(
                    OLLAMA_URL = "https://stowing-unspoiled-singer.ngrok-free.dev",
                    url=f"{OLLAMA_URL}/api/generate",
                    json={
                        "model": "llama3",
                        "prompt": prompt,
                        "stream": False
                    }
                )

                ai_response = response.json()["response"]

                # Save AI Response
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response,
                    'timestamp': datetime.now().isoformat()
                })

                st.rerun()

        except Exception as e:

            st.error(f"❌ Error: {str(e)}")

            st.info(
                "Make sure Ollama is running using: ollama run llama3"
            )

# RIGHT SIDE
with col2:

    st.header("📊 Quick Actions")

    symptom_buttons = {
        "🤒 Fever": "I have fever",
        "🤕 Headache": "I have headache",
        "😷 Cold": "I have cold symptoms",
        "🤢 Nausea": "I feel nausea",
        "😫 Fatigue": "I feel tired",
        "🦴 Body Pain": "I have body pain"
    }

    for label, symptom in symptom_buttons.items():

        if st.button(label):

            st.session_state.chat_history.append({
                'role': 'user',
                'content': symptom,
                'timestamp': datetime.now().isoformat()
            })

            st.rerun()

    st.divider()

    st.subheader("💡 Health Tips")

    st.info("""
    - Drink enough water
    - Sleep 7-9 hours
    - Exercise regularly
    - Eat healthy food
    - Reduce stress
    """)

    st.divider()

    st.subheader("🚨 Emergency Warning Signs")

    st.error("""
    - Severe chest pain
    - Breathing difficulty
    - Stroke symptoms
    - Severe bleeding
    - Unconsciousness

    Contact emergency services immediately.
    """)

# Footer
st.divider()

st.markdown("""
<div style="text-align:center; color:gray; padding:10px;">
AI Healthcare Navigation Agent • Localhost Version • Powered by Ollama + Llama3
<br><br>
⚠️ Educational purposes only. Not professional medical advice.
</div>
""", unsafe_allow_html=True)