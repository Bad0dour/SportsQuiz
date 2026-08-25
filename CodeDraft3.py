# Imports
import pandas as pd
import gspread
import streamlit as st
import time
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier

st.set_page_config(
    page_title="Sports Quiz",
    page_icon=":material/sports_soccer:",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #f4f6f1;
        color: #17252a;
    }

    h1 {
        color: #12343b;
        text-align: center;
        font-size: 42px;
        font-weight: 800;
    }

    .subtitle {
        text-align: center;
        color: #425457;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 28px;
    }

    div[data-testid="stRadio"] {
        background: #ffffff;
        padding: 16px 18px;
        border-radius: 8px;
        border: 1px solid #c8d1cc;
        margin-bottom: 12px;
        color: #17252a;
    }

    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] p,
    div[data-testid="stRadio"] span {
        color: #17252a !important;
        opacity: 1 !important;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background-color: #2f6f73;
        color: white;
        font-weight: 700;
        border: none;
        padding: 12px;
    }

    .stButton > button:hover {
        background-color: #24575a;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# DEBUG prints extra information about how each sport is scored.
#~~~~~~~~~~~~#
DEBUG = False
#~~~~~~~~~~~~#

sports: list[str] = [
    "Basketball",
    "Soccer",
    "Volleyball",
    "AFL",
    "Rugby",
    "Golf",
    "Track",
    "Tennis",
    "Cricket",
    "Swimming",
    "Badminton",
    "Boxing",
    "Table Tennis",
]

# Each question has two options:
# 1 means the user prefers the option in `questions`.
# 0 means the user prefers the opposite option in `anti_questions`.
questions: list[str] = [
    "Being indoors",
    "Being on a team",
    "Physical contact",
    "Using your hands",
    "Frequent breaks",
    "A slower pace",
    "Being in water",
    "Running around",
]
anti_questions: list[str] = [
    "Being outdoors",
    "Being alone",
    "No physical contact",
    "Not using your hands",
    "Long, stamina driven games",
    "A faster pace",
    "Not being in water",
    "Not running around",
]

# Each sport has a unique list of 1s and 0s matching the questions above.
data: list[list[int]] = [
    [1, 1, 1, 1, 1, 0, 0, 1],  # Basketball
    [0, 1, 1, 0, 0, 0, 0, 1],  # Soccer
    [1, 1, 0, 1, 1, 0, 0, 1],  # Volleyball
    [0, 1, 1, 1, 1, 0, 0, 1],  # AFL
    [0, 1, 1, 1, 0, 0, 0, 1],  # Rugby
    [0, 0, 0, 1, 1, 1, 0, 0],  # Golf
    [0, 0, 0, 0, 0, 0, 0, 1],  # Track
    [0, 0, 0, 1, 1, 0, 0, 1],  # Tennis
    [0, 1, 0, 1, 1, 0, 0, 1],  # Cricket
    [1, 0, 0, 1, 0, 0, 1, 0],  # Swimming
    [1, 0, 0, 1, 0, 0, 0, 1],  # Badminton
    [1, 0, 1, 1, 1, 0, 0, 0],  # Boxing
    [1, 0, 0, 1, 1, 0, 0, 0],  # Table Tennis
]

def ask(question1: str, question2: str, key: str) -> int:
    choice = st.radio(
        "What do you prefer?",
        [question1, question2],
        key=key,
    )

    if choice == question1:
        return 1
    return 0

gc = gspread.service_account(filename="BoringStuff/service_account.json")
sheet = gc.open_by_key("1zBDU1tVMppV0JTV2dWlSguEClaEHiiMLtoYqW_7JC_Y").sheet1

# Dynamics begin Below V
# Dynamics begin Below V

st.title("Sports Quiz")
st.markdown(
    '<p class="subtitle">Answer the questions below to find the sport that suits you best.</p>',
    unsafe_allow_html=True,
)

# Train the decision tree once using the sport data.
df = pd.DataFrame(data, columns=questions, index=sports)
X = df[questions]
Y = df.index

dtree = DecisionTreeClassifier(random_state=0)
dtree = dtree.fit(X, Y)


def save_result(usr_pref: list[int], result: str) -> None:
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        *usr_pref,
        result,
    ])


