#### WORD WALL ####
# This is a terminal application that accepts user words, meanings and
#   categories. It displays these words and meanings, along with other
#   statistics about the data. Oh, and it includes a guessing game to
#   quiz the user on the words within the program!

import os
from time import sleep
import pickle
import statistics

### FUNCTIONS ###
def load_words():
    # This function tries to open word data. If it doesn't exist,
    #  it returns the preset word list.
    try:
        print("Loading WORD WALL data.")
        file_object = open('words.pydata', 'rb')
        words = pickle.load(file_object)
        file_object.close()
        print("Loading complete.")
        sleep(1)
        return words
    except:
        print("Failed to load word list data.")
        sleep(1)
        return words_known
def save_and_quit():
    # Saves the words_known dictionary and prints a confirmation, or error
    show_banner()
    try:
        file_object = open('words.pydata', 'wb')
        pickle.dump(words_known, file_object)
        file_object.close()
        
        print("\nWORD WALL will remember...")
    except Exception as e:
        print(e)
        print("\nWORD WALL couldn't save its words.")
def show_banner():
    # Clears screen then displays a simple title banner
    os.system('cls')
    print("""
    #############################
    ######### WORD WALL #########
    #############################
""")
def show_options(options_shown_list):
    # Prints the requested options from the choice_options dictionary
    for key, value in choice_options.items():
        if key in options_shown_list or len(options_shown_list) == 0:
            print("[%s] - %s"  % (key, value[0]))
def view_words():
    active_scene = 'view words'
    while active_scene == 'view words':
        show_banner()
        print(active_scene.title(),'\n')
        
        # Prints the category, then each word and meaning in that category.
        for category, words in words_known.items():
            print("Category: %s" % category.title())
            for word, defenition in words.items():
                print("%s: \n%s\n" % (word.title(), defenition.capitalize()))
        
        # Show quit option and handle exceptions
        show_options(['q'])
        choice = input("\nPress 'q' to return to main menu.\n")
        if choice == 'q':
            active_scene = 'back'
        else:
            print("Sorry, I don't recognise that input")
def create_new_word():
    active_scene = 'create/modify word'
    while active_scene == 'create/modify word':
        show_banner()
        print(active_scene.title(),'\n')
        show_options(['q'])
        
        # Get the requested new word
        new_word = input(
                "What word would you like to add or modify in WORD WALL?\n")
        
        # Handle quit request
        if new_word == 'q':
            active_scene = 'back'
        
        # Active if requested word exists in any category within words_known
        elif any(new_word in words for category, words in words_known.items()):
                show_banner()
                print("WORD WALL already knows that word.")
                print("Would you like to edit the meaning of '%s'?"
                                                            % new_word.title())
                
                # Confirm user wants to edit the meaning of the word
                choice = input("[y] or [n]\n")
                if choice == 'y':
                    show_banner()
                    
                    # Get new meaning
                    new_meaning = input("Please enter a new meaning for '%s'\n"
                                                            % new_word.title())
                    
                    # Locate word and replace meaning
                    for category, words in words_known.items():
                        if new_word in words:
                            words_known[category][new_word] = new_meaning
                    
                    # Clean screen and show confirmation
                    show_banner()
                    print("Thank you, the meaning for '%s' has been updated."
                                                       % new_word.title())
                    sleep(1)
                
                # Exit meaning change if input != 'y'
                print("Returning to previous page.")
                sleep(2)
        else:
            show_banner()
            print(active_scene.title(),'\n')
            
            # Get a meaning for the new word
            new_meaning = input("Please type a definition for '%s'\n"
                                                        % new_word.title())
            
            # Enter the new word and meaning in the 'un-categorised' category
            words_known['un-categorised'][new_word.lower()] = 
                                                            new_meaning.lower()
            
            # Print confirmation
            print("Thank you, '%s' has been added to WORD WALL."
                                                        % new_word.title())
            sleep(2)
def modify_word():
    # Setup scene title, banner and options
    active_scene = 'modify word'
    while active_scene == 'modify word':
        show_banner()
        print(active_scene.title(),'\n')
        show_options('q')
        
        # Get the word whose spelling needs to change
        old_key = input("Which words spelling would you like to modify?\n")
        
        if old_key != 'q':
            # Fresh screen with banner, scene title and options
            show_banner()
            print(active_scene.title(),'\n')
            show_options('q')
            
            # Get the new spelling of the word.
            new_key = input("What would you like the new spelling to be?\n")
            
            # Find the location of the word
            for category, words in words_known.items():
                if old_key in words:
                    
                    # Create new key and assign it the value of old spelling.
                    words_known[category][new_key] = 
                                                words_known[category][old_key]
                    
                    # Delete the old spelling key-value pair
                    del words_known[category][old_key]
            
            # Print confirmation of spelling change.
            print("The spelling has been changed from '%s' to '%s'."
                                                     % (old_key, new_key))
            sleep(3)
        
        # Handle quit request.
        else:
            active_scene = 'back'
