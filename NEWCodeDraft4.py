import csv, time
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

#~~~~~~~~~~~~#
DEBUG = False
FILE_PATH = "sport_data.csv"
#~~~~~~~~~~~~#

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)

def ask(question1: str, question2: str) -> int:
    # Keep asking until the user enters a valid answer.
    while True:
        answer = input(f"Do you prefer {question1} (1) or {question2} (2)? [1/2] : ")

        if answer == "1":
            return 1
        elif answer == "2":    # User's inputs of '1' or '2' get converted into 1's and 0's
            return 0

        print("   !!! Please enter '1' or '2' !!!")
      
def reveal_result(result: str) -> None:
    # Print the final sport result with a short delay for suspense.
    print("\nAccording to the data you most align with...")

    for dot in [".", "..", "..."]:
        time.sleep(0.75)
        print(dot)

    print(f"\n{result}!\n")
    
# Lists of the questions worded in a readable way to be used when asking the user questions. (not used anywhere else)
# Each question has two options:
questions: list[str] = [
    "being indoors",
    "playing on a team",
    "physical contact",
    "using your hands",
    "frequent breaks",
    "a slower pace",
    "being in water",
    "running around",
]        # 1 means the user prefers the option in `questions`.
anti_questions: list[str] = [
    "being outdoors",
    "playing solo",
    "no physical contact",
    "not using your hands",
    "long, stamina driven games",
    "a faster pace",
    "not being in water",
    "not running around",
]   # 0 means the user prefers the opposite option in `anti_questions`.

# List of Nicknames for each column/question for script to use for headers
df_cols: list[str] = [
    "Indoors",
    "Team",
    "Contact",
    "Hands",
    "Breaks",
    "Slow",
    "Water",
    "Running",
    "SPORT",
]

# Nicknames for each column/question for script to use for headers and calculations EXCLUDING SPORT
features: list[str] = [
    "Indoors",
    "Team",
    "Contact",
    "Hands",
    "Breaks",
    "Slow",
    "Water",
    "Running",
]

# Dictionary of Sports and a number associated with them because the DecisionTree can't do strings.
sports_dict: dict[str, int] = {
    "Basketball":0,
    "Soccer":1,
    "Volleyball":2,
    "AFL":3,
    "Rugby":4,
    "Golf":5,
    "Track":6,
    "Tennis":7,
    "Cricket":8,
    "Swimming":9,
    "Badminton":10,
    "Boxing":11,
    "Table Tennis":12,
} 
sports_data: list[int] = []


# Create DataFrame from the data
data_df = pd.read_csv(FILE_PATH, names=df_cols)

if DEBUG:
    print(f"""Data DataFrame:\n{data_df}""")
    print(f"""data_df[features]:\n{data_df[features]}""")
    print(f"""data_df['SPORT']:\n{data_df['SPORT']}""")

# Train a decision tree using the sport data.
# X is the question data, and Y is the sports associated with the question data.
X = data_df[features]
y = data_df['SPORT']
dtree = DecisionTreeClassifier(random_state=0)
dtree = dtree.fit(X, y)

print("\n~~~~~~~ Let's Find Out What Sport Suits You Best! ~~~~~~~~\n")

# Ask the user each question and store their answers as 1s and 0s into a list.
usr_pref = [ask(questions[i], anti_questions[i]) for i in range(len(questions))]

if DEBUG:
    print(f"usr_pref: {usr_pref}")

reveal_result(dtree.predict([usr_pref])[0])