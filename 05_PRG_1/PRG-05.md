# Conditions
Very often, you will want to run a piece of code only when certain conditions are met. For example, you might want to write something to an error log only if the reply you receive from a server contains an error.

Python makes use of the if, elif, and else statements.

## Key-terms
N/A

## Opdracht
**Exercise 1**
- Create a new script.
- Use the input() function to ask the user of your script for their name. If the name they input is your name, print a personalized welcome message. If not, print a different personalized message.

**Exercise 2**
- Create a new script.
- Ask the user of your script for a number. Give them a response based on whether the number is higher than, lower than, or equal to 100.
- Make the game repeat until the user inputs 100.

### Gebruikte bronnen
ChatGPT

### Ervaren problemen
None

### Resultaat
**Exercise 1**

Look at PRG-05-01.py

**Exercise 2**

Look at PRG-05-02.py

***Explanation of "while True" loop***

The while True: loop creates an infinite loop that continues until the user picks the secret number 100. Make sure that the follow up code lines fall properly under the "while True" loop, so it will know that the code lines belong under the loop.

***Explanation of why not "while False" loop***

The reason for using while True: instead of while False: is that while False: would immediately evaluate to False, and the loop would never run. The loop body would not be entered, and there would be no opportunity to trigger anything.

***Explanation of "break"***

The break statement is used to exit the loop and end the program.



