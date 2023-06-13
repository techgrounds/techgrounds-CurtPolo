# Tuesday June 13, 2023

## Daily Report
I am pushing to have one errorless working code for today and figure out the best way to test it.
## Obstacles
Figuring out what is the best way to test my application without costs.
## Solutions
I found out I needed to install pytest in my test folder and create a 'pytest.ini' file in my root directory and configure it to be able to instructs pytest to look for test files that start with "test_" and have the ".py" extension.
## Learnings
I learned how to create the pytest.ini file, how to configure it for this specific use and the best practice of using the test folder to test changes in my code before adapting it to my main code.