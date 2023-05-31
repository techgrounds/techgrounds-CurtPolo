# Functions
A function is a block of code that only runs when it is called. Functions are recognizable by the brackets () next to the function name. These brackets serve as a place to input data into a function.
Functions return data as a result.

Besides the built-in functions, you can also write custom functions, or import functions from a library or package.


## Key-terms
[Schrijf hier een lijst met belangrijke termen met eventueel een korte uitleg.]

## Opdracht
**Exercise 1**
- Create a new script.
- Import the random package.
- Print 5 random integers with a value between 0 and 100.

**Exercise 2**
- Create a new script.
- Write a custom function myfunction() that prints “Hello, world!” to the terminal. Call myfunction.
- Rewrite your function so that it takes a string as an argument. Then, it should print “Hello, <string>!”.

**Exercise 3**
- Create a new script.
- Copy the code below into your script.

def avg():

	# write your code here

#you are not allowed to edit any code below here

x = 128

y = 255

z = avg(x,y)

print("The average of",x,"and",y,"is",z)

- Write the custom function avg() so that it returns the average of the given parameters. You are not allowed to edit any code below the second comment.

### Gebruikte bronnen
ChatGPT

### Ervaren problemen
None

### Resultaat
**Exercise 1**

Look at PRG-06-01.py

***Explanation of "Random"***

By including this statement at the beginning of your Python script or in the interactive Python interpreter, you make the random module available for use in your code. The random module provides various functions for generating random numbers, selecting random elements, shuffling sequences, and more.

***Explanation of "random.randint"***

Once you have imported the random module, you can access its functions and attributes using dot notation. For example, to generate a random integer between a given range, you can use the randint() function from the random module

***Explanation of "_"***

Here, the loop variable _ is assigned the values from range(5) on each iteration, but since it is not used within the loop body, the choice of i, b or _ does not impact the behavior of the code.

Using _ as a convention can help convey to other programmers reading the code that the loop variable is intentionally being ignored and its value is not relevant for that specific loop.

**Exercise 2**

Look at PRG-06-02.py

***Explanation of "def"***

To create your own custom function in Python, you can use the def keyword followed by the function name and a set of parentheses.

def function_name(parameters):

    # Function body
    # Code to be executed
    # Optional return statement

for example

def greet(name):

    print("Hello, " + name + "! How are you?")

#Calling the function

greet("Alice")

**Exercise 3**

Look at PRG-06-03.py

***Explanation of "return"***

The return statement, returns the calculated average value (x + y) / 2. The calculated result is then stored in the variable z when calling the function avg(x, y).



