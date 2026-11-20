
import streamlit as st
import pandas as pd

from recommender import EducationRecommender
from blockchain import EducationBlockchain


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Smart Education AI",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(120deg, #172554, #2563eb);
    padding: 30px;
    border-radius: 15px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
}

.hero p {
    color: #dbeafe;
    font-size: 17px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

.course-card {
    background: white;
    border: 1px solid #e2e8f0;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 15px;
}

.small-text {
    color: #64748b;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- INITIALIZE SYSTEM ----------------

@st.cache_resource
def load_recommender():
    return EducationRecommender("data/courses.csv")


recommender = load_recommender()
blockchain = EducationBlockchain()


# ---------------- SESSION STATE ----------------

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "student_id" not in st.session_state:
    st.session_state.student_id = None


# ---------------- SIDEBAR ----------------

st.sidebar.title("🎓 Smart Education")
st.sidebar.caption("AI-Powered Learning Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "AI Recommendations",
        "Course Catalogue",
        "Blockchain Explorer",
        "About Project"
    ]
)

st.sidebar.divider()
st.sidebar.success("AI Engine: Active")
st.sidebar.success("Blockchain: Active")


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Smart Education Recommendation System</h1>
        <p>
        Discover the right learning path using Artificial Intelligence
        and secure blockchain technology.
        </p>
    </div>
    """, unsafe_allow_html=True)

    courses = recommender.courses
    chain = blockchain.get_chain()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Available Courses",
        len(courses)
    )

    col2.metric(
        "Blockchain Records",
        len(chain)
    )

    col3.metric(
        "Course Categories",
        courses["category"].nunique()
    )

    st.divider()

    st.subheader("Welcome to Smart Education")

    st.write("""
    This platform helps students identify suitable educational
    opportunities based on their academic background, skills,
    interests and future career ambitions.

    The system combines:

    - Artificial Intelligence for personalized recommendations.
    - Machine Learning using TF-IDF and cosine similarity.
    - Blockchain-inspired technology for recommendation integrity.
    - Interactive Streamlit dashboards for students.
    """)

    st.subheader("How the system works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("**01. Student Profile**\n\nEnter your skills, interests and career goals.")

    with col2:
        st.info("**02. AI Analysis**\n\nThe recommendation engine finds relevant courses.")

    with col3:
        st.info("**03. Blockchain Record**\n\nThe recommendation event is recorded in the hash chain.")


# ---------------- AI RECOMMENDATIONS ----------------

elif page == "AI Recommendations":

    st.title("🤖 AI Education Recommendations")

    st.write(
        "Tell us about yourself to discover your personalized learning path."
    )

    with st.form("student_form"):

        student_id = st.text_input(
            "Student ID",
            placeholder="Example: STUDENT001"
        )

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Student Name")

            education = st.selectbox(
                "Academic Background",
                [
                    "High School",
                    "Diploma",
                    "Undergraduate",
                    "Postgraduate",
                    "Other"
                ]
            )

            level = st.selectbox(
                "Learning Level",
                [
                    "Beginner",
                    "Intermediate",
                    "Advanced"
                ]
            )

        with col2:
            career_goal = st.selectbox(
                "Career Goal",
                [
                    "AI Engineer",
                    "Data Scientist",
                    "Python Developer",
                    "Web Developer",
                    "Cloud Engineer",
                    "Security Analyst",
                    "Blockchain Developer",
                    "UX Designer",
                    "Mobile Developer",
                    "Data Analyst",
                    "Other"
                ]
            )

            interests = st.text_input(
                "Interests",
                placeholder="AI, programming, data science"
            )

            skills = st.text_input(
                "Existing Skills",
                placeholder="Python, SQL, communication"
            )

        top_n = st.slider(
            "Number of recommendations",
            min_value=3,
            max_value=10,
            value=5
        )

        submitted = st.form_submit_button(
            "🚀 Generate Recommendations",
            use_container_width=True
        )

    if submitted:

        if not student_id.strip() or not name.strip():
            st.error("Please enter your Student ID and name.")

        elif not interests.strip() and not skills.strip():
            st.error("Please enter at least your interests or skills.")

        else:
            with st.spinner("AI is analyzing your learning profile..."):

                results = recommender.recommend(
                    interests=interests,
                    skills=skills,
                    career_goal=career_goal,
                    level=level,
                    top_n=top_n
                )

                if results.empty:
                    st.warning("No matching courses found.")
                else:
                    st.session_state.recommendations = results
                    st.session_state.student_id = student_id

                    recommendation_ids = (
                        results["course_id"].astype(str).tolist()
                    )

                    record = blockchain.add_record(
                        student_id=student_id,
                        recommendations=recommendation_ids
                    )

                    st.session_state.latest_block = record

                    st.session_state.student_profile = {
                        "name": name,
                        "education": education,
                        "level": level,
                        "career_goal": career_goal
                    }

                    st.success(
                        "Recommendations generated and blockchain record created!"
                    )

    if st.session_state.recommendations is not None:

        results = st.session_state.recommendations

        st.divider()
        st.subheader("Your Personalized Recommendations")

        for _, course in results.iterrows():

            percentage = float(course["match_percentage"])

            st.markdown(
                f"""
                <div class="course-card">
                    <h3>{course['course_name']}</h3>
                    <p class="small-text">
                    {course['category']} | {course['level']}
                    </p>
                    <p>{course['description']}</p>
                    <b>Career Path:</b> {course['career']}<br><br>
                    <b>AI Match Score: {percentage:.2f}%</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(min(percentage / 100, 1.0))

        st.info(
            "These scores measure text similarity between your profile "
            "and course descriptions. They are not probabilities of success."
        )

        if "latest_block" in st.session_state:
            block = st.session_state.latest_block

            st.subheader("Blockchain Confirmation")

            st.code(block["hash"], language="text")

            st.caption(
                f"Block #{block['index']} | {block['timestamp']}"
            )


# ---------------- COURSE CATALOGUE ----------------

elif page == "Course Catalogue":

    st.title("📚 Course Catalogue")

    courses = recommender.courses

    categories = ["All"] + sorted(
        courses["category"].unique().tolist()
    )

    selected_category = st.selectbox(
        "Filter by Category",
        categories
    )

    if selected_category != "All":
        courses = courses[
            courses["category"] == selected_category
        ]

    search = st.text_input("Search courses")

    if search:
        mask = courses["combined_text"].str.contains(
            search,
            case=False,
            na=False
        )
        courses = courses[mask]

    st.write(f"Found {len(courses)} courses")

    st.dataframe(
        courses[
            [
                "course_id",
                "course_name",
                "category",
                "skills",
                "level",
                "career"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ---------------- BLOCKCHAIN EXPLORER ----------------

elif page == "Blockchain Explorer":

    st.title("⛓️ Blockchain Explorer")

    chain = blockchain.get_chain()

    valid, message = blockchain.verify_chain()

    col1, col2 = st.columns(2)

    col1.metric("Total Blocks", len(chain))

    col2.metric(
        "Integrity Status",
        "Valid" if valid else "Invalid"
    )

    if valid:
        st.success(message)
    else:
        st.error(message)

    st.divider()

    st.subheader("Blockchain Records")

    if not chain:
        st.info("No recommendation records available yet.")

    for block in reversed(chain):

        with st.expander(
            f"Block #{block['index']} - {block['student_id']}"
        ):

            st.write("**Timestamp:**", block["timestamp"])

            st.write(
                "**Recommendations:**",
                ", ".join(block["recommendations"])
            )

            st.write("**Previous Hash:**")
            st.code(block["previous_hash"])

            st.write("**Current Hash:**")
            st.code(block["hash"])

    st.divider()

    if st.button("🔍 Verify Blockchain Integrity"):
        valid, message = blockchain.verify_chain()

        if valid:
            st.success(message)
        else:
            st.error(message)


# ---------------- ABOUT PROJECT ----------------

elif page == "About Project":

    st.title("About the Project")

    st.markdown("""
    ## Smart Education Recommendation System Using AI and Blockchain

    ### Project Objective

    To develop an intelligent educational recommendation platform
    that suggests relevant learning opportunities based on individual
    student profiles.

    ### Technologies Used

    | Technology | Purpose |
    |---|---|
    | Python | Core programming |
    | Streamlit | Web application |
    | Pandas | Dataset management |
    | Scikit-learn | AI recommendation engine |
    | TF-IDF | Text feature extraction |
    | Cosine Similarity | Recommendation matching |
    | SHA-256 | Cryptographic hashing |
    | Blockchain | Tamper-evident audit records |

    ### System Modules

    1. Student Profile Management
    2. AI-Based Course Recommendation
    3. Course Catalogue
    4. Blockchain Record Management
    5. Blockchain Integrity Verification

    ### Future Enhancements

    - Student performance prediction.
    - Advanced deep learning recommendation models.
    - Verified certificates.
    - Smart contract integration.
    - Institution and administrator dashboards.
    """)
    
    st.caption(
        "Academic prototype. The current hash-chain ledger is locally "
        "stored and is not a decentralized blockchain network."
    )


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    "<center>Smart Education Recommendation System | "
    "AI + Blockchain | Python & Streamlit</center>",
    unsafe_allow_html=True
)
