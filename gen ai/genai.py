import streamlit as st
import pyttsx3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
st.set_page_config(page_title="AI Interview Simulator", layout="centered")
st.title("🎯 AI Placement Interview Simulator")
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
if "role" not in st.session_state:
    st.session_state.role = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "scores" not in st.session_state:
    st.session_state.scores = []
if "submitted" not in st.session_state:
    st.session_state.submitted = False
basic_questions = [
{"question":"Tell me about yourself",
"ideal":"I am a B.Tech student passionate about technology, programming and problem solving."},
{"question":"What are your strengths?",
"ideal":"My strengths are problem solving ability, quick learning and dedication."},
{"question":"What is your weakness?",
"ideal":"Sometimes I overthink but I am improving through better planning."},
{"question":"Why should we hire you?",
"ideal":"I am hardworking, eager to learn and ready to contribute to the company."},
{"question":"Where do you see yourself in 5 years?",
"ideal":"I see myself as a skilled professional working on impactful projects."}
]
role_questions = {
"Software Developer":[
{"question":"What is Object Oriented Programming?",
"ideal":"OOP is a programming paradigm based on objects and classes including encapsulation inheritance polymorphism and abstraction"},
{"question":"Difference between stack and queue",
"ideal":"Stack follows LIFO order while queue follows FIFO order"},
{"question":"What is a pointer?",
"ideal":"A pointer stores the memory address of another variable"},
{"question":"What is recursion?",
"ideal":"Recursion is a function calling itself to solve smaller instances of a problem"}
],
"Data Scientist":[
{"question":"What is machine learning?",
"ideal":"Machine learning allows computers to learn patterns from data and make predictions"},
{"question":"What is overfitting?",
"ideal":"Overfitting happens when a model performs well on training data but poorly on new data"},
{"question":"What is data preprocessing?",
"ideal":"Data preprocessing involves cleaning transforming and organizing data"},
{"question":"What is regression?",
"ideal":"Regression predicts continuous numerical values"}
],
"AI/ML Engineer":[
{"question":"What is supervised learning?",
"ideal":"Supervised learning uses labeled data to train models"},
{"question":"What is neural network?",
"ideal":"A neural network is a system of interconnected nodes inspired by the human brain"},
{"question":"What is gradient descent?",
"ideal":"Gradient descent is an optimization algorithm used to minimize loss functions"},
{"question":"What is deep learning?",
"ideal":"Deep learning uses neural networks with multiple layers"}
],
"Web Developer":[
{"question":"What is HTML?",
"ideal":"HTML structures web page content"},
{"question":"What is CSS?",
"ideal":"CSS styles and designs web pages"},
{"question":"What is JavaScript?",
"ideal":"JavaScript adds interactivity to websites"},
{"question":"What is responsive design?",
"ideal":"Responsive design adapts websites to different screen sizes"}
],
"Cyber Security":[
{"question":"What is encryption?",
"ideal":"Encryption converts data into secure coded form"},
{"question":"What is firewall?",
"ideal":"Firewall protects network by filtering traffic"},
{"question":"What is phishing?",
"ideal":"Phishing is a cyber attack to steal sensitive information"}
],
"Cloud Engineer":[
{"question":"What is cloud computing?",
"ideal":"Cloud computing provides computing services over the internet"},
{"question":"What is IaaS?",
"ideal":"Infrastructure as a Service provides virtual computing resources"},
{"question":"What is SaaS?",
"ideal":"Software as a Service delivers applications over the internet"}
]
}
def evaluate_answer(answer, ideal):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([answer, ideal])
    similarity = cosine_similarity(vectors)[0][1]
    ideal_words = set(ideal.lower().split())
    answer_words = set(answer.lower().split())
    keyword_match = len(ideal_words & answer_words) / len(ideal_words)
    final_score = max(similarity, keyword_match)
    return round(final_score * 10,2)
if st.session_state.role is None:
    st.subheader("Select Job Role")
    role = st.selectbox(
        "Choose Role",
        list(role_questions.keys())
    )
    if st.button("Start Interview"):
        st.session_state.role = role
        st.session_state.questions = basic_questions + role_questions[role]
        st.session_state.q_index = 0
        st.session_state.scores = []
        st.rerun()
else:
    questions = st.session_state.questions
    index = st.session_state.q_index
    if index < len(questions):
        q = questions[index]
        st.subheader(f"Question {index+1}")
        st.write(q["question"])
        if st.button("🔊 Voice Question"):
            speak(q["question"])
        answer = st.text_area("Your Answer")
        if st.button("Submit Answer"):
            score = evaluate_answer(answer, q["ideal"])
            st.session_state.scores.append(score)
            st.session_state.submitted = True
            st.subheader("AI Feedback")
            if score >= 8:
                st.success(f"Excellent Answer | Score: {score}/10")
            elif score >= 5:
                st.warning(f"Good Answer | Score: {score}/10")
            else:
                st.error(f"Needs Improvement | Score: {score}/10")
                st.info("Suggested Answer")
                st.write(q["ideal"])
        if st.session_state.submitted:
            if st.button("Next Question"):
                st.session_state.q_index += 1
                st.session_state.submitted = False
                st.rerun()
    else:
        st.header("🎉 Interview Completed")
        avg = sum(st.session_state.scores)/len(st.session_state.scores)
        st.write("Average Score:", round(avg,2),"/10")
        if avg > 7:
            st.success("Excellent Performance")
        elif avg > 5:
            st.warning("Good Performance but needs improvement")
        else:
            st.error("Practice more")
        if st.button("Restart Interview"):
            st.session_state.role = None
            st.session_state.q_index = 0
            st.session_state.scores = []
            st.session_state.submitted = False
            st.rerun()