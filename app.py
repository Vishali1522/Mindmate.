import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

# ==========================================================
# MINDMATE
# Student Pressure & Study Support Web App
# Class XI Artificial Intelligence Project
# ==========================================================

st.set_page_config(
    page_title="MindMate",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------- STYLE --------------------------

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #F8FBFF 0%, #EEF5FF 50%, #F9F7FF 100%);
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: #263B70;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    font-size: 19px;
    color: #667085;
    margin-top: 5px;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    margin: 15px 0;
    box-shadow: 0 4px 18px rgba(50,70,100,0.08);
}
</style>
""", unsafe_allow_html=True)

# ------------------------- HEADER -------------------------

st.markdown('<div class="main-title">🧠 MindMate</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Understand your pressure • Organise your day • Take one step at a time</div>',
    unsafe_allow_html=True,
)

st.info(
    "MindMate is an educational student-support project. "
    "It does not diagnose medical or mental-health conditions."
)

# ------------------- STUDENT INFORMATION -----------------

st.header("👤 About You")
c1, c2 = st.columns(2)

with c1:
    name = st.text_input("Your Name", placeholder="Enter your name")

with c2:
    age = st.number_input("Age", min_value=10, max_value=25, value=16, step=1)

# ---------------------- PRESSURE INPUT -------------------

st.header("📊 Your Pressure Levels")
st.write("Rate each area from 1 to 6. Half-point values such as 2.5 or 4.5 are allowed.")

c1, c2 = st.columns(2)

with c1:
    peer_pressure = st.number_input("👥 Peer Pressure", 1.0, 6.0, 1.0, 0.5)
    family_pressure = st.number_input("👨‍👩‍👧 Family Pressure", 1.0, 6.0, 1.0, 0.5)
    academic_pressure = st.number_input("🏫 Academic / School Pressure", 1.0, 6.0, 1.0, 0.5)

with c2:
    study_pressure = st.number_input("📚 Study Pressure", 1.0, 6.0, 1.0, 0.5)
    social_pressure = st.number_input("🌐 Social Pressure", 1.0, 6.0, 1.0, 0.5)
    workload = st.number_input("📝 Workload", 1.0, 6.0, 1.0, 0.5)

# ---------------------- DAILY ROUTINE --------------------

st.header("⏰ Your Daily Routine")
c1, c2, c3 = st.columns(3)

with c1:
    sleep_hours = st.number_input("😴 Sleep Hours", 0.0, 15.0, 7.0, 0.5)
with c2:
    study_hours = st.number_input("📖 Study Hours", 0.0, 15.0, 4.0, 0.5)
with c3:
    free_hours = st.number_input("🌿 Free Time", 0.0, 15.0, 2.0, 0.5)

# ------------------------- SUBJECTS -----------------------

st.header("📚 Your Subjects")
subjects = st.text_input(
    "Enter subjects separated by commas",
    placeholder="Accountancy, Economics, Business Studies, Maths",
)
subject_list = [x.strip() for x in subjects.split(",") if x.strip()]

# -------------------------- NLP ---------------------------

st.header("💬 Tell MindMate What You're Going Through")
st.write(
    "Write freely in English, Hindi, Hinglish, Punjabi, Tamil, Telugu, "
    "Kannada or another language."
)

situation = st.text_area(
    "Your Situation",
    placeholder="Example: I am worried about marks and I don't get enough time to study and rest...",
    height=180,
)

def analyse_text(text):
    """Lightweight multilingual keyword/theme detection.

    This is intentionally conservative: if no known theme is detected,
    MindMate does not pretend to understand the message.
    """
    text = text.lower().strip()
    keyword_groups = {
        "📚 Academic / Study Concern": [
            "study", "studies", "exam", "exams", "marks", "grade", "grades",
            "school", "homework", "पढ़ाई", "परीक्षा", "एग्जाम", "मार्क्स",
            "படிப்பு", "தேர்வு", "చదువు", "పరీక్ష",
        ],
        "👨‍👩‍👧 Family Concern": [
            "family", "parent", "parents", "mother", "father",
            "माता", "पिता", "परिवार", "मम्मी", "पापा",
            "அம்மா", "அப்பா", "குடும்பம்",
        ],
        "👥 Peer / Comparison Concern": [
            "friend", "friends", "peer", "compare", "comparison",
            "दोस्त", "तुलना", "நண்பர்கள்",
        ],
        "⏰ Time / Workload Concern": [
            "time", "busy", "workload", "schedule",
            "समय", "काम", "टाइम", "நேரம்",
        ],
        "😟 Worry / Stress Language": [
            "stress", "stressed", "worried", "worry", "tension",
            "pressure", "overthink", "चिंता", "तनाव", "टेंशन", "दबाव",
            "கவலை", "மன அழுத்தம்",
        ],
    }

    themes = []
    for theme, keywords in keyword_groups.items():
        if any(word in text for word in keywords):
            themes.append(theme)
    return themes

# ---------------------- ANALYSIS ENGINE ------------------

def calculate_score(peer, family, academic, study, social, workload, sleep, free_time):
    pressure_values = np.array([peer, family, academic, study, social], dtype=float)
    average_pressure = np.mean(pressure_values)

    # Transparent, deterministic score:
    # 60% average pressure + 20% workload + up to 12 sleep + up to 8 free-time.
    score = (average_pressure / 6) * 60 + (workload / 6) * 20

    if sleep < 6:
        score += 12
    elif sleep < 7:
        score += 6

    if free_time < 1:
        score += 8
    elif free_time < 2:
        score += 4

    return round(float(np.clip(score, 0, 100)), 1)

def get_category(score):
    if score < 35:
        return "Low"
    if score < 60:
        return "Moderate"
    if score < 80:
        return "High"
    return "Very High"

def generate_advice():
    advice = []

    if academic_pressure >= 4.5:
        advice.append("🏫 Academic pressure is relatively high. Break study goals into smaller daily targets.")
    if family_pressure >= 4.5:
        advice.append("👨‍👩‍👧 If expectations feel difficult to manage, consider discussing your workload with a trusted adult.")
    if peer_pressure >= 4.5:
        advice.append("👥 Focus on your own progress rather than comparing yourself with classmates.")
    if study_pressure >= 4.5:
        advice.append("📚 Use focused study sessions and divide large chapters into smaller sections.")
    if workload >= 4.5:
        advice.append("📝 Your workload rating is high. Prioritise urgent and important tasks first.")
    if sleep_hours < 7:
        advice.append("😴 Your reported sleep is below 7 hours. Try to protect adequate sleep and keep a consistent routine.")
    if free_hours < 1:
        advice.append("🌿 Your free time is very limited. Add short breaks and a relaxing activity to your routine.")

    if not advice:
        advice.append("💡 Your current inputs do not show a major pressure area. Continue maintaining a balanced routine.")
    return advice

def generate_todo():
    todo = ["📝 Write your top 3 priorities for today."]

    if subject_list:
        for subject in subject_list[:3]:
            todo.append(f"📚 Complete one focused session of {subject}.")
    else:
        todo.append("📚 Choose one important subject for your first study session.")

    if workload >= 4:
        todo.append("✂️ Divide large assignments into smaller tasks.")

    todo.append("☕ Take short breaks between focused sessions.")
    todo.append("🌿 Keep some time for yourself.")

    if sleep_hours < 7:
        todo.append("😴 Make sleep a priority tonight.")

    return todo

def create_timetable():
    s = subject_list[:3]
    while len(s) < 3:
        s.append(["Priority Subject", "Second Subject", "Revision"][len(s)])

    return pd.DataFrame({
        "Time": [
            "5:30 AM", "6:00 AM", "7:00 AM – 2:00 PM", "2:00 PM – 3:00 PM",
            "3:00 PM – 4:00 PM", "4:00 PM – 5:30 PM", "6:00 PM – 7:00 PM",
            "7:15 PM – 8:15 PM", "8:15 PM – 9:00 PM", "9:00 PM – 10:00 PM",
            "10:00 PM – 10:30 PM",
        ],
        "Activity": [
            "🌅 Wake up & get ready", "🥣 Breakfast / preparation", "🏫 School",
            "🍱 Lunch + Rest", "📝 Homework / light work", "📖 Tuition / learning",
            f"📚 {s[0]}", f"📘 {s[1]}", "🍽️ Dinner + Relaxation",
            f"📝 {s[2]}", "🌙 Prepare for tomorrow",
        ],
    })

# -------------------------- RUN ---------------------------

st.divider()

if st.button("🧠 Analyse My Situation", use_container_width=True):
    if not name.strip():
        st.warning("Please enter your name.")
    elif not situation.strip():
        st.warning("Please tell MindMate about your situation first.")
    else:
        detected_themes = analyse_text(situation)

        stress_score = calculate_score(
            peer_pressure, family_pressure, academic_pressure,
            study_pressure, social_pressure, workload,
            sleep_hours, free_hours,
        )
        category = get_category(stress_score)

        st.success(f"Welcome, {name}! 🧠 MindMate has analysed the information you provided.")

        st.header("🧠 MindMate Analysis")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Stress Indicator", f"{stress_score}/100")
        with c2:
            st.metric("Pressure Level", category)
        with c3:
            st.metric("Detected Themes", len(detected_themes))

        st.subheader("🔍 Why did MindMate give this result?")
        st.write(
            "The indicator is calculated from the five pressure ratings, workload, "
            "reported sleep and free time. The calculation is deterministic and "
            "does not use random values."
        )
        st.caption(
            "The free-text NLP layer is conservative: it detects predefined themes "
            "only and does not make a medical diagnosis."
        )

        st.subheader("💬 Themes Found in Your Message")
        if detected_themes:
            for theme in detected_themes:
                st.write(f"• {theme}")
        else:
            st.write(
                "No predefined concern keywords were confidently detected. "
                "MindMate will not guess a concern from unknown text."
            )

        pressure_df = pd.DataFrame({
            "Area": ["👥 Peer", "👨‍👩‍👧 Family", "🏫 Academic", "📚 Study", "🌐 Social"],
            "Level": [peer_pressure, family_pressure, academic_pressure, study_pressure, social_pressure],
        })

        st.subheader("📊 Your Pressure Breakdown")
        st.dataframe(pressure_df, use_container_width=True, hide_index=True)

        st.subheader("📈 Pressure Graph")
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.bar(pressure_df["Area"], pressure_df["Level"])
        ax.set_ylim(0, 6)
        ax.set_ylabel("Level (1–6)")
        ax.set_title("MindMate Pressure Analysis")
        ax.grid(axis="y", alpha=0.25)
        st.pyplot(fig)

        st.subheader("🎯 Main Pressure Contributors")
        top_two = pressure_df.sort_values("Level", ascending=False).head(2)
        for _, row in top_two.iterrows():
            st.write(f"**{row['Area']} — {row['Level']}/6**")

        st.subheader("💡 Personalised Suggestions")
        for item in generate_advice():
            st.write(item)

        st.subheader("📝 Your Personalised To-Do List")
        for task in generate_todo():
            st.checkbox(task)

        st.subheader("🗓️ Suggested Daily Timetable")
        st.dataframe(create_timetable(), use_container_width=True, hide_index=True)

        st.subheader("🌟 A Message for You")
        if stress_score >= 80:
            st.warning(
                "Your answers indicate a high level of pressure. You do not have to "
                "manage everything alone. Consider speaking with a trusted adult, "
                "teacher, school counsellor or qualified professional."
            )
        elif stress_score >= 60:
            st.info(
                "Your answers show several pressure factors. Focus on one manageable "
                "task at a time and give yourself reasonable breaks."
            )
        else:
            st.success(
                "🌟 Keep going! Small, consistent steps and a balanced routine "
                "can make studying more manageable."
            )

        st.divider()
        st.caption(
            "⚠️ MindMate is an educational AI project, not a medical diagnosis system. "
            "If you are experiencing serious distress or feel unable to cope, please "
            "reach out to a trusted adult or qualified professional."
        )

st.divider()
st.caption("🧠 MindMate • Class XI AI Project • Python • NumPy • Pandas • Matplotlib • Streamlit")
