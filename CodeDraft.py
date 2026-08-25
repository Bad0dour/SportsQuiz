usr_contact = input("Do you enjoy Physical Contact? [y/n] : ")
usr_inside = input("Do you prefer Indoors? [y/n] : ")
if usr_contact == 'y' and usr_inside == 'y': #Contact, Inside
    print("Your sport is Basketball!")
elif usr_contact == 'y' and usr_inside == 'n':  #Contact, outside
    usr_hands = input("Do you enjoy using your Hands? [y/n] : ")
    if usr_hands == 'n': #Contact, outside, noHands
        print("Your Sport is Soccer!")
    else:             #Contact, outside, Hands
        usr_breaks = input("Do you enjoy Frequent Breaks? [y/n] : ")
        if usr_breaks == 'y': #Contact, outside, Hands, Breaks
            print("Your sport is AFL!")
        elif usr_breaks == 'n':  #Contact, outside, Hands, noBreaks
            print("Your sport is Rugby!")
elif usr_contact == 'n' and usr_inside == 'y':  # noContact, Inside
    usr_team = input("Do you enjoy working in Teams? [y/n] : ")
    if usr_team == 'y': # noContact, Inside, Team
        print("Your sport is Volleyball!")
    elif usr_team == 'n': # noContact, Inside, noTeam
        print("Your sport is Swimming!")
elif usr_contact == 'n' and usr_inside == 'n':  # noContact, outside
    usr_hands = input("Do you enjoy using your Hands? [y/n] : ")
    if usr_hands == 'n': # noContact, outside, noHands
        print("Your sport is Track!")
    elif usr_hands == 'y': # noContact, outside, Hands
        usr_slow = input("Do you enjoy a slower pace? [y/n] : ")
        if usr_slow == 'y':  # noContact, outside, Hands, slow
            print("Your sport is Golf!")
        elif usr_slow == 'n': # noContact, outside, Hands, fast
            usr_team = input("Do you enjoy working in Teams? [y/n] : ")
            if usr_team == 'y': # noContact, outside, Hands, fast, team
                print("Your sport is Cricket!")
            elif usr_team == 'n': # noContact, outside, Hands, fast, noteam
                print("Your sport is Tennis!")
