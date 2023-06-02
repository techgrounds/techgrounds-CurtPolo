import csv

register_dict = {}

first_name = input("Enter your name: ")
register_dict["Name"] = first_name

last_name = input("Enter your surname: ")
register_dict["Surname"] = last_name

job_title = input("Enter your job title: ")
register_dict["Job Title"] = job_title

company = input("Enter your company: ")
register_dict["Company"] = company


with open("register.csv", "a", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(register_dict.values())

print("Data written to register.csv successfully.")