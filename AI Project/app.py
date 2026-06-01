import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree

# PAGE SETTINGS
st.set_page_config(
    page_title="FutureGrade AI",
    page_icon="🤖",
    layout="wide"
)

# LOAD CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# LOGIN SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_name" not in st.session_state:
    st.session_state.student_name = ""   

# LOGIN PAGE
if not st.session_state.logged_in:
    st.markdown(
        """
        <div class="login-container">
        <h1>🤖 AI Student Performance System 🤖</h1>
        <p class="login-text">
        Futuristic AI-Based Student Prediction Dashboard
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    student_name = st.text_input("Enter Student Name")
    student_id = st.text_input("Enter Student ID")

    if st.button("Login"):
        if student_name != "" and student_id != "":
            st.session_state.logged_in = True
            st.session_state.student_name = student_name
            st.rerun()
        else:
            st.warning("Please Enter All Details")

# MAIN APP
else:
    st.sidebar.title("🤖 Navigation")
    st.sidebar.success(f"Welcome {st.session_state.student_name}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
        
    # FIX 1: Added proper parentheses around the radio button options
    menu = st.sidebar.radio(
        "Select Page",
        [
            "Home",
            "Train Model",
            "Prediction",
            "About"
        ]
    )
    
    # LOAD DATASET
    data = pd.read_csv("dataset.csv")

    # FIX 2: Indented all the page content blocks so they reside inside the 'else' scope
    # HOME PAGE
    if menu == "Home":
        st.title("🤖 AI Student Performance Dashboard 🤖")
        st.write("---")
        st.subheader("Dataset Preview")
        st.dataframe(data)
        st.write("---")
        st.subheader("Project Description")
        st.write(
            """
            This futuristic AI software predicts
            student academic performance using
            a Decision Tree Machine Learning model.
            """
        )

    # TRAIN MODEL PAGE
    elif menu == "Train Model":
        st.title("🌳 Train AI Decision Tree 🌳")
        criterion = st.selectbox(
            "Select Criterion",
            ["gini", "entropy"]
        )
        max_depth = st.slider(
            "Select Max Depth",
            1,
            10,
            3
        )

        # FEATURES
        X = data[[
            "Subject",
            "StudyHours",
            "Attendance",
            "CorrectAnswers",
            "WrongAnswers",
            "Assignment"
        ]]

        # LABEL
        y = data["Result"]

        # MODEL
        model = DecisionTreeClassifier(
            criterion=criterion,
            max_depth=max_depth,
            random_state=42
        )

        model.fit(X, y)
        st.write("---")
        st.subheader("Decision Tree Visualization")

        # FIGURE
        fig, ax = plt.subplots(figsize=(12, 6))

        # LIGHT BLUE BACKGROUND
        fig.patch.set_facecolor('#E6F7FF')
        ax.set_facecolor('#E6F7FF')

        # DECISION TREE
        plot_tree(
            model,
            feature_names=[
                "Subject",
                "StudyHours",
                "Attendance",
                "CorrectAnswers",
                "WrongAnswers",
                "Assignment"
            ],
            class_names=model.classes_,
            filled=True,
            rounded=True,
            fontsize=9,
            proportion=True,
            ax=ax
        )

        # LIGHT BLUE BORDER
        for collection in ax.collections:
            collection.set_edgecolor("#87CEFA")
            collection.set_linewidth(2)

        # BLACK TEXT
        for text in ax.texts:
            text.set_color("black")

        plt.tight_layout()
        st.pyplot(fig)

    # PREDICTION PAGE
    elif menu == "Prediction":
        st.title("🧑‍🎓 Student Performance Prediction 🧑‍🎓")

        # SUBJECT
        subject = st.selectbox(
            "Select Subject",
            ["Math IV", "COA", "AI", "DAA", "OS", "DBMS"]
        )

        # SUBJECT ENCODING
        subject_mapping = {
            "Math IV": 0,
            "COA": 1,
            "AI": 2,
            "DAA": 3,
            "OS": 4,
            "DBMS": 5,
        }

        subject_value = subject_mapping[subject]

        # STUDY HOURS
        study_hours = st.slider(
            "Study Hours",
            0,
            10,
            5
        )

        # ATTENDANCE
        attendance = st.slider(
            "Attendance Percentage",
            0,
            100,
            60
        )

        # CORRECT ANSWERS
        correct_answers = st.slider(
            "Correct Answers",
            0,
            20,
            10
        )

        # WRONG ANSWERS
        wrong_answers = st.slider(
            "Wrong Answers",
            0,
            20,
            5
        )

        # ASSIGNMENT
        assignment = st.selectbox(
            "Assignment Submitted",
            ["No", "Yes"]
        )

        assignment_value = 1 if assignment == "Yes" else 0

        # FEATURES
        X = data[[
            "Subject",
            "StudyHours",
            "Attendance",
            "CorrectAnswers",
            "WrongAnswers",
            "Assignment"
        ]]

        # LABEL
        y = data["Result"]

        # MODEL
        model = DecisionTreeClassifier()
        model.fit(X, y)

        # INPUT DATA
        input_data = pd.DataFrame(
            [[
                subject_value,
                study_hours,
                attendance,
                correct_answers,
                wrong_answers,
                assignment_value
            ]],
            columns=[
                "Subject",
                "StudyHours",
                "Attendance",
                "CorrectAnswers",
                "WrongAnswers",
                "Assignment"
            ]
        )

        # FINAL RULE
        fail_reason = ""
        if attendance < 60:
            prediction = ["Fail"]
            fail_reason = "Attendance Below 60%"
        elif assignment == "No":
            prediction = ["Fail"]
            fail_reason = "Assignment Not Submitted"
        else:
            prediction = ["Pass"]

        # BUTTON
        if st.button("Predict Result"):
            # PASS RESULT
            if prediction[0] == "Pass":
                st.markdown(
                    f'''
                    <div class="result-box">
                    🎉😊 STUDENT WILL PASS 😊🎉
                    <br><br>
                    Attendance: {attendance}%
                    <br>
                    Assignment Submitted: {assignment}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
            # FAIL RESULT
            else:
                st.markdown(
                    f'''
                    <div class="result-box">
                    ❌😔 STUDENT WILL FAIL 😔❌
                    <br><br>
                    Reason: {fail_reason}
                    <br><br>
                    Current Attendance: {attendance}%
                    <br>
                    Assignment Submitted: {assignment}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

    # ABOUT PAGE
    elif menu == "About":
        st.title("🤖 About This Project 🤖")
        st.write(
            """
            FutureGrade AI is an AI-powered student performance prediction system designed to analyze academic factors such as study hours, 
            attendance percentage, assignment completion, subject performance, and assessment results. Using the Decision Tree Machine Learning algorithm, 
            the system predicts whether a student is likely to pass or fail and presents the results through an interactive and user-friendly dashboard. The project demonstrates the practical application of Artificial Intelligence in educational analytics and student performance monitoring.
            """
        )
        st.write(
            """
            Technologies Used:
            • Python
            • Streamlit
            • Scikit-learn
            • Pandas
            • Matplotlib
            """
        )