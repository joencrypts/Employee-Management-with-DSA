import sqlite3
import pandas as pd
import time
import sys

# Connect to SQLite database (it will create one if not exists)
conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

def add_employee():
    id = int(input("Enter employee ID: "))
    name = input("Enter employee name: ")
    salary = float(input("Enter employee salary: "))
    cursor.execute("INSERT INTO employees (id, name, salary) VALUES (?, ?, ?)", (id, name, salary))
    conn.commit()
    print("Employee added successfully!")

def search_and_edit_employee():
    id = int(input("Enter employee ID to search: "))
    cursor.execute("SELECT * FROM employees WHERE id = ?", (id,))
    employee = cursor.fetchone()
    if employee:
        print(f"Found employee: ID={employee[0]}, Name={employee[1]}, Salary={employee[2]}")
        new_name = input("Enter new name or press enter to skip: ")
        new_salary = input("Enter new salary or press enter to skip: ")
        if new_name:
            cursor.execute("UPDATE employees SET name = ? WHERE id = ?", (new_name, id))
        if new_salary:
            cursor.execute("UPDATE employees SET salary = ? WHERE id = ?", (new_salary, id))
        conn.commit()
        print("Employee updated successfully!")
    else:
        print("Employee not found.")

def export_employees_to_excel(filename):
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    df.to_excel(filename, index=False)
    print(f"Data exported to {filename} successfully!")

def sort_employees():
    global sorted_df  # To hold the sorted data frame
    sorted_df = pd.read_sql_query("SELECT * FROM employees ORDER BY name ASC", conn)
    print("Employee data sorted by name successfully!")

def export_sorted_employees_to_excel(filename='sorted_employees.xlsx'):
    global sorted_df
    if 'sorted_df' in globals():
        sorted_df.to_excel(filename, index=False)
        print(f"Sorted data exported to {filename} successfully!")
    else:
        print("No sorted data to export. Please sort the data first.")

def main():
    while True:
        choice = input("Press 1 to add, 2 to search/edit, 3 to export all, 4 to sort by name, 5 to export sorted data, 0 to exit: ")
        start_time = time.time()
        if choice == '1':
            add_employee()
        elif choice == '2':
            search_and_edit_employee()
        elif choice == '3':
            export_employees_to_excel('employees.xlsx')
        elif choice == '4':
            sort_employees()
        elif choice == '5':
            export_sorted_employees_to_excel()
        elif choice == '0':
            break
        else:
            print("Invalid choice.")
        
        elapsed_time = time.time() - start_time
        memory_usage = sys.getsizeof(globals())
        print(f"Time taken: {elapsed_time*1000:.2f} ms")
        print(f"Memory used: {memory_usage} bytes")

if __name__ == "__main__":
    main()