def categorise_words():
    active_scene = 'categorise word'
    while active_scene == 'categorise word':
        # Set up a list containing all words in WORD WALL
        all_words = []
        for key, value in recursive_items(words_known):
            all_words.append(key)
        # Set up a list containing all categories
        all_cat = [cat for cat in words_known]
        
        # Show words known and ask which one they want to (re)categorise
        show_banner()
        print(active_scene.title(),'\n')
        show_options('q')
        print("Here are all the words I know:")
        print(', '.join(all_words).title())
        word_choice = input("\nWhich word would you like to (re)categorise?\n")
        
        if word_choice == 'q':
            active_scene = 'back'
        elif word_choice in all_words:
            # Display the chosen word's current category and get new category
            show_banner()
            print(active_scene.title(),'\n')
            show_options('q')
            
            # Find the words current category
            for category in all_cat:
                if word_choice in words_known[category]:
                    word_choice_cat = category
            
            # Print which category the word is in, and a list of all categories
            print("%s is currently in the '%s' category."
                        % (word_choice.title(), str(word_choice_cat)))
            print("The current categories are:")
            print(', '.join(all_cat).title())
            
            # Get the new category
            print("Choose an existing category or create your own.")
            category_choice = input()
            
            # Move the chosen word from one category to another
            meaning_holder = words_known[word_choice_cat].pop(word_choice)
            if category_choice in all_cat:
                words_known[category_choice][word_choice] = meaning_holder
            else:
                words_known.update({category_choice: {}})
                words_known[category_choice][word_choice] = meaning_holder
            
            # Print a confirmation
            print("'%s' has been successfully re-categorised under '%s'"
                        % (word_choice.title(), category_choice.title()))
        else:
            print("Sorry, WORD WALL doesn't know that word.")
def guess_the_word():
    import random
    
    # Set up a list of all words and picks a random word form that list.
    all_words = []
    for key, value in recursive_items(words_known):
        all_words.append((key, value))
    chosen_word = random.choice(all_words)
    
    # Banner and title setup
    active_scene = 'guess the word'
    while active_scene == 'guess the word':
        show_banner()
        show_options('q')
        print('\n', active_scene.title(), '\n')
        
        # Print the description and allow guessing
        print("The description for the word is:\n%s" 
                                                % chosen_word[1].capitalize())
        guess = input("\nGuess the word!\n")
        
        # Quit to main menu if guess == 'q'
        if guess == 'q':
            active_scene = 'back'
        
        # Show if guess is correct or incorrect
        elif guess == chosen_word[0]:
            print("Well done, that is correct!")
            sleep(2)
            active_scene = 'back'
        else:
            print("That is incorrect. Try again.")
            sleep(1)
def view_stats():
    # Set up a list of all words.
    all_words = []
    all_meanings = []
    for key, value in recursive_items(words_known):
        all_words.append(key)
        all_meanings.append(value)
    
    # Banner and options
    active_scene = 'stats'
    while active_scene == 'stats':
        show_banner()
        show_options('q')
        
        # Print basic stats for words
        print("\nThere are %d words in WORD WALL" % len(all_words))
        total_char_len = sum(len(string) for string in all_words)
        ave_char_len = total_char_len / len(all_words)
        print("The average length of a word is %d characters." % ave_char_len)
        print("All words combined have a total of %d characters." 
                                                    % total_char_len)
        
        # Recalculate and print basic stats for meanings
        total_char_len = sum(len(string) for string in all_meanings)
        ave_char_len = total_char_len / len(all_meanings)
        print("\nThe average length of a meaning is %d characters." 
                                                    % ave_char_len)
        print("All meanings combined have a total of %d characters." 
                                                    % total_char_len)
        
        # Quit to main menu
        choice = input("\nEnter 'q' to return to main menu.\n")
        if choice == 'q':
            active_scene = 'back'
        
        # Catch inputs that are != 'q'
        else:
            print("No, I said 'q', silly.")
            sleep(1)
def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield (key, value)

### DICTIONARIES ###
choice_options = {
        '1':['View all words and corresponding meanings.', view_words],
        '2':['Enter a word or modify a meaning.', create_new_word],
        '3':['Modify the spelling of a word.', modify_word],
        '4':['Categorise words.', categorise_words],
        '5':["'Guess the Word' game.", guess_the_word]''
        '6':['View statistics.', view_stats],
        'q':'Go back a scene (or quit if on main menu)'}
words_known = {'un-categorised':{
    'bee':
"""a stinging winged insect which collects nectar and pollen, produces wax and
honey, and lives in large communities. Also called honeybee.""",
    'elephant':
"""a very large plant-eating mammal with a prehensile trunk, long curved ivory
tusks, and large ears, native to Africa and southern Asia. It is the largest
living land animal.""",
    'wolf':
"""a wild carnivorous mammal which is the largest member of the dog family,
living and hunting in packs."""}}

### MAIN CODE ###

# Load word dictionary
words_known = load_words()

# Setup active scene, banner and options
active_scene = 'main menu'
while active_scene != 'quit':
    show_banner()
    print(active_scene.title(),'\n')
    show_options([])
    
    # Get user option choice
    choice = input("\nPlease make a selection.\n")
    try:
        # Quit program on request by changing active_scene
        if choice == 'q':
            active_scene = 'quit'
        
        # Run the function of the associated option
        else:
            choice_options[choice][1]()
    
    # Handle exceptions
    except Exception as e:
        print(e)
        print("Sorry, I don't recognise that input")
        sleep(3)

save_and_quit()
