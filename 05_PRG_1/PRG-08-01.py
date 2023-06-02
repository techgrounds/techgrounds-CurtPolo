tech_dict = {
    "First_name": "Casper",
    "Last_name": "Vlezen",
    "Job_title": "Learning Coach",
    "Company": "Techgrounds"}

for key, value in tech_dict.items():
    print(key + " : " + value)

# 1. We start by defining the tech_dict dictionary with four key-value pairs
# 2. We use a for loop to iterate over the key-value pairs in the tech_dict dictionary.
#    The items() method is used to obtain a sequence of tuples, where each tuple contains a key-value pair.
# 3. Inside the loop, we print the key and value using the print() function.
#    We concatenate the key and value together, separating them with a colon (:) and a space.
#    This ensures that the key-value pair is displayed as "key: value".
# 4. The loop continues iterating over each key-value pair until all pairs have been processed.