def get_highscore_list(usr_pref: list[int]) -> list[tuple[str, list[int], int]]:
    scores: list[tuple[str, list[int], int]] = []

    for sport_name, sport_data in zip(sports, data):
        current_score = 0

        for user_answer, sport_answer in zip(usr_pref, sport_data):
            if user_answer == sport_answer:
                current_score += 1

        scores.append((sport_name, sport_data, current_score))

    highscore = max(score for _, _, score in scores)
    return [sport for sport in scores if sport[2] == highscore]


def finish_quiz(result: str) -> None:
    if not st.session_state.saved:
        save_result(st.session_state.usr_pref, result)
        st.session_state.saved = True

    st.success(f"According to the data, you most align with: {result}!")


if "started" not in st.session_state:
    st.session_state.started = False
if "hsl" not in st.session_state:
    st.session_state.hsl = []
if "usr_pref" not in st.session_state:
    st.session_state.usr_pref = []
if "saved" not in st.session_state:
    st.session_state.saved = False


if not st.session_state.started:
    usr_pref: list[int] = []
    
    left_col, right_col = st.columns(2)
    
    for i in range(len(questions)):
        if i < 4:
            with left_col:
                answer = ask(questions[i], anti_questions[i], f"question_{i}")
        else:
            with right_col:
                answer = ask(questions[i], anti_questions[i], f"question_{i}")
    
        usr_pref.append(answer)

    if st.button("Submit Quiz"):
        st.session_state.usr_pref = usr_pref
        st.session_state.saved = False
        st.session_state.started = True

        if usr_pref in data:
            usr_df = pd.DataFrame([usr_pref], columns=questions)
            result = str(dtree.predict(usr_df)[0])
            st.session_state.hsl = [(result, [], 0)]
        else:
            st.session_state.hsl = get_highscore_list(usr_pref)

        st.rerun()


else:
    hsl: list[tuple[str, list[int], int]] = st.session_state.hsl
    usr_pref = st.session_state.usr_pref

    if len(hsl) == 1:
        finish_quiz(hsl[0][0])

    else:
        st.write("There is a tie. Answer this follow-up question.")

        _, s1_data, _ = hsl[0]
        _, s2_data, _ = hsl[1]

        diffs: list[int] = []
        s1_agreement_index: int | None = None
        s2_agreement_index: int | None = None

        for i in range(len(questions)):
            if s1_data[i] != s2_data[i]:
                diffs.append(i)

        for i in diffs:
            if s1_data[i] == usr_pref[i]:
                s1_agreement_index = i
                break

        for i in diffs:
            if s2_data[i] == usr_pref[i]:
                s2_agreement_index = i
                break

        if s1_agreement_index is None or s2_agreement_index is None:
            result = hsl[0][0]
            finish_quiz(result)

        else:
            option1 = questions[s1_agreement_index] if usr_pref[s1_agreement_index] == 1 else anti_questions[s1_agreement_index]
            option2 = questions[s2_agreement_index] if usr_pref[s2_agreement_index] == 1 else anti_questions[s2_agreement_index]

            choice = st.radio(
                "What do you prefer?",
                [option1, option2],
                key=f"followup_{len(hsl)}",
            )

            if st.button("Submit Follow-Up"):
                if choice == option1:
                    chosen_fav_index = s1_agreement_index
                else:
                    chosen_fav_index = s2_agreement_index

                new_hsl: list[tuple[str, list[int], int]] = []

                for sport in hsl:
                    if sport[1][chosen_fav_index] == usr_pref[chosen_fav_index]:
                        new_hsl.append(sport)

                st.session_state.hsl = new_hsl
                st.rerun()

    if st.button("Restart Quiz"):
        st.session_state.started = False
        st.session_state.hsl = []
        st.session_state.usr_pref = []
        st.session_state.saved = False
        st.rerun()