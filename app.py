import streamlit as st
import json
import plotly.graph_objects as go

from calculations.cgpa import (
    calculate_cgpa,
    required_future_sgpa,
    maximum_possible_cgpa
)
from calculations.attendance import (
    calculate_attendance,
    classes_needed_for_target,
    projected_attendance
)

from calculations.achievements import (
    get_achievements,
    ALL_ACHIEVEMENTS
)

from database import (
    initialize_database,
    save_student,
    get_all_students
    
)

st.markdown(
    """
    <style>

    /* ═════════════════════════════════════════════
       GRADETRACK — GLOBAL VISUAL POLISH
       ═════════════════════════════════════════════ */

    /* ─────────────────────────────────────────────
       GLOBAL APP SPACING
       ───────────────────────────────────────────── */

    div[data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Slightly cleaner vertical rhythm */

    div[data-testid="stVerticalBlock"] {
        gap: 0.75rem;
    }


    /* ─────────────────────────────────────────────
       SIDEBAR
       ───────────────────────────────────────────── */

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.15);
    }

    section[data-testid="stSidebar"] .stButton > button {

        width: 100%;
        text-align: left;

        border: 1px solid transparent;
        background: transparent;

        padding: 0.65rem 0.85rem;
        margin-bottom: 0.2rem;

        border-radius: 10px;

        font-weight: 550;

        transition:
            background-color 0.18s ease,
            border-color 0.18s ease,
            transform 0.18s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {

        background-color: rgba(99, 102, 241, 0.10);

        border-color: rgba(99, 102, 241, 0.18);

        transform: translateX(2px);
    }


    /* ─────────────────────────────────────────────
       MAIN BUTTONS
       ───────────────────────────────────────────── */

    div[data-testid="stMainBlockContainer"] .stButton > button {

        border-radius: 12px;

        padding: 0.7rem 1rem;

        font-weight: 650;

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease,
            border-color 0.18s ease;
    }

    div[data-testid="stMainBlockContainer"] .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 7px 18px rgba(0, 0, 0, 0.18);
    }


    /* ─────────────────────────────────────────────
       INPUT FIELDS
       ───────────────────────────────────────────── */

    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {

        border-radius: 10px !important;

        transition:
            border-color 0.18s ease,
            box-shadow 0.18s ease;
    }

    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stTextInput"] input:focus {

        box-shadow:
            0 0 0 2px rgba(99, 102, 241, 0.18) !important;
    }


    /* ─────────────────────────────────────────────
       DASHBOARD SNAPSHOT CARDS
       ───────────────────────────────────────────── */

    .snapshot-title {

        font-size: 1.35rem;
        font-weight: 700;

        margin-bottom: 1rem;
    }

    .metric-card {

        padding: 1.2rem;

        border-radius: 14px;

        border:
            1px solid rgba(128, 128, 128, 0.20);

        background:
            rgba(128, 128, 128, 0.06);

        min-height: 125px;

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .metric-card:hover {

        transform: translateY(-3px);

        border-color:
            rgba(99, 102, 241, 0.45);

        box-shadow:
            0 8px 24px rgba(0, 0, 0, 0.12);
    }

    .metric-label {

        font-size: 0.9rem;
        font-weight: 600;

        opacity: 0.75;

        margin-bottom: 0.45rem;
    }

    .metric-value {

        font-size: 2rem;
        font-weight: 750;

        line-height: 1.1;

        margin-bottom: 0.4rem;
    }

    .metric-subtitle {

        font-size: 0.78rem;

        opacity: 0.6;
    }


    /* ─────────────────────────────────────────────
       TOP-RIGHT STUDENT PROFILE
       ───────────────────────────────────────────── */

    .top-profile {

        display: flex;

        align-items: center;
        justify-content: flex-end;

        gap: 0.55rem;

        padding: 0.45rem 0.7rem;

        border:
            1px solid rgba(128, 128, 128, 0.2);

        border-radius: 12px;

        background:
            rgba(128, 128, 128, 0.06);

        margin-bottom: 0.8rem;
    }

    .top-profile-icon {

        font-size: 1.35rem;
    }

    .top-profile-name {

        font-weight: 650;

        font-size: 0.9rem;

        white-space: nowrap;
    }

    .top-profile-subtitle {

        font-size: 0.7rem;

        opacity: 0.55;
    }


    /* ─────────────────────────────────────────────
       ACHIEVEMENT CARDS
       ───────────────────────────────────────────── */

    .achievement-card {

        padding: 1.2rem;

        border-radius: 14px;

        border:
            1px solid rgba(128, 128, 128, 0.20);

        background:
            linear-gradient(
                135deg,
                rgba(99, 102, 241, 0.10),
                rgba(168, 85, 247, 0.06)
            );

        min-height: 145px;

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .achievement-card:hover {

        transform: translateY(-4px);

        border-color:
            rgba(99, 102, 241, 0.45);

        box-shadow:
            0 8px 22px rgba(0, 0, 0, 0.12);
    }

    .achievement-progress-card {

        padding: 22px 24px;

        margin: 10px 0 28px 0;

        border-radius: 18px;

        background:
            linear-gradient(
                135deg,
                rgba(99, 102, 241, 0.16),
                rgba(168, 85, 247, 0.10)
            );

        border:
            1px solid rgba(129, 140, 248, 0.25);

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.08);
    }

    .achievement-progress-header {

        display: flex;

        justify-content: space-between;
        align-items: center;

        gap: 20px;
    }

    .achievement-progress-title {

        font-size: 1.25rem;

        font-weight: 700;
    }

    .achievement-progress-subtitle {

        margin-top: 4px;

        font-size: 0.88rem;

        opacity: 0.65;
    }

    .achievement-progress-count {

        font-size: 1.35rem;

        font-weight: 800;

        text-align: right;
    }

    .achievement-progress-count span {

        display: block;

        font-size: 0.72rem;

        font-weight: 500;

        opacity: 0.6;

        margin-top: 2px;
    }

    .achievement-progress-bar {

        width: 100%;

        height: 10px;

        margin-top: 20px;

        border-radius: 999px;

        background:
            rgba(128, 128, 128, 0.18);

        overflow: hidden;
    }

    .achievement-progress-fill {

        height: 100%;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                #6366f1,
                #a855f7
            );

        transition:
            width 0.6s ease;
    }

    .achievement-progress-footer {

        display: flex;

        justify-content: space-between;

        margin-top: 9px;

        font-size: 0.75rem;

        opacity: 0.65;
    }


    /* ─────────────────────────────────────────────
       LOCKED ACHIEVEMENTS
       ───────────────────────────────────────────── */

    .achievement-locked {

        opacity: 0.68;

        position: relative;
    }

    .achievement-locked:hover {

        opacity: 0.85;
    }

    .locked-icon-wrapper {

        position: relative;

        width: fit-content;

        margin-bottom: 0.5rem;
    }

    .locked-badge-icon {

        opacity: 0.45;

        filter: saturate(0.65);
    }

    .locked-overlay {

        position: absolute;

        right: -10px;
        bottom: -5px;

        font-size: 1rem;

        padding: 0.15rem 0.3rem;

        border-radius: 999px;

        background:
            rgba(40, 40, 50, 0.85);

        border:
            1px solid rgba(255, 255, 255, 0.18);

        box-shadow:
            0 3px 10px rgba(0, 0, 0, 0.2);
    }

    .achievement-icon {

        font-size: 2rem;

        margin-bottom: 0.5rem;
    }

    .achievement-title {

        font-size: 1.05rem;

        font-weight: 700;

        margin-bottom: 0.35rem;
    }

    .achievement-description {

        font-size: 0.8rem;

        opacity: 0.65;

        line-height: 1.4;
    }


    /* ─────────────────────────────────────────────
       ACHIEVEMENT RARITY
       ───────────────────────────────────────────── */

    .achievement-rarity {

        display: inline-block;

        margin-top: 0.8rem;

        padding: 0.25rem 0.6rem;

        border-radius: 999px;

        font-size: 0.62rem;

        font-weight: 750;

        letter-spacing: 0.08em;
    }

    .rarity-common {

        background:
            rgba(128, 128, 128, 0.12);

        border:
            1px solid rgba(128, 128, 128, 0.25);
    }

    .rarity-rare {

        background:
            rgba(59, 130, 246, 0.12);

        border:
            1px solid rgba(59, 130, 246, 0.30);
    }

    .rarity-epic {

        background:
            rgba(168, 85, 247, 0.13);

        border:
            1px solid rgba(168, 85, 247, 0.32);
    }

    .rarity-legendary {

        background:
            rgba(245, 158, 11, 0.14);

        border:
            1px solid rgba(245, 158, 11, 0.35);
    }

    .achievement-empty {

        text-align: center;

        padding: 1.5rem;

        border-radius: 14px;

        border:
            1px dashed rgba(128, 128, 128, 0.30);

        background:
            rgba(128, 128, 128, 0.04);
    }

    .achievement-empty-icon {

        font-size: 2rem;

        margin-bottom: 0.5rem;
    }

    .achievement-empty-title {

        font-weight: 700;

        margin-bottom: 0.3rem;
    }

    .achievement-empty-text {

        font-size: 0.8rem;

        opacity: 0.6;
    }


    /* ─────────────────────────────────────────────
       BADGE COLLECTION
       ───────────────────────────────────────────── */

    .badge-tile {

        border-radius: 16px;

        padding: 14px 8px 10px 8px;

        text-align: center;

        min-height: 115px;

        display: flex;

        flex-direction: column;

        justify-content: center;

        align-items: center;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .badge-tile.owned {

        background:
            linear-gradient(
                145deg,
                rgba(120, 80, 255, 0.22),
                rgba(0, 200, 255, 0.12)
            );

        border:
            1px solid rgba(150, 120, 255, 0.55);

        box-shadow:
            0 0 18px rgba(120, 80, 255, 0.16),
            inset 0 0 18px rgba(255, 255, 255, 0.03);
    }

    .badge-tile.owned:hover {

        transform: translateY(-4px);

        box-shadow:
            0 8px 24px rgba(120, 80, 255, 0.25),
            inset 0 0 18px rgba(255, 255, 255, 0.05);
    }

    .badge-tile.locked {

        background:
            rgba(120, 120, 120, 0.06);

        border:
            1px solid rgba(150, 150, 150, 0.18);

        filter: grayscale(0.8);

        opacity: 0.48;
    }

    .badge-icon {

        font-size: 38px;

        line-height: 1;

        margin-bottom: 8px;
    }

    .badge-lock {

        position: absolute;

        top: 7px;
        left: 9px;

        font-size: 13px;
    }

    .badge-name {

        font-size: 12px;

        font-weight: 700;

        line-height: 1.15;
    }

    .badge-rarity {

        font-size: 10px;

        opacity: 0.65;

        margin-top: 4px;
    }

    .badge-requirement {

        font-size: 9px;

        opacity: 0.7;

        margin-top: 6px;

        line-height: 1.2;

        max-width: 95px;
    }

    /* ─────────────────────────────────────────────
    DASHBOARD SECTION RHYTHM
    ───────────────────────────────────────────── */

    div[data-testid="stMainBlockContainer"] h2,
    div[data-testid="stMainBlockContainer"] h3 {
        margin-top: 1.15rem;
        margin-bottom: 0.45rem;
    }

    div[data-testid="stMainBlockContainer"] hr {
        margin-top: 1.1rem;
        margin-bottom: 1.1rem;
    }

    div[data-testid="stMainBlockContainer"] .stCaption {
        line-height: 1.45;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="GradeTrack",
    page_icon="🎓",
    layout="wide"
)

initialize_database()

if "cgpa" not in st.session_state:
    st.session_state["cgpa"] = None

if "attendance" not in st.session_state:
    st.session_state["attendance"] = None

if "target_cgpa" not in st.session_state:
    st.session_state["target_cgpa"] = None

if "target_attendance" not in st.session_state:
    st.session_state["target_attendance"] = None

if "completed_credits" not in st.session_state:
    st.session_state["completed_credits"] = None

if "remaining_credits" not in st.session_state:
    st.session_state["remaining_credits"] = None

if "semesters" not in st.session_state:
    st.session_state["semesters"] = None

if "course" not in st.session_state:
    st.session_state["course"] = None

if "current_semester" not in st.session_state:
    st.session_state["current_semester"] = None

if "student_name" not in st.session_state:
    st.session_state["student_name"] = None

if "roll_number" not in st.session_state:
    st.session_state["roll_number"] = None

if "batch" not in st.session_state:
    st.session_state["batch"] = None

if "department" not in st.session_state:
    st.session_state["department"] = None

if "college" not in st.session_state:
    st.session_state["college"] = None

if "email" not in st.session_state:
    st.session_state["email"] = None

if "students" not in st.session_state:
    st.session_state["students"] = {}

if "current_student_id" not in st.session_state:
    st.session_state["current_student_id"] = None

if "creating_new_student" not in st.session_state:
    st.session_state["creating_new_student"] = False

if st.session_state["current_student_id"]:

    if (
        st.session_state.get("current_student_id")
        not in st.session_state["students"]
    ):
        st.session_state["current_student_id"] = next(
            iter(st.session_state["students"])
        )

    current_student = st.session_state["students"][
        st.session_state["current_student_id"]
    ]

    if "academic" not in current_student:
        current_student["academic"] = {
            "cgpa": None,
            "attendance": None,
            "target_cgpa": None,
            "target_attendance": None,
            "completed_credits": None,
            "remaining_credits": None,
            "semesters": None
        }

# ─────────────────────────────────────────────
# BADGE DEFINITIONS
# ─────────────────────────────────────────────

BADGES = [
    {
        "id": "getting_started",
        "icon": "🥉",
        "name": "Getting Started",
        "rarity": "Common",
        "description": "You've started tracking your academic journey!",
        "requirement": "Enter your CGPA"
    },
    {
        "id": "rising_star",
        "icon": "📈",
        "name": "Rising Star",
        "rarity": "Rare",
        "description": "Your SGPA is improving!",
        "requirement": "Improve your SGPA between semesters"
    },
    {
        "id": "attendance_warrior",
        "icon": "🔥",
        "name": "Attendance Warrior",
        "rarity": "Rare",
        "description": "Your attendance is above 90%!",
        "requirement": "Reach 90% attendance"
    },
    {
        "id": "perfect_attendance",
        "icon": "💯",
        "name": "Perfect Attendance",
        "rarity": "Legendary",
        "description": "Not a single class missed!",
        "requirement": "Reach 100% attendance"
    },
    {
        "id": "goal_crusher",
        "icon": "🎯",
        "name": "Goal Crusher",
        "rarity": "Epic",
        "description": "You've reached your CGPA goal!",
        "requirement": "Reach your CGPA target"
    },
    {
        "id": "elite_performer",
        "icon": "🏆",
        "name": "Elite Performer",
        "rarity": "Epic",
        "description": "You've entered elite academic territory!",
        "requirement": "Reach a CGPA of 9.0"
    },
    {
        "id": "attendance_target",
        "icon": "🎯",
        "name": "Attendance Target",
        "rarity": "Rare",
        "description": "You've reached your attendance goal!",
        "requirement": "Reach your attendance target"
    },
    {
        "id": "consistency_king",
        "icon": "🚀",
        "name": "Consistency King",
        "rarity": "Epic",
        "description": "You've maintained strong performance every semester!",
        "requirement": "Maintain 8.0+ SGPA in every semester"
    },
    {
        "id": "academic_comeback",
        "icon": "⭐",
        "name": "Academic Comeback",
        "rarity": "Legendary",
        "description": "You've made a major academic comeback!",
        "requirement": "Improve SGPA by 1.0+ points"
    }
]

def get_earned_badges():

    earned = []

    cgpa = st.session_state.get("cgpa")
    attendance = st.session_state.get("attendance")
    target_cgpa = st.session_state.get("target_cgpa")
    target_attendance = st.session_state.get("target_attendance")
    semesters = st.session_state.get("semesters")

    if cgpa is not None:
        earned.append("getting_started")

    if attendance is not None and attendance >= 90:
        earned.append("attendance_warrior")

    if attendance is not None and attendance >= 100:
        earned.append("perfect_attendance")

    if (
        cgpa is not None
        and target_cgpa is not None
        and cgpa >= target_cgpa
    ):
        earned.append("goal_crusher")

    if cgpa is not None and cgpa >= 9.0:
        earned.append("elite_performer")

    if (
        attendance is not None
        and target_attendance is not None
        and attendance >= target_attendance
    ):
        earned.append("attendance_target")

    if semesters:

        valid_sgpas = [
            semester.get("sgpa")
            for semester in semesters
            if semester.get("sgpa") is not None
        ]

        if len(valid_sgpas) >= 2:

            if valid_sgpas[-1] > valid_sgpas[0]:
                earned.append("rising_star")

            if all(sgpa >= 8.0 for sgpa in valid_sgpas):
                earned.append("consistency_king")

            if max(valid_sgpas) - min(valid_sgpas) >= 1.0:
                earned.append("academic_comeback")

    return earned

def save_academic_data():
    student_id = st.session_state.get("current_student_id")

    if not student_id:
        return

    if student_id not in st.session_state["students"]:
        return

    st.session_state["students"][student_id]["academic"] = {
        "cgpa": st.session_state.get("cgpa"),
        "attendance": st.session_state.get("attendance"),
        "target_cgpa": st.session_state.get("target_cgpa"),
        "target_attendance": st.session_state.get("target_attendance"),
        "completed_credits": st.session_state.get("completed_credits"),
        "remaining_credits": st.session_state.get("remaining_credits"),
        "semesters": st.session_state.get("semesters")
    }

    current_student = st.session_state["students"][student_id]

    save_student(current_student)

# Load saved students from SQLite
if not st.session_state["students"]:

    saved_students = get_all_students()

    for student in saved_students:

        student_id = str(student[2])

        semesters_data = None

        if student[15]:
            try:
                semesters_data = json.loads(student[15])
            except json.JSONDecodeError:
                semesters_data = None

        st.session_state["students"][student_id] = {
            "name": student[1],
            "roll_number": student[2],
            "batch": student[3],
            "department": student[4],
            "course": student[5],
            "college": student[6],
            "semester": student[7],
            "email": student[8],

            "academic": {
                "cgpa": student[9],
                "attendance": student[10],
                "target_cgpa": student[11],
                "target_attendance": student[12],
                "completed_credits": student[13],
                "remaining_credits": student[14],
                "semesters": semesters_data
            }
        }


# Set the first saved student as the active student
if (
    st.session_state["students"]
    and st.session_state["current_student_id"] is None
    and not st.session_state.get("creating_new_student", False)
):

    student_id = next(iter(st.session_state["students"]))

    selected_data = st.session_state["students"][student_id]

    st.session_state["current_student_id"] = student_id

    st.session_state["student_name"] = selected_data["name"]
    st.session_state["roll_number"] = selected_data["roll_number"]
    st.session_state["batch"] = selected_data["batch"]
    st.session_state["department"] = selected_data["department"]
    st.session_state["course"] = selected_data["course"]
    st.session_state["college"] = selected_data["college"]
    st.session_state["current_semester"] = selected_data["semester"]
    st.session_state["email"] = selected_data["email"]

    academic_data = selected_data["academic"]

    st.session_state["cgpa"] = academic_data["cgpa"]
    st.session_state["attendance"] = academic_data["attendance"]
    st.session_state["target_cgpa"] = academic_data["target_cgpa"]
    st.session_state["target_attendance"] = academic_data["target_attendance"]
    st.session_state["completed_credits"] = academic_data["completed_credits"]
    st.session_state["remaining_credits"] = academic_data["remaining_credits"]
    st.session_state["semesters"] = academic_data["semesters"]


# -----------------------------
# Main Header
# -----------------------------




# -----------------------------
# Navigation
# -----------------------------

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────

st.sidebar.title("🎓 GradeTrack")

st.sidebar.caption(
    "Your College Performance Companion"
)

st.sidebar.divider()

st.sidebar.markdown(
    "### 🧭 Your Space"
)

pages = [

    ("🏠", "Dashboard"),

    ("🧮", "CGPA Calculator"),

    ("🎯", "CGPA Goal Planner"),

    ("📅", "Attendance Calculator"),

    ("🎯", "Attendance Goal Planner"),

    ("📈", "Future Attendance Projection")

]

if "page" not in st.session_state:

    st.session_state["page"] = "Dashboard"

for icon, page_name in pages:

    active = page_name == st.session_state["page"]

    if active:

        st.sidebar.markdown(
            f"""
            <div class="active-nav">
                {icon}&nbsp;&nbsp;{page_name}
            </div>
            """,
            unsafe_allow_html=True
    )

    else:

        if st.sidebar.button(
            f"{icon}  {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True
        ):

            st.session_state["page"] = page_name

            st.rerun()

page = st.session_state["page"]



# Generate achievements for the current student
achievements = get_achievements(
    cgpa=st.session_state.get("cgpa"),
    attendance=st.session_state.get("attendance"),
    target_cgpa=st.session_state.get("target_cgpa"),
    target_attendance=st.session_state.get("target_attendance"),
    semesters=st.session_state.get("semesters")
)

st.markdown(
    """
    <style>

    /* ─────────────────────────────────────────────
   SIDEBAR NAVIGATION
   ───────────────────────────────────────────── */

div[data-testid="stSidebar"] .stButton > button {

    width: 100%;

    justify-content: flex-start !important;

    text-align: left !important;

    padding: 0.68rem 0.85rem !important;

    margin-bottom: 0.28rem !important;

    border: 1px solid transparent !important;

    border-radius: 11px !important;

    background: transparent !important;

    font-weight: 520 !important;

    transition:
        background 0.18s ease,
        border-color 0.18s ease,
        transform 0.18s ease,
        box-shadow 0.18s ease !important;
}


/* Button text alignment */

div[data-testid="stSidebar"] .stButton > button p {

    text-align: left !important;

    width: 100%;
}


/* Hover */

div[data-testid="stSidebar"] .stButton > button:hover {

    background:
        rgba(99, 102, 241, 0.10) !important;

    border-color:
        rgba(99, 102, 241, 0.18) !important;

    transform: translateX(3px);

    box-shadow:
        0 4px 12px rgba(0, 0, 0, 0.08);
}


/* Active navigation item */

.active-nav {

    width: 100%;

    box-sizing: border-box;

    display: flex;

    align-items: center;

    gap: 0.55rem;

    padding: 0.68rem 0.85rem;

    margin-bottom: 0.28rem;

    border-radius: 11px;

    background:
        linear-gradient(
            90deg,
            rgba(99, 102, 241, 0.26),
            rgba(99, 102, 241, 0.08)
        );

    border:
        1px solid rgba(99, 102, 241, 0.34);

    font-weight: 650;

    text-align: left;

    box-shadow:
        0 5px 16px rgba(0, 0, 0, 0.10);

    position: relative;

    overflow: hidden;
}


/* Active indicator */

.active-nav::before {

    content: "";

    position: absolute;

    left: 0;

    top: 18%;

    height: 64%;

    width: 4px;

    border-radius: 0 4px 4px 0;

    background: #6366f1;

    box-shadow:
        0 0 10px rgba(99, 102, 241, 0.65);
}


/* Active icon */



    /* ─────────────────────────────────────────────
    DASHBOARD METRIC COLORS
    ───────────────────────────────────────────── */

    .metric-purple {
        background: rgba(124, 58, 237, 0.12);
        border: 1px solid rgba(124, 58, 237, 0.35);
        border-radius: 16px;
        padding: 14px;
    }

    .metric-blue {
        background: rgba(37, 99, 235, 0.12);
        border: 1px solid rgba(37, 99, 235, 0.35);
        border-radius: 16px;
        padding: 14px;
    }

    .metric-orange {
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.35);
        border-radius: 16px;
        padding: 14px;
    }  

        /* ─────────────────────────────────────────────
       DASHBOARD QUICK ACTIONS
       ───────────────────────────────────────────── */

    div[data-testid="stMainBlockContainer"] .stButton > button {
        border-radius: 14px !important;
        padding: 0.85rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stMainBlockContainer"] .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
    }  

    </style>
    """,
    unsafe_allow_html=True
)


# ============================
# Dashboard
# ============================

if page == "Dashboard":

    # ─────────────────────────────────────────────
    # TOP PROFILE / ACCOUNT
    # ─────────────────────────────────────────────

    profile_top_col1, profile_top_col2 = st.columns([5, 1])

    with profile_top_col2:

        if st.session_state.get("current_student_id"):

            with st.popover(
                f"👤 {st.session_state['student_name']}",
                use_container_width=True
            ):

                # Profile header

                st.markdown(
                    f"### 👤 {st.session_state.get('student_name') or 'Student'}"
                )

                st.caption(
                    st.session_state.get("course") or "Course not set"
                )

                st.divider()


                # Profile information

                st.markdown("### 👤 Student Profile")

                profile_col1, profile_col2 = st.columns(2)

                with profile_col1:

                    st.caption("NAME")
                    st.write(
                        st.session_state.get("student_name")
                        or "Not set"
                    )

                    st.caption("ROLL NUMBER")
                    st.write(
                        st.session_state.get("roll_number")
                        or "Not set"
                    )

                    st.caption("BATCH / DIVISION")
                    st.write(
                        st.session_state.get("batch")
                        or "Not set"
                    )

                    st.caption("DEPARTMENT")
                    st.write(
                        st.session_state.get("department")
                        or "Not set"
                    )

                with profile_col2:

                    st.caption("COURSE")
                    st.write(
                        st.session_state.get("course")
                        or "Not set"
                    )

                    st.caption("SEMESTER")
                    st.write(
                        st.session_state.get("current_semester")
                        or "Not set"
                    )

                    st.caption("EMAIL")
                    st.write(
                        st.session_state.get("email")
                        or "Not set"
                    )

                st.write("")

                if st.button(
                    "✏️  Edit Profile",
                    use_container_width=True
                ):

                    st.session_state["editing_profile"] = True

                    st.rerun()

                if st.button(
                    "➕  Add New Student",
                    use_container_width=True,
                    key="dashboard_add_student"
                ):
                    st.session_state["creating_new_student"] = True
                    st.session_state["current_student_id"] = None

                    st.session_state["student_name"] = ""
                    st.session_state["roll_number"] = ""
                    st.session_state["batch"] = ""
                    st.session_state["department"] = ""
                    st.session_state["course"] = ""
                    st.session_state["college"] = ""
                    st.session_state["current_semester"] = 1
                    st.session_state["email"] = ""

                    st.session_state["cgpa"] = None
                    st.session_state["attendance"] = None
                    st.session_state["target_cgpa"] = None
                    st.session_state["target_attendance"] = None
                    st.session_state["completed_credits"] = 0
                    st.session_state["remaining_credits"] = 0
                    st.session_state["semesters"] = []

                    st.session_state["editing_profile"] = False

                    st.rerun()

                st.divider()

                #---------------
                # Switch student
                #---------------

                st.markdown("### 🔄 Switch Student")

                current_id = st.session_state.get(
                    "current_student_id"
                )

                current_student = (
                    st.session_state["students"].get(current_id)
                    if current_id
                    else None
                )

                if current_student:

                    st.caption(
                        f"Currently active: **{current_student['name']}** "
                        f"({current_student['roll_number']})"
                    )

                student_ids = list(
                    st.session_state["students"].keys()
                )

                if len(student_ids) > 1:

                    selected_student = st.selectbox(
                        "Choose another student",
                        student_ids,
                        index=(
                            student_ids.index(current_id)
                            if current_id in student_ids
                            else 0
                        ),
                        format_func=lambda student_id:
                            f"{st.session_state['students'][student_id]['name']} "
                            f"({student_id})",
                    key="switch_student_select"
                    )

                    if st.button(
                        "🔄 Switch Student",
                        use_container_width=True
                    ):

                        save_academic_data()

                        selected_data = (
                            st.session_state["students"][
                                selected_student
                            ]
                        )

                        st.session_state[
                            "current_student_id"
                        ] = selected_student

                        academic_data = selected_data.get(
                            "academic",
                            {}
                        )

                        st.session_state["cgpa"] = (
                            academic_data.get("cgpa")
                        )

                        st.session_state["attendance"] = (
                            academic_data.get("attendance")
                        )

                        st.session_state["target_cgpa"] = (
                            academic_data.get("target_cgpa")
                        )

                        st.session_state["target_attendance"] = (
                            academic_data.get("target_attendance")
                        )

                        st.session_state["completed_credits"] = (
                            academic_data.get("completed_credits")
                        )

                        st.session_state["remaining_credits"] = (
                            academic_data.get("remaining_credits")
                        )

                        st.session_state["semesters"] = (
                            academic_data.get("semesters")
                        )

                        st.session_state["student_name"] = (
                            selected_data["name"]
                        )

                        st.session_state["roll_number"] = (
                            selected_data["roll_number"]
                        )

                        st.session_state["batch"] = (
                            selected_data["batch"]
                        )

                        st.session_state["department"] = (
                            selected_data["department"]
                        )

                        st.session_state["course"] = (
                            selected_data["course"]
                        )

                        st.session_state["college"] = (
                            selected_data["college"]
                        )

                        st.session_state["current_semester"] = (
                            selected_data["semester"]
                        )

                        st.session_state["email"] = (
                            selected_data["email"]
                        )

                        st.rerun()

                else:

                    st.caption(
                        "Save another student profile to enable switching."
                    )


    # ─────────────────────────────────────────────
    # DASHBOARD HEADER
    # ─────────────────────────────────────────────

    st.title("🎓 GradeTrack")

    st.caption(
    "Your College Performance Companion"
)

    student_name = (
        st.session_state.get("student_name")
        or "Student"
)

    course = (
        st.session_state.get("course")
        or "Course not set"
)

    semester = (
        st.session_state.get("current_semester")
        or "Not set"
)

    cgpa = st.session_state.get("cgpa")
    attendance = st.session_state.get("attendance")


    st.markdown(
    f"### 👋 Welcome back, {student_name}!"
)

    st.caption(
    f"{course} • Semester {semester}"
)


    if cgpa is not None:

        st.write(
        f"📚 You're currently at **{cgpa:.2f} CGPA**. "
        "Keep pushing your academic performance!"
    )

    elif attendance is not None:

        st.write(
        f"📅 You're currently tracking **{attendance:.1f}% attendance**. "
        "Stay consistent!"
    )

    else:

        st.markdown(
        "### 🚀 Let's get your academic journey started!"
    )

        st.caption(
        "Start by calculating your CGPA or attendance. "
        "Your dashboard will automatically build your academic overview."
    )

        empty_col1, empty_col2 = st.columns(2)

        with empty_col1:

            if st.button(
            "🧮  Calculate Your CGPA",
            use_container_width=True,
            key="dashboard_empty_cgpa"
        ):
                st.session_state["page"] = "CGPA Calculator"
                st.rerun()

        with empty_col2:

            if st.button(
            "📅  Calculate Attendance",
            use_container_width=True,
            key="dashboard_empty_attendance"
        ):
                st.session_state["page"] = "Attendance Calculator"
                st.rerun()



    st.divider()

    # ─────────────────────────────────────────────
    # KEY METRICS
    # ─────────────────────────────────────────────

    cgpa = st.session_state.get("cgpa")
    attendance = st.session_state.get("attendance")
    target_cgpa = st.session_state.get("target_cgpa")

    metric_col1, metric_col2, metric_col3 = st.columns(3)


    with metric_col1:

        with st.container(border=True):

            st.markdown("## 🟣")
            st.markdown("**CURRENT CGPA**")

            cgpa_value = (
            f"{cgpa:.2f}"
            if cgpa is not None
            else "—"
        )

            st.metric(
            "Your CGPA",
            cgpa_value,
            help="Your current overall academic performance"
        )

            if cgpa is None:

                st.caption(
                "📚 No CGPA calculated yet"
            )

                if st.button(
                "🧮 Calculate CGPA →",
                key="dashboard_calc_cgpa",
                use_container_width=True
            ):

                    st.session_state["page"] = "CGPA Calculator"
                    st.rerun()

            elif cgpa >= 9:

                st.caption(
                "🏆 Excellent academic performance"
            )

            elif cgpa >= 8:

                st.caption(
                "🔥 Very strong academic performance"
            )

            elif cgpa >= 7:

                st.caption(
                "👍 Good performance — keep improving"
            )

            else:

                st.caption(
                "📈 Focus on improving your next semester"
            )


    with metric_col2:

        with st.container(border=True):

            st.markdown("## 🔵")
            st.markdown("**ATTENDANCE**")

            attendance_value = (
            f"{attendance:.1f}%"
            if attendance is not None
            else "—"
        )

            st.metric(
            "Current Attendance",
            attendance_value,
            help="Your current attendance percentage"
        )

            if attendance is None:

                st.caption(
                "📅 No attendance recorded yet"
            )

                if st.button(
                "📅 Calculate Attendance →",
                key="dashboard_calc_attendance",
                use_container_width=True
            ):

                    st.session_state["page"] = "Attendance Calculator"
                    st.rerun()

            elif attendance >= 90:

                st.caption(
                "🔥 Excellent attendance"
            )

            elif attendance >= 75:

                st.caption(
                "👍 Good attendance — keep it consistent"
            )

            elif attendance >= 60:

                st.caption(
                "⚠️ Attendance needs some attention"
            )

            else:

                st.caption(
                "🚨 Your attendance needs immediate attention"
            )


    with metric_col3:

        with st.container(border=True):

            st.markdown("## 🟠")
            st.markdown("**CGPA TARGET**")

            target_value = (
            f"{target_cgpa:.2f}"
            if target_cgpa is not None
            else "—"
        )

            st.metric(
            "Target CGPA",
            target_value,
            help="The CGPA you are working toward"
        )

            if target_cgpa is None:

                st.caption(
                "🎯 No target set yet"
            )

                if st.button(
                "🎯 Set Your Goal →",
                key="dashboard_set_goal",
                use_container_width=True
            ):

                    st.session_state["page"] = "CGPA Goal Planner"
                    st.rerun()

            elif cgpa is None:

                st.caption(
                "📚 Calculate your CGPA to track progress"
            )

            elif cgpa >= target_cgpa:

                st.caption(
                "🎉 You've reached your CGPA target!"
            )

            else:

                target_gap = target_cgpa - cgpa

                st.caption(
                f"📈 {target_gap:.2f} CGPA points to go"
            )

    st.write("")

    st.subheader("⚡ Quick Actions")

    st.caption(
    "Jump straight into the tools you use most."
)

    action_col1, action_col2 = st.columns(2)


    with action_col1:

        if st.button(
        "🧮  Calculate CGPA",
        use_container_width=True
    ):

            st.session_state["page"] = "CGPA Calculator"
            st.rerun()


        if st.button(
        "🎯  Plan Your CGPA",
        use_container_width=True
    ):

            st.session_state["page"] = "CGPA Goal Planner"
            st.rerun()


    with action_col2:

        if st.button(
        "📅  Check Attendance",
        use_container_width=True
    ):

            st.session_state["page"] = "Attendance Calculator"
            st.rerun()


        if st.button(
        "📈  Project Attendance",
        use_container_width=True
    ):

            st.session_state["page"] = "Future Attendance Projection"
            st.rerun()


    # PROFILE SETUP

    profile_exists = bool(
    st.session_state.get("current_student_id")
    )

    editing_profile = st.session_state.get(
        "editing_profile",
        False
    )

    with st.expander(
    "🎓 Student Profile",
    expanded=True
):

        st.subheader("👤 Personal Information")

        st.caption(
        "Enter the basic details used to identify your student profile."
    )

        profile_col1, profile_col2 = st.columns(2)

        with profile_col1:

            student_name = st.text_input(
            "👤 Student Name",
            value=st.session_state.get("student_name", ""),
            placeholder="e.g. Aditya"
        )

            roll_number = st.text_input(
            "🔢 Roll Number",
            value=st.session_state.get("roll_number", ""),
            placeholder="e.g. 27",
            disabled=editing_profile
        )

            batch = st.text_input(
            "🆔 Batch / Division",
            value=st.session_state.get("batch", ""),
            placeholder="e.g. A / 2026"
        )

            email = st.text_input(
            "📧 Email",
            value=st.session_state.get("email", ""),
            placeholder="e.g. student@example.com"
        )

        with profile_col2:

            department = st.text_input(
            "🏫 Department",
            value=st.session_state.get("department", ""),
            placeholder="e.g. Computer Engineering"
        )

            college = st.text_input(
            "🏛️ College / Institute",
            value=st.session_state.get("college", ""),
            placeholder="e.g. PVG COET"
        )

            course = st.text_input(
            "🎓 Course / Degree",
            value=st.session_state.get("course", ""),
            placeholder="e.g. B.Tech"
        )

            current_semester = st.number_input(
            "📚 Current Semester",
            min_value=1,
            max_value=8,
            value=st.session_state.get("current_semester") or 1,
            step=1
        )

        st.write("")

        if st.button(
        "💾 Update Profile" if editing_profile else "💾 Save Profile",
        use_container_width=True
    ):

            student_name = student_name or ""
            roll_number = roll_number or ""
            batch = batch or ""
            department = department or ""
            course = course or ""
            college = college or ""
            email = email or ""

            existing_student_id = st.session_state.get(
            "current_student_id"
        )

            student_id = roll_number.strip()

            if not student_id:

                st.error(
                "❌ Please enter a roll number."
            )

            else:

                student_data = {

                    "name": student_name,

                    "roll_number": roll_number,

                    "batch": batch,

                    "department": department,

                    "course": course,

                    "college": college,

                    "semester": current_semester,

                    "email": email,

                    "academic": {

                        "cgpa": None,

                        "attendance": None,

                        "target_cgpa": None,

                        "target_attendance": None,

                        "completed_credits": 0,

                        "remaining_credits": 0,

                        "semesters": []

                    }

                }

                if editing_profile and existing_student_id:

                    # Keep the existing student ID while editing

                    st.session_state["students"][
                    existing_student_id
                ] = student_data

                    st.session_state[
                    "current_student_id"
                ] = existing_student_id

                else:

                    st.session_state["students"][
                    student_id
                ] = student_data

                    st.session_state[
                    "current_student_id"
                ] = student_id

                save_student(
                student_data,
                old_roll_number=(
                    existing_student_id
                    if editing_profile
                    else None
                )
            )

                st.session_state["student_name"] = student_name
                st.session_state["roll_number"] = roll_number
                st.session_state["batch"] = batch
                st.session_state["department"] = department
                st.session_state["course"] = course
                st.session_state["college"] = college
                st.session_state["current_semester"] = current_semester
                st.session_state["email"] = email

                st.success(
                "✅ Student profile saved successfully!"
            )

                st.session_state["creating_new_student"] = False
                st.session_state["editing_profile"] = False

                st.rerun()

    if (
        st.session_state["course"] is not None
        and st.session_state["current_semester"] is not None
    ):

        profile_display_col1, profile_display_col2 = st.columns(2)

        with profile_display_col1:

            st.write(
                f"🎓 **{st.session_state['course']}**"
            )

        with profile_display_col2:

            st.write(
                f"📚 **Semester {st.session_state['current_semester']}**"
            )
    

    current_cgpa = st.session_state["cgpa"]
    attendance = st.session_state["attendance"]
    target_cgpa = st.session_state["target_cgpa"]
    target_attendance = st.session_state["target_attendance"]
    completed_credits = st.session_state["completed_credits"]
    remaining_credits = st.session_state["remaining_credits"]

    if current_cgpa is None:
        current_cgpa = 0

    if attendance is None:
        attendance = 0

    #------------ 
    # TOP METRICS
    #------------

    with st.container(border=True):

        st.markdown(
            """
            <div class="snapshot-title">
                📊 Academic Snapshot
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        # Current CGPA card
        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">📚 Current CGPA</div>
                    <div class="metric-value">{current_cgpa:.2f}</div>
                    <div class="metric-subtitle">Academic performance</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Attendance card
        with col2:
            attendance_status = (
                "On track"
                if target_attendance is None
                or attendance >= target_attendance
                else "Below target"
            )

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">📅 Attendance</div>
                    <div class="metric-value">{attendance:.1f}%</div>
                    <div class="metric-subtitle">{attendance_status}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Target CGPA card
        with col3:
            target_text = (
                f"{target_cgpa:.2f}"
                if target_cgpa is not None
                else "Not set"
            )

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">🎯 CGPA Target</div>
                    <div class="metric-value">{target_text}</div>
                    <div class="metric-subtitle">Your academic goal</div>
                </div>
                """,
                unsafe_allow_html=True
            )



    # =========================
    # OVERALL STATUS
    # =========================

    if (
        current_cgpa is not None
        and target_cgpa is not None
        and attendance is not None
        and target_attendance is not None
        and completed_credits is not None
        and remaining_credits is not None
        and remaining_credits > 0
    ):

        required_sgpa = required_future_sgpa(
            current_cgpa,
            completed_credits,
            target_cgpa,
            remaining_credits
        )

        if required_sgpa > 10:

            st.error(
                "🔴 Overall Status: Needs Attention — "
                "Your current CGPA target is mathematically impossible."
            )

        elif (
            attendance < target_attendance
            and required_sgpa >= 9
        ):

            st.warning(
                "🟡 Overall Status: Needs Improvement — "
                "Both CGPA and attendance need focused attention."
            )

        elif attendance < target_attendance:

            st.warning(
                "🟡 Overall Status: Needs Improvement — "
                "Your attendance is below your target."
            )

        elif required_sgpa >= 9:

            st.warning(
                "🟡 Overall Status: Needs Improvement — "
                "Your CGPA target requires excellent performance."
            )

        else:

            st.success(
                "🟢 Overall Status: On Track — "
                "Keep maintaining your current performance!"
            )

    # =========================
    # CGPA GOAL PROGRESS
    # =========================

    if (
        current_cgpa is not None
        and target_cgpa is not None
        and target_cgpa > 0
    ):

        st.subheader("🎯 CGPA Goal Progress")

        progress = min(
            current_cgpa / target_cgpa,
            1.0
        )

        st.progress(progress)

        progress_percentage = progress * 100

        if current_cgpa >= target_cgpa:

            st.success(
                f"🎉 Target achieved! "
                f"You have reached {current_cgpa:.2f} CGPA."
            )

        else:

            remaining = target_cgpa - current_cgpa

            progress_col1, progress_col2 = st.columns(2)

            with progress_col1:

                st.metric(
                    "Goal Progress",
                    f"{progress_percentage:.1f}%"
                )

            with progress_col2:

                st.metric(
                    "Remaining CGPA",
                    f"{remaining:.2f}"
                )

    # =========================
    # CGPA ANALYTICS
    # =========================

    if current_cgpa is not None and target_cgpa is not None:

        with st.container(border=True):

            st.subheader("📊 CGPA Analytics")

            st.write(
                "Track your current CGPA against your target and monitor "
                "your semester-wise SGPA performance."
            )

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                with st.container(border=True):

                    st.write("**Current vs Target CGPA**")

                    fig1 = go.Figure()

                    fig1.add_trace(
                        go.Bar(
                        x=["Current", "Target"],
                        y=[current_cgpa, target_cgpa],
                        text=[
                            f"{current_cgpa:.2f}",
                            f"{target_cgpa:.2f}"
                        ],
                        textposition="auto"
                    )
                )

                    fig1.update_layout(
                    yaxis_title="CGPA",
                    yaxis=dict(range=[0, 10]),
                    height=400
                )

                    st.plotly_chart(
                    fig1,
                    use_container_width=True
                )

            with chart_col2:
                with st.container(border=True):

                    semesters = st.session_state["semesters"]

                    if semesters is not None and len(semesters) > 0:

                        st.write("**Semester-wise SGPA Trend**")

                        semester_numbers = []
                        sgpa_values = []

                        for i, semester in enumerate(semesters):

                            semester_numbers.append(
                            f"Sem {i + 1}"
                        )

                            sgpa_values.append(
                            semester["sgpa"]
                        )

                        fig2 = go.Figure()

                        fig2.add_trace(
                            go.Scatter(
                            x=semester_numbers,
                            y=sgpa_values,
                            mode="lines+markers",
                            name="SGPA"
                        )
                    )

                        fig2.update_layout(
                        yaxis_title="SGPA",
                        yaxis=dict(range=[0, 10]),
                        height=400
                    )

                        st.plotly_chart(
                        fig2,
                        use_container_width=True
                    )

                    else:

                        st.info(
                        "Calculate your CGPA to view your "
                        "semester-wise SGPA trend."
                    )

    #======================
    # ATTENDANCE ANALYTICS
    #======================

    if attendance is not None and target_attendance is not None:

        with st.container(border=True):

            st.subheader("📅 Attendance Analytics")

            st.write(
                "Monitor your current attendance, target attendance, "
                "and progress toward your goal."
            )

            attendance_col1, attendance_col2 = st.columns(2)

            with attendance_col1:
                with st.container(border=True):

                    st.write("**Attendance Goal Progress**")

                    progress = min(
                    attendance / target_attendance,
                    1.0
                    )

                    st.progress(progress)

                    progress_percentage = progress * 100

                    if attendance >= target_attendance:

                        st.success(
                        "🎉 You've reached your attendance target!"
                    )

                    else:

                        remaining = target_attendance - attendance

                        st.metric(
                        "Goal Progress",
                        f"{progress_percentage:.1f}%"
                    )

                        st.write(
                        f"You are **{remaining:.2f} percentage points** "
                        f"away from your attendance target."
                    )

            with attendance_col2:
                with st.container(border=True):

                    st.write("**Current vs Target Attendance**")

                    fig3 = go.Figure()

                    fig3.add_trace(
                        go.Bar(
                        x=["Current", "Target"],
                        y=[
                            attendance,
                            target_attendance
                        ],
                        text=[
                            f"{attendance:.1f}%",
                            f"{target_attendance:.1f}%"
                        ],
                        textposition="auto"
                    )
                )

                    fig3.update_layout(
                    yaxis_title="Attendance (%)",
                    yaxis=dict(range=[0, 100]),
                    height=400
                )

                    st.plotly_chart(
                    fig3,
                    use_container_width=True
                )

    #===============================
    # ACADEMIC PERFORMANCE OVERVIEW
    #===============================

    if (
        current_cgpa is not None
        and target_cgpa is not None
        and attendance is not None
        and target_attendance is not None
    ):

        with st.container(border=True):

            st.subheader("📈 Academic Performance Overview")

            st.write(
                "Get a quick visual comparison of your current academic "
                "performance against your targets."
            )

            current_cgpa_percentage = current_cgpa * 10
            target_cgpa_percentage = target_cgpa * 10

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=[
                        "Current CGPA",
                        "Target CGPA",
                        "Current Attendance",
                        "Target Attendance"
                    ],
                    y=[
                        current_cgpa_percentage,
                        target_cgpa_percentage,
                        attendance,
                        target_attendance
                    ],
                    text=[
                        f"{current_cgpa:.2f}",
                        f"{target_cgpa:.2f}",
                        f"{attendance:.1f}%",
                        f"{target_attendance:.1f}%"
                    ],
                    textposition="auto"
                )
            )

            fig.update_layout(
                yaxis_title="Performance (%)",
                yaxis=dict(range=[0, 100]),
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ─────────────────────────────────────────────
    # BADGE COLLECTION
    # ─────────────────────────────────────────────

    with st.container(border=True):

        st.subheader("🏆 Achievements")

        st.caption(
            "Collect badges by hitting academic and attendance milestones."
        )

        earned_badges = get_earned_badges()

        total_badges = len(BADGES)
        earned_count = len(earned_badges)
        remaining_count = total_badges - earned_count

        progress_value = (
            earned_count / total_badges
            if total_badges > 0
            else 0
        )

        st.progress(progress_value)

        st.caption(
            f"✨ {earned_count}/{total_badges} collected "
            f"  •  🔒 {remaining_count} remaining"
        )

        st.write("")

        owned_col, locked_col = st.columns(2)

        with owned_col:

            with st.container(border=True):

                st.markdown("**✨ OWNED**")

                owned_badges = [
                badge
                for badge in BADGES
                if badge["id"] in earned_badges
            ]

                owned_rows = [
                owned_badges[i:i + 3]
                for i in range(0, len(owned_badges), 3)
            ]

                for row in owned_rows:

                    badge_cols = st.columns(3)

                    for column, badge in zip(
                    badge_cols,
                    row
                ):

                        with column:

                            st.markdown(
                            f"""
                            <div class="badge-tile owned">
                                <div class="badge-icon">
                                    {badge["icon"]}
                                </div>
                                <div class="badge-name">
                                    {badge["name"]}
                                </div>
                                <div class="badge-rarity">
                                    {badge["rarity"]}
                                </div>
                                <div class="badge-requirement">
                                    ✓ {badge["requirement"]}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


        with locked_col:
            with st.container(border=True):

                st.markdown("**🔒 NOT OWNED**")

                locked_badges = [
                badge
                for badge in BADGES
                if badge["id"] not in earned_badges
            ]

                locked_rows = [
                locked_badges[i:i + 3]
                for i in range(0, len(locked_badges), 3)
            ]

                for row in locked_rows:

                    badge_cols = st.columns(3)

                    for column, badge in zip(
                    badge_cols,
                    row
                ):

                        with column:

                            st.markdown(
                            f"""
                            <div class="badge-tile locked">
                                <div class="badge-lock">
                                    🔒
                                </div>
                                <div class="badge-icon">
                                    {badge["icon"]}
                                </div>
                                <div class="badge-name">
                                    {badge["name"]}
                                </div>
                                <div class="badge-rarity">
                                    {badge["rarity"]}
                                </div>
                                <div class="badge-requirement">
                                    🔒 {badge["requirement"]}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

    
    #=====================
    # SMART RECOMMENDATION
    #=====================

    st.write("")

    with st.container(border=True):

        st.subheader("💡 Smart Recommendations")

        st.caption(
            "Personalized suggestions based on your current academic progress."
        )



        # CGPA recommendation

        recommendation_col1, recommendation_col2 = st.columns(2)

        with recommendation_col1:
            with st.container(border=True):

                if (
                current_cgpa is not None
                and target_cgpa is not None
                and completed_credits is not None
                and remaining_credits is not None
                and remaining_credits > 0
                ):

                    required_sgpa = required_future_sgpa(
                    current_cgpa,
                    completed_credits,
                    target_cgpa,
                    remaining_credits
                )

                    max_cgpa = maximum_possible_cgpa(
                    current_cgpa,
                    completed_credits,
                    remaining_credits
                    )

                    st.write("### 📚 CGPA Recommendation")

                    if current_cgpa >= target_cgpa:

                        st.success(
                    "🎉 You have already reached your target CGPA. "
                    "Focus on maintaining your performance."
                    )

                    elif required_sgpa > 10:

                        st.error(
                    f"❌ Your target CGPA of {target_cgpa:.2f} "
                    f"is not mathematically achievable."
                    )

                        st.write(
                    f"Maximum possible CGPA: **{max_cgpa:.2f}**"
                    )

                    elif required_sgpa >= 9:

                        st.warning(
                    f"⚠️ You need an average SGPA of "
                    f"**{required_sgpa:.2f}**."
                    )

                        st.write(
                    "This is an ambitious target. You will need "
                    "consistently excellent semester performance."
                    )

                    elif required_sgpa >= 8:

                        st.info(
                    f"🎯 You need an average SGPA of "
                    f"**{required_sgpa:.2f}** "
                    f"to reach your target CGPA."
                    )

                        st.write(
                    "Your target is challenging but achievable "
                    "with consistent performance."
                    )

                    else:

                        st.success(
                    f"🟢 You need an average SGPA of "
                    f"**{required_sgpa:.2f}**."
                    )

                        st.write(
                    "Your target is currently within a comfortable "
                    "range. Keep maintaining your performance."
                    )

                else:

                    st.info(
                "Calculate your CGPA goal to receive a personalized "
                "CGPA recommendation."
                )

        with recommendation_col2:

            with st.container(border=True):

            # Attendance recommendation

                if (
                attendance is not None
                and target_attendance is not None
                ):

                    st.write("### 📅 Attendance Recommendation")

                    if attendance >= target_attendance:

                        st.success(
                    f"🎉 Your attendance is **{attendance:.2f}%**, "
                    f"above your target of **{target_attendance:.1f}%**. "
                    "Keep it up!"
                    )

                    else:

                        attendance_gap = target_attendance - attendance

                        st.warning(
                    f"⚠️ Your attendance is **{attendance:.2f}%**, "
                    f"which is **{attendance_gap:.2f} percentage points** "
                    f"below your target."
                    )

                        st.write(
                    "Try to attend upcoming classes consistently "
                    "to improve your attendance."
                    )

                else:

                    st.info(
                "Calculate your attendance goal to receive a "
                "personalized attendance recommendation."
                )

    #--------------------
    # PERFORMANCE SUMMARY
    #--------------------

    if (
        current_cgpa is not None
        and attendance is not None
    ):

        with st.container(border=True):

            st.subheader("📋 Performance Summary")

            summary_col1, summary_col2 = st.columns(2)

            with summary_col1:
                with st.container(border=True):

                    st.write("### 📚 CGPA")

                    if target_cgpa is not None:

                        if current_cgpa >= target_cgpa:

                            st.success(
                            "🎉 Target achieved"
                        )

                        else:

                            st.warning(
                            "📈 Target not yet achieved"
                        )

                        st.write(
                        f"Current: **{current_cgpa:.2f}**"
                    )

                        st.write(
                        f"Target: **{target_cgpa:.2f}**"
                    )

                    else:

                        st.info(
                        "No CGPA target set."
                    )

            with summary_col2:
                with st.container(border=True):

                    st.write("### 📅 Attendance")

                    if target_attendance is not None:

                        if attendance >= target_attendance:

                            st.success(
                            "🎉 Target achieved"
                        )

                        else:

                            st.warning(
                            "📈 Below target"
                        )

                        st.write(
                        f"Current: **{attendance:.2f}%**"
                    )

                        st.write(
                        f"Target: **{target_attendance:.1f}%**"
                    )

                    else:

                        st.info(
                        "No attendance target set."
                    )

    # ===========
    # FINAL INFO
    # ===========

    with st.container(border=True):

        st.subheader("ℹ️ About GradeTrack")

        st.write(
            "GradeTrack helps college students monitor their academic "
            "performance, track attendance, and plan future goals."
        )

        st.caption(
            "Built with Python, Streamlit, Pandas and Plotly."
        )


# -----------------------------
# CGPA Calculator
# -----------------------------

elif page == "CGPA Calculator":

    st.header("📚 CGPA Calculator")

    st.caption(
        "Calculate your overall CGPA using your semester SGPA and credits."
    )

    st.info(
        "💡 Enter the SGPA and credits for each completed semester. "
        "GradeTrack will calculate your credit-weighted CGPA."
    )

    with st.container(border=True):

        st.subheader("📖 Semester Details")

        st.caption(
            "Add the SGPA and credits for each completed semester."
        )

        number_of_semesters = st.number_input(
            "Number of semesters",
            min_value=1,
            max_value=12,
            value=1,
            step=1
        )

        st.write("")

        semesters = []

        for i in range(number_of_semesters):

            st.markdown(
                f"**📘 Semester {i + 1}**"
            )

            col1, col2 = st.columns(2)

            with col1:

                sgpa = st.number_input(
                    f"SGPA - Semester {i + 1}",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.0,
                    step=0.01,
                    key=f"sgpa_{i}"
                )

            with col2:

                credits = st.number_input(
                    f"Credits - Semester {i + 1}",
                    min_value=1,
                    max_value=50,
                    value=20,
                    step=1,
                    key=f"credits_{i}"
                )

            semesters.append({
                "sgpa": sgpa,
                "credits": credits
            })

            if i < number_of_semesters - 1:
                st.divider()

    st.write("")

    if st.button(
        "🧮  Calculate CGPA",
        use_container_width=True
    ):

        cgpa = calculate_cgpa(semesters)

        st.session_state["cgpa"] = cgpa
        st.session_state["semesters"] = semesters

        save_academic_data()

        with st.container(border=True):

            st.subheader("🎉 Your CGPA Result")

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.metric(
                    "Overall CGPA",
                    f"{cgpa:.2f}"
                )

            with result_col2:

                if cgpa >= 9:
                    performance = "🏆 Excellent"
                elif cgpa >= 8:
                    performance = "🔥 Very Good"
                elif cgpa >= 7:
                    performance = "👍 Good"
                elif cgpa >= 6:
                    performance = "📈 Keep Improving"
                else:
                    performance = "💪 Keep Working"

                st.metric(
                    "Performance",
                    performance
                )

            st.write("")

            if cgpa >= 9:
                st.success(
                    "🏆 Excellent work! You're currently in elite "
                    "academic territory."
                )
            elif cgpa >= 8:
                st.info(
                    "🔥 Strong performance! Keep this consistency "
                    "going across your remaining semesters."
                )
            elif cgpa >= 7:
                st.warning(
                    "👍 You're on a solid track. Improving your "
                    "next few semesters can push your CGPA even higher."
                )
            else:
                st.info(
                    "📈 This is your starting point. Use GradeTrack's "
                    "goal planner to see what SGPA you need next."
                )

            st.caption(
                "Your CGPA is calculated using a credit-weighted "
                "average of your semester SGPAs."
            )


# -----------------------------
# CGPA Goal Planner
# -----------------------------

if page == "CGPA Goal Planner":

    st.header("🎯 CGPA Goal Planner")

    st.caption(
        "Build your academic roadmap and find the average SGPA "
        "you need to reach your target CGPA."
    )

    st.info(
        "💡 Enter your current academic progress, choose your target, "
        "and GradeTrack will calculate the SGPA required in your "
        "remaining credits."
    )

    with st.container(border=True):

        st.subheader("📋 Your Academic Plan")

        st.caption(
            "Tell GradeTrack where you are now and where you want to go."
        )

        input_col1, input_col2 = st.columns(2)

        with input_col1:

            st.markdown("**📚 Current Progress**")

            current_cgpa = st.number_input(
                "Current CGPA",
                min_value=0.0,
                max_value=10.0,
                value=8.0,
                step=0.1
            )

            completed_credits = st.number_input(
                "Completed Credits",
                min_value=0,
                value=60,
                step=1
            )

        with input_col2:

            st.markdown("**🎯 Your Target**")

            target_cgpa = st.number_input(
                "Target CGPA",
                min_value=0.0,
                max_value=10.0,
                value=9.0,
                step=0.1
            )

            remaining_credits = st.number_input(
                "Remaining Credits",
                min_value=0,
                value=60,
                step=1
            )

    st.write("")

    if st.button(
        "🎯  Calculate Required SGPA",
        use_container_width=True
    ):

        required_sgpa = required_future_sgpa(
            current_cgpa,
            completed_credits,
            target_cgpa,
            remaining_credits
        )

        max_cgpa = maximum_possible_cgpa(
            current_cgpa,
            completed_credits,
            remaining_credits
        )

        st.session_state["target_cgpa"] = target_cgpa
        st.session_state["completed_credits"] = completed_credits
        st.session_state["remaining_credits"] = remaining_credits

        save_academic_data()

        with st.container(border=True):

            st.subheader("📊 Your CGPA Roadmap")

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.metric(
                    "Required Average SGPA",
                    f"{required_sgpa:.2f}"
                )

            with result_col2:

                st.metric(
                    "Maximum Possible CGPA",
                    f"{max_cgpa:.2f}"
                )

            st.write("")

            if current_cgpa >= target_cgpa:

                st.success(
                    f"🎉 You've already reached your target CGPA "
                    f"of **{target_cgpa:.2f}**!"
                )

            elif required_sgpa > 10:

                st.error(
                    f"❌ Your target CGPA of **{target_cgpa:.2f}** "
                    "is currently mathematically impossible."
                )

                st.info(
                    f"Even with a **10.00 SGPA** in every remaining "
                    f"credit, your maximum possible CGPA is "
                    f"**{max_cgpa:.2f}**."
                )

            elif required_sgpa >= 9:

                st.warning(
                    f"⚠️ You need an average SGPA of "
                    f"**{required_sgpa:.2f}** in your remaining credits."
                )

                st.write(
                    "This is an ambitious target. You'll need "
                    "consistently excellent semester performance."
                )

            elif required_sgpa >= 8:

                st.info(
                    f"🎯 You need an average SGPA of "
                    f"**{required_sgpa:.2f}** in your remaining credits."
                )

                st.write(
                    "Your target is challenging but achievable "
                    "with consistent performance."
                )

            else:

                st.success(
                    f"🟢 You need an average SGPA of "
                    f"**{required_sgpa:.2f}** in your remaining credits."
                )

                st.write(
                    "Your target is currently within a comfortable "
                    "range. Keep maintaining your performance."
                )

            st.caption(
                "This roadmap is based on your current CGPA, "
                "completed credits, target CGPA, and remaining credits."
            )


# -----------------------------
# Attendance Calculator
# -----------------------------

elif page == "Attendance Calculator":

    st.header("📅 Attendance Calculator")

    st.caption(
        "Calculate your current attendance percentage "
        "from classes attended and total classes conducted."
    )

    st.info(
        "💡 Enter your current attendance details and GradeTrack "
        "will calculate your attendance percentage instantly."
    )

    with st.container(border=True):

        st.subheader("📋 Attendance Details")

        st.caption(
            "Enter how many classes you've attended and how many "
            "have been conducted so far."
        )


        col1, col2 = st.columns(2)

        with col1:

            st.markdown("**✅ Classes Attended**")

            attended = st.number_input(
                "Classes Attended",
                min_value=0,
                value=40,
                step=1
            )

        with col2:

            st.markdown("**📚 Total Classes**")

            conducted = st.number_input(
                "Total Classes Conducted",
                min_value=0,
                value=50,
                step=1
            )

    st.write("")

    if st.button(
        "📅  Calculate Attendance",
        use_container_width=True
    ):

        if conducted <= 0:

            st.warning(
                "⚠️ Total classes conducted must be greater than 0."
            )

        elif attended > conducted:

            st.error(
                "❌ Classes attended cannot be greater than "
                "classes conducted."
            )

        else:

            attendance = calculate_attendance(
                attended,
                conducted
            )

            st.session_state["attendance"] = attendance

            save_academic_data()

            with st.container(border=True):

                st.subheader("📊 Your Attendance Result")

                result_col1, result_col2 = st.columns(2)

                with result_col1:

                    st.metric(
                        "Current Attendance",
                        f"{attendance:.2f}%"
                    )

                with result_col2:

                    if attendance >= 90:
                        status = "🔥 Excellent"
                    elif attendance >= 75:
                        status = "👍 Good"
                    elif attendance >= 60:
                        status = "⚠️ Needs Attention"
                    else:
                        status = "🚨 Low"

                    st.metric(
                        "Attendance Status",
                        status
                    )

                st.write("")

                if attendance >= 90:

                    st.success(
                        "🔥 Excellent attendance! You're maintaining "
                        "a very strong attendance record."
                    )

                elif attendance >= 75:

                    st.info(
                        "👍 Your attendance is in a good range. "
                        "Keep attending classes consistently."
                    )

                elif attendance >= 60:

                    st.warning(
                        "⚠️ Your attendance needs attention. "
                        "Try to be more consistent with upcoming classes."
                    )

                else:

                    st.error(
                        "🚨 Your attendance is quite low. "
                        "You'll need to attend upcoming classes consistently."
                    )

                st.caption(
                    "Attendance is calculated as classes attended "
                    "divided by total classes conducted."
                )


# -----------------------------
# Attendance Goal Planner
# -----------------------------

elif page == "Attendance Goal Planner":

    st.header("🎯 Attendance Goal Planner")

    st.caption(
        "Find out how many consecutive classes you need to attend "
        "to reach your target attendance."
    )

    st.info(
        "💡 Enter your current attendance details and set your target. "
        "GradeTrack will calculate the number of classes you need "
        "to attend consecutively."
    )

    with st.container(border=True):

        st.subheader("📋 Attendance Plan")

        st.caption(
            "Tell GradeTrack where your attendance stands "
            "and where you want it to be."
        )


        input_col1, input_col2 = st.columns(2)

        with input_col1:

            st.markdown("**📚 Current Attendance**")

            attended = st.number_input(
                "Classes Attended",
                min_value=0,
                value=40,
                step=1
            )

            conducted = st.number_input(
                "Total Classes Conducted",
                min_value=0,
                value=50,
                step=1
            )

        with input_col2:

            st.markdown("**🎯 Your Target**")

            target_attendance = st.number_input(
                "Target Attendance (%)",
                min_value=0.0,
                max_value=100.0,
                value=85.0,
                step=1.0
            )

    st.write("")

    if st.button(
        "🎯  Calculate Required Classes",
        use_container_width=True
    ):

        if conducted <= 0:

            st.error(
                "❌ Total classes conducted must be greater than 0."
            )

        elif attended > conducted:

            st.error(
                "❌ Classes attended cannot be greater than "
                "total classes conducted."
            )

        else:

            current_attendance = calculate_attendance(
                attended,
                conducted
            )

            required_classes = classes_needed_for_target(
                attended,
                conducted,
                target_attendance
            )

            st.session_state["attendance"] = current_attendance
            st.session_state["target_attendance"] = target_attendance

            save_academic_data()

            with st.container(border=True):

                st.subheader("📊 Your Attendance Roadmap")

                result_col1, result_col2 = st.columns(2)

                with result_col1:

                    st.metric(
                        "Current Attendance",
                        f"{current_attendance:.2f}%"
                    )

                with result_col2:

                    st.metric(
                        "Target Attendance",
                        f"{target_attendance:.1f}%"
                    )

                st.write("")

                if current_attendance >= target_attendance:

                    st.success(
                        f"🎉 You've already reached your target "
                        f"attendance of **{target_attendance:.1f}%**!"
                    )

                    st.caption(
                        "Keep attending consistently to maintain "
                        "your attendance level."
                    )

                else:

                    st.warning(
                        f"📚 You need to attend the next "
                        f"**{required_classes} classes consecutively** "
                        f"to reach **{target_attendance:.1f}%** attendance."
                    )

                    st.info(
                        "💪 Every upcoming class matters. Stay consistent "
                        "and avoid unnecessary absences while recovering "
                        "your attendance."
                    )

                st.caption(
                    "The required-class estimate assumes you attend "
                    "every upcoming class until the target is reached."
                )

# -----------------------------
# Future Attendance Projection
# -----------------------------

elif page == "Future Attendance Projection":

    st.header("📈 Future Attendance Projection")

    st.caption(
        "Predict how your attendance could change based on "
        "your upcoming classes."
    )

    st.info(
        "💡 Enter your current attendance and estimate how many "
        "upcoming classes you expect to attend."
    )

    with st.container(border=True):

        st.subheader("📋 Attendance Projection")

        st.caption(
            "Enter your current attendance first, then estimate "
            "your future attendance."
        )


        st.markdown("**📚 Current Attendance**")

        current_col1, current_col2 = st.columns(2)

        with current_col1:

            attended = st.number_input(
                "Current Classes Attended",
                min_value=0,
                value=40,
                step=1
            )

        with current_col2:

            conducted = st.number_input(
                "Current Total Classes Conducted",
                min_value=0,
                value=50,
                step=1
            )

        st.divider()

        st.markdown("**🔮 Future Attendance**")

        future_col1, future_col2 = st.columns(2)

        with future_col1:

            future_classes = st.number_input(
                "Upcoming Classes",
                min_value=0,
                value=20,
                step=1
            )

        with future_col2:

            future_attended = st.number_input(
                "Upcoming Classes You Will Attend",
                min_value=0,
                value=18,
                step=1
            )

    st.write("")

    if st.button(
        "📈  Project Attendance",
        use_container_width=True
    ):

        if conducted <= 0:

            st.error(
                "❌ Current total classes conducted must be "
                "greater than 0."
            )

        elif attended > conducted:

            st.error(
                "❌ Classes attended cannot be greater than "
                "classes conducted."
            )

        elif future_attended > future_classes:

            st.error(
                "❌ Future classes attended cannot be greater "
                "than upcoming classes."
            )

        else:

            current_attendance = calculate_attendance(
                attended,
                conducted
            )

            projected = projected_attendance(
                attended,
                conducted,
                future_classes,
                future_attended
            )

            st.session_state["attendance"] = current_attendance

            save_academic_data()

            with st.container(border=True):

                st.subheader("📊 Your Projection")

                result_col1, result_col2 = st.columns(2)

                with result_col1:

                    st.metric(
                        "Current Attendance",
                        f"{current_attendance:.2f}%"
                    )

                with result_col2:

                    st.metric(
                        "Projected Attendance",
                        f"{projected:.2f}%"
                    )

                st.write("")

                if projected > current_attendance:

                    improvement = projected - current_attendance

                    st.success(
                        f"📈 Your attendance could increase to "
                        f"**{projected:.2f}%**."
                    )

                    st.caption(
                        f"That's an improvement of "
                        f"**{improvement:.2f} percentage points**."
                    )

                    st.info(
                        "🔥 Your planned attendance is helping "
                        "improve your overall percentage."
                    )

                elif projected < current_attendance:

                    decrease = current_attendance - projected

                    st.warning(
                        f"📉 Your attendance could fall to "
                        f"**{projected:.2f}%**."
                    )

                    st.caption(
                        f"That's a decrease of "
                        f"**{decrease:.2f} percentage points**."
                    )

                    st.info(
                        "⚠️ Missing too many upcoming classes could "
                        "pull your overall attendance down."
                    )

                else:

                    st.info(
                        "➡️ Your projected attendance will remain "
                        "unchanged."
                    )

                    st.caption(
                        "Your future attendance plan matches "
                        "your current attendance rate."
                    )

                st.caption(
                    "The projection combines your current attendance "
                    "with the number of upcoming classes you expect "
                    "to attend."
                )