# Loops
You can use loops when you want to run a block of code multiple times. For example, you might want to do an operation on every item in a (large) list, or you want to write an algorithm that follows the same set of instructions for multiple iterations.

## Key-terms
**While loop**

The while loop runs while a condition is true. They can run indefinitely if that condition never changes. If your code is stuck in an infinite loop, just press ctrl-c (or command-c on MacOS) to force quit the running code.

**While loop**

The for loop runs for a predetermined number of iterations. This number can be hard coded using the range() function, or dynamically assigned (using a variable, the size of a list, or the number of lines in a document). It is also possible to accidentally create an infinite for loop. You can use the same command (ctrl/cmd+c) to exit your program.

## Opdracht
**Exercise 1**
- Create a new script.
- Create a variable x and give it the value 0.
- Use a while loop to print the value of x in every iteration of the loop. After printing, the value of x should increase by 1. The loop should run as long as x is smaller than or equal to 10.

**Exercise 2**
- Create a new script.
- Copy the code below into your script.

for i in range(10):

	#do something here
- Print the value of i in the for loop. You did not manually assign a value to i. Figure out how its value is determined.
- Add a variable x with value 5 at the top of your script.
- Using the for loop, print the value of x multiplied by the value of i, for up to 50 iterations.


### Gebruikte bronnen
ChatGPT

### Ervaren problemen
None

### Resultaat
**Exercise 1**

Look at PRG-04-01.py

***Explanation of "+="***

When you write a += 1, it is equivalent to a = a + 1. The value of 1 is added to the current value of a, and the result is then assigned back to a.

**Exercise 2**

Look at PRG-04-02.py

***Explanation of "Range()"***

In Python, the range() function is used to generate a sequence of numbers. When you call range(10), it creates a sequence of numbers starting from 0 up to, but not including, 10.

**Exercise 3**

Look at PRG-04-03.py

***Explanation of "Array"***

In Python, arrays are implemented through the built-in list data type. Lists are a versatile and commonly used data structure that can hold a collection of elements. They can contain elements of different types, including integers, strings, or even other lists.

***Explanation of "for name in arr:"***

The "name" part is a variable you assigned to all the in the "arr" array. Because of the for loop it goes over every element in the array and prints them.