import random, sys

card_names = {
    1 : "J",
    2 : "Q",
    3 : "K"
}

# probability of the bot betting at each infoset
bot_strategy = {
    "1" : 2/9,
    "2" : 0,
    "3" : 2/3,
    "1p" : 1/3,
    "1b" : 0,
    "2p" : 0,
    "2b" : 1/3,
    "3p" : 1,
    "3b" : 1,
    "1pb" : 0,
    "2pb" : 5/9,
    "3pb" : 1,
}

rng = random.Random()

cards = [1, 2, 3]

def sample_action(p_b):
    """Samples an action, returns 'b' with probability p_b, else 'p'"""
    return 'b' if rng.random() < p_b else 'p'

def is_terminal(history):
    actions = history[1:]
    return len(actions) > 1 and (actions[-1] == 'p' or actions[-2:] == 'bb')

def showdown(history, user_is_p1):
    """history: first char is the bot's card ('1'/'2'/'3'), then actions 'p'/'b'
    user_is_p1: True if user acted first this hand, else False
    Uses globals: user_stack, bot_stack, pot, user_card, bot_card, card_names
    """
    global user_stack, bot_stack, pot, user_card, bot_card
    actions  = history[1:] # drop leading bot card

    if actions == "pp":
        # check-check -> showdown for pot = 2
        print(f"Showdown! Your card: {card_names[user_card]} | Bot card: {card_names[bot_card]}")
        if user_card > bot_card:
            user_stack += pot
            print("You win +1.")
        else:
            bot_stack += pot
            print("You lose -1.")
    elif actions[-2:] == "bb":
        # bet-call -> showdown for pot = 4
        print(f"Showdown! Your card: {card_names[user_card]} | Bot card: {card_names[bot_card]}")
        if user_card > bot_card:
            user_stack += pot
            print("You win +2.")
        else:
            bot_stack += pot
            print("You lose -2.")
    
    # Fold cases (no reveal)
    elif actions == "bp":
        if user_is_p1:
            # user bet, bot folded -> user takes pot
            user_stack += pot
            print("Bot folds. You take the pot. (Cards not revealed)")
            print("You win +1.")
        else:
            # bot bet, user folded -> bot takes pot
            bot_stack += pot
            print("You fold. Bot takes the pot. (Cards not revealed)")
            print("You lose -1")
    
    elif actions == "pbp":
        if user_is_p1:
            #bot bet, user folded -> bot takes pot
            bot_stack += pot
            print("You fold. Bot takes the pot. (Cards not revealed)")
            print("You lose -1.")
        else:
            # user bet, bot folded -> user takes pot
            user_stack += pot
            print("Bot folds. You take the pot. (Cards not revealed)")
            print("You win +1.")
    else:
        print("Something went wrong")
        return
    
    # Check if anyone is broke
    if user_stack == 0:
        print("You are broke, the bot has taken all your money.")
    elif bot_stack == 0:
        print("You win! the bot is broke.")
    
    print(f"Stacks | You: {user_stack}  Bot: {bot_stack} \n")

def pause_between_hands():
    s = input("Press Enter to deal the next hand (or 'q' to quit): ").strip().lower()
    if s == 'q':
        print("Goodbye!")
        sys.exit(0)

user_stack = bot_stack = 0

while True:
    s = input("Buy-in chips (>=2): ").strip()
    try:
        buy_in = int(s)
        if buy_in >= 2:
            user_stack = bot_stack = buy_in
            break
        print("Enter a number >= 2.")
    except ValueError:
        print("Please enter a valid integer.")

hand = 0
while user_stack >= 1 and bot_stack >=1:
    history = ""
    rng.shuffle(cards)
    user_card = cards[0]
    bot_card = cards[1]
    pot = 2
    user_stack -= 1
    bot_stack -= 1
    history += str(bot_card)

    if hand % 2 == 0: # User is player 1
        print("You are player 1.")
        print(f"Your card is: {card_names[user_card]}")
        user_action = ""
        while True:
            user_action = input("Your move (b = bet, p = check): ").strip().lower()
            if user_action in ("b", "p"):
                if user_action == "b" and user_stack < 1:
                    print("You don't have a chip to bet/call; forced check/fold")
                    user_action = "p"
                history += user_action
                if user_action == "b":
                    pot+=1
                    user_stack-=1
                break
            else:
                print("Please type 'b' or 'p'")

        bot_action = sample_action(bot_strategy[history])
        if bot_action == "b" and bot_stack < 1:
            bot_action = "p"
        if bot_action == "b":
            pot+=1
            bot_stack-=1
        history += bot_action

        match history[1:]:
            case "bb":
                print("Bot calls.")
            case "pp":
                print("Bot checks.")
            case "pb":
                print("Bot bets.")

        if is_terminal(history):
            showdown(history, 1)
            if user_stack == 0 or bot_stack == 0:
                break
            pause_between_hands()
            hand+=1
            continue

        while True:
            user_action = input("Your response (b = call, p = fold): ").strip().lower()
            if user_action in ("b", "p"):
                if user_action == "b" and user_stack < 1:
                    print("You don't have a chip to bet/call; forced check/fold")
                    user_action = "p"
                history += user_action
                if user_action == "b":
                    pot+=1
                    user_stack-=1
                break
            else:
                print("Please type 'b' or 'p'")
        
        if is_terminal(history):
            showdown(history, 1)
            if user_stack == 0 or bot_stack == 0:
                break
            pause_between_hands()
            hand+=1
            continue
    else:
        print("You are player 2.")
        print(f"Your card is: {card_names[user_card]}")

        bot_action = sample_action(bot_strategy[history])
        if bot_action == "b" and bot_stack < 1:
            bot_action = "p"
        if bot_action == "b":
            pot+=1
            bot_stack-=1
        history += bot_action

        match bot_action:
            case "b":
                print("Bot bets.")
            case "p":
                print("Bot checks.")
        
        user_action = ""
        while True:
            user_action = input("Your move (b = bet, p = check): ").strip().lower()
            if user_action in ("b", "p"):
                if user_action == "b" and user_stack < 1:
                    print("You don't have a chip to bet/call; forced check/fold")
                    user_action = "p"
                history += user_action
                if user_action == "b":
                    pot+=1
                    user_stack-=1
                break
            else:
                print("Please type 'b' or 'p'")
        
        if is_terminal(history):
            showdown(history, 0)
            if user_stack == 0 or bot_stack == 0:
                break
            pause_between_hands()
            hand+=1
            continue

        bot_action = sample_action(bot_strategy[history])
        if bot_action == "b" and bot_stack < 1:
            bot_action = "p"
        if bot_action == "b":
            pot+=1
            bot_stack-=1
        history += bot_action

        match bot_action:
            case "b":
                print("Bot calls.")
        
        if is_terminal(history):
            showdown(history, 0)
            if user_stack == 0 or bot_stack == 0:
                break
            pause_between_hands()
            hand+=1
            continue
    
    # Check if anyone is broke
    if user_stack == 0:
        print("You are broke, the bot has taken all your money.")
        print(f"Stacks | You: {user_stack}  Bot: {bot_stack} \n")
        break
    elif bot_stack == 0:
        print("You win! the bot is broke.")
        print(f"Stacks | You: {user_stack}  Bot: {bot_stack} \n")
        break