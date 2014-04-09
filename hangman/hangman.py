try:
    from msvcrt import getch
except: # This will fail on some platforms, use nasty hack
    getch = raw_input # bind raw_input to the getch we use everywhere else:
import os
import random

try:
    from conex import *
except:
    # On non-Windows, conex is not supported.
    # Use an empty method instead
    def empty(*args, **kwargs):
        pass

    colorc = empty
    printc = empty

# A simple noose
NOOSE = ["[ ]------^",
         " |       |",
         " |      ",
         " |     ",
         " |     ",
         " |",
         "_-_"]

# The slashed O for the head
HEAD = "\x9d"
# Victim matrix
VICTIM = [["", HEAD, HEAD, HEAD, HEAD, HEAD, HEAD],
          ["", "", " | ", "/| ", "/|\\", "/|\\", "/|\\"],
          ["", "", "", "", "", "/  ", "/ \\"]]

WORDS = None


def wordlist():
    """
        Parses word database; returns array of all words.
    """
    global WORDS
    if not WORDS:
        try:
            with open("../hangman/words.txt", "r") as words:
                WORDS = words.read().split("\n")
        except: # We're pretty screwed...
            WORDS = ["fester", "undulate", "cardinal", "krypton"]
    return WORDS


def pause(text):
    """
        Pauses the console with a message.
    """
    print text, # Leave cursor on same line
    getch() # Pause


def title(colour=FOREGROUND_WHITE | FOREGROUND_INTENSITY):
    """
        Prints the title "Hangman" - with colour.
    """
    colorc(colour)
    print "Hangman".center(80) # Center title to 80-wide console


def clear():
    """
        Readies console for redraw.
    """
    # CLEAR on *nix, CLS on win
    os.system("CLEAR" if os.name == "posix" else "CLS")
    title() # Print title


def input_s(text):
    """
        String input with intent highlighting.
    """
    colorc(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
    print text,
    colorc(FOREGROUND_YELLOW | FOREGROUND_INTENSITY)
    try:
        s = raw_input()
    except:
        s = ""
    colorc(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
    return s


def input_i(text):
    """
        Int input with intent highlighting.
    """
    return float(input_s(text))


def main():
    """
        Main game method. Starts the game loop.
    """
    words = wordlist() # Cache word array

    def new_word():
        """
            Generate a new word from the cached word list.
        """
        return random.choice(words).upper().strip()

    used = [] # Initialize array to hold all used letters
    lives = 6
    turn = 0 # Set up accumulator for the current round
    score = {} # Dictionary to hold all player points

    clear()
    players = input_i("Enter number of players:")
    if not players:
        pause("You must specify at least one player.")
        main()
        return
    phrase = new_word()
    pause("\nPress any key to begin the game!")

    while True:
        clear()

        decoded = lambda word: [char if char in used else '_' for char in word]
        wrong = [char for char in used if char not in phrase]

        def draw():
            c = FOREGROUND_INTENSITY
            if lives == 3:
                c |= FOREGROUND_YELLOW
            elif lives < 3:
                c |= FOREGROUND_RED
            else:
                c |= FOREGROUND_GREEN
            colorc(c)
            # General information
            print "[Round %d]" % (turn / players + 1)
            print ">>> Player %d\n" % ((turn % players) + 1)
            if lives:
                print "%s/6 lives left." % lives

            # Draw the noose and our poor victim
            for n in xrange(0, len(NOOSE)):
                colorc(c) # Color to the current colour
                print NOOSE[n],
                if 1 < n < 5: # Victim is 3 chars tall
                    # Should always be red
                    colorc(FOREGROUND_RED | FOREGROUND_INTENSITY)
                    print VICTIM[n - 2][6 - lives] # Print the matrix segment
                else:
                    print # Newline

            line = decoded(phrase) # Fetch the decoded string
            l = len(line)

            # Draw linked cubes containing the letters
            print "\xc9" + (("\xcd" * 3 + "\xcb") * (l - 1)) + "\xcd" * 3 + "\xbb"
            print "\xba",
            for char in line:
                # The characters should be yellow
                colorc(FOREGROUND_YELLOW | FOREGROUND_INTENSITY)
                print "%s" % char,
                colorc(c) # Restore colour for rest of boxes
                print "\xba",
            print "\n\xc8" + (("\xcd" * 3 + "\xca") * (l - 1)) + "\xcd" * 3 + "\xbc"
            colorc(FOREGROUND_GREEN | FOREGROUND_INTENSITY) # Reset to green colour

        draw()

        if len(wrong): # If the player has been wrong, inform them with what
            print "You've wrongly guessed the letter(s):", ', '.join(wrong)

        letter = input_s("\nInput a letter:").upper() # Fetch a letter
        # Sanity checks... what else?
        if len(letter) != 1:
            pause("\nYou must type one character at a time.")
            continue
        if letter in used:
            pause("You've already guessed that letter!")
            continue
        else:
            try:
                int(letter) # Attempt to parse int
                pause("What are you thinking? You can't enter numbers!")
                continue
            except: # Int parse failed, means its a letter
                used.append(letter)
            # Tests were passed.
        if letter in phrase: # Does the letter exist in our word?
            clear()
            draw()
            # Create a list containing only correct characters: check if all chars have been guessed
            if len([char for char in phrase if char in used and char.strip()]) == len(phrase):
                pause("Congratulations, you guessed the phrase '%s' in %d lives!" % (phrase, 6 - lives))
            else:
                pause("\nCorrect!") # Correct letter
                continue # But game isn't over yet
        else:
            lives -= 1
            clear()
            draw()
            if not lives: # All your base are belong to us.
                pause("You failed. The phrase was '%s'." % phrase)
            else:
                pause("\nWrong!")
                continue
        player = turn % players
        score[player] = score.get(player, 0) + (lives)
        lives = 6
        if (turn + 1) % players == 0:
            clear()
            colorc(FOREGROUND_YELLOW | FOREGROUND_INTENSITY)
            print "Played %d round(s).\n" % ((turn / players) + 1)
            print "Player #       Score"
            print "--------       -----"

            # Sort players by score
            sorted_scores = sorted(score.items(), key=lambda k: k[1], reverse=True)
            for player, points in sorted_scores:
                print "Player %d       %5d" % (player + 1, points)
                # Ask if the user wishes to play a second round.
            # If not, exit game loop.
            if 'Y' not in input_s("\nWould you like to continue? [Y/N]").upper():
                break

        turn += 1 # Increase the turn
        del used[:] # Reset the used letters
        phrase = new_word() # Create a new word to play with

    print "\nGoodbye!" # We're a friendly program.
    colorc(FOREGROUND_WHITE) # restore default gray


if __name__ == '__main__':
    main()