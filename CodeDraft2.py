# Imports
import pandas as pd
import time
from sklearn.tree import DecisionTreeClassifier


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
    "being indoors",
    "being on a team",
    "physical contact",
    "using your hands",
    "frequent breaks",
    "a slower pace",
    "being in water",
    "running around",
]
anti_questions: list[str] = [
    "being outdoors",
    "being alone",
    "no physical contact",
    "not using your hands",
    "long, stamina driven games",
    "a faster pace",
    "not being in water",
    "not running around",
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

# Define Functons
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

# Dynamics begin Below V

print("\n~~~~~~~ Let's Find Out What Sport Suits You Best! ~~~~~~~~\n")

# Ask the user each question and store their answers as 1s and 0s.
usr_pref = [ask(questions[i], anti_questions[i]) for i in range(len(questions))]

# Create a dataframe with the user's answers.
usr_df = pd.DataFrame([usr_pref], columns=questions)

# Train a decision tree using the sport data.
# X is the question data, and Y is the sport name for each row.
df = pd.DataFrame(data, columns=questions, index=sports)
X = df[questions]
Y = df.index

dtree = DecisionTreeClassifier(random_state=0)
dtree = dtree.fit(X, Y)

if DEBUG:
    print(f"User Preferences (1/0): \n {usr_pref}")

# If the user's answers exactly match one sport's data,
# use the decision tree to predict and reveal the result immediately.
if usr_pref in data:
    reveal_result(dtree.predict(usr_df)[0])

else:
    # Otherwise, score every sport by counting how many answers match. Then choose the one with highest amount of matching answers.
    scores: list[tuple[str, list[int], int]] = []

    if DEBUG:
        print("No initial Match, iterating...")

    for sport_name, sport_data in zip(sports, data):
        current_score = 0

        if DEBUG:
            print(f"\n~~~~~~~~~~{sport_name}~~~~~~~~~~")
            print(f"User Preferences (1/0): \n {usr_pref}")
            print(f"Current Sport Iteration:\n {sport_data}")
            print("Indexes: \n [0, 1, 2, 3, 4, 5, 6, 7]")

        for i, (user_answer, sport_answer) in enumerate(zip(usr_pref, sport_data)):
            if user_answer == sport_answer:
                current_score += 1

                if DEBUG:
                    print(f"Index: {i}. Match!    (usr dig: {user_answer}, sport dig: {sport_answer}, current score: {current_score})")
            else:
                if DEBUG:
                    print(f"Index: {i}. No Match! (usr dig: {user_answer}, sport dig: {sport_answer}, current score: {current_score})")

        if DEBUG:
            print(f"Sport Score: {current_score}")

        # Store the sport name, its data, and its final score.
        scores.append((sport_name, sport_data, current_score))

    # Find the highest score, then keep every sport that got that score.
    # There may be more than one, which means there is a tie between multiple sports with the same amount of matching answers.
    highscore = max(score for _, _, score in scores)
    hsl = [sport for sport in scores if sport[2] == highscore]

    if DEBUG:
        print(f"\n\nHighscore: {highscore}")
        print(f"# of Highscores: {len(hsl)}")
        print("Sports = Highscore:")

        for i in range(len(hsl)):
            print(f" - {hsl[i][0]}")

        print(f"\nHSL: {hsl}")

    first = True

    # If multiple sports are tied, ask follow-up questions until only one remains.
    while len(hsl) > 1:
        if first:
            first = False
            print("\n~~~~~~~ Nothing Yet... Let's ask some follow up questions! ~~~~~~~~")
            print("                ~~~~~~~ You have to pick one. ~~~~~~~~\n")

        # Compare the first two tied sports and find where their data is different.
        _, s1_data, _ = hsl[0]
        _, s2_data, _ = hsl[1]
        diffs: list[int] = []
        s1_agreement_index: int | None = None
        s2_agreement_index: int | None = None

        # Find all of the preferences (indexes) in which sport 1 and sport 2 differ from each other.
        for i in range(len(questions)):
            if s1_data[i] != s2_data[i]:
                diffs.append(i)

        # Pick the first difference that supports sport 1.
        for i in diffs:
            if s1_data[i] == usr_pref[i]:
                s1_agreement_index = i
                break

        # Pick the first difference that supports sport 2.
        for i in diffs:
            if s2_data[i] == usr_pref[i]:
                s2_agreement_index = i
                break

        if s1_agreement_index is None or s2_agreement_index is None:
            break

        # Ask a follow-up question using the preference that supports each tied sport.
        choice = ask(
            questions[s1_agreement_index]            # Sport 1 preference.
            if usr_pref[s1_agreement_index] == 1     # If the user's answer is 1, use the normal question text.   
            else anti_questions[s1_agreement_index], # If it is 0, use the opposite question text from anti_questions.
            
            questions[s2_agreement_index]            # Sport 2 Preference.
            if usr_pref[s2_agreement_index] == 1     # If the user's answer is 1, use the normal question text.
            else anti_questions[s2_agreement_index], # If it is 0, use the opposite question text from anti_questions.
        )

        # Determine the users answer to know which sport the user would rather choose
        if choice == 1:
            chosen_fav_index = s1_agreement_index  # Sport 1 wins
        else:
            chosen_fav_index = s2_agreement_index  # Sport 2 wins

        # Keep only the sports that match the user's chosen follow-up preference. This means we can eliminate multiple sports at once if there was a 4 way tie.
        new_hsl: list[tuple[str, list[int], int]] = []
        for sport in hsl:
            if sport[1][chosen_fav_index] == usr_pref[chosen_fav_index]:
                new_hsl.append(sport)
        hsl = new_hsl

    # Repeat until there is only one sport left
    if len(hsl) == 1:
        reveal_result(hsl[0][0])