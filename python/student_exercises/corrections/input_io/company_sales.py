import csv
# import matplotlib.pyplot as plt
# conda install matplotlib
import os

CURRENT_DIR: str = os.path.dirname(os.path.realpath(__file__))

def read_sales_data() -> list[dict[str, str|int]]:
    """
    Reads the sales data from the "sales_data.csv" file.

    Arguments: None

    Returns:
    - sales_data (list): List of dictionaries representing sales data.
    """
    sales_path: str = os.path.join(CURRENT_DIR, "sales_data.csv")
    sales_data: list[dict[str, str | int]] = []

    with open(sales_path, "r") as sales_csv:
        csv_reader = csv.DictReader(sales_csv)
        for row in csv_reader:
            row["Amount"] = int(row["Amount"])
            sales_data.append(row)
    return sales_data


def read_employee_data() -> list[dict[str, str|int]]:
    """
    Reads the employee data from the "employee_data.csv" file.

    Arguments: None

    Returns:
    - employee_data (list): List of dictionaries representing employee data.
    """
    employee_path: str = os.path.join(CURRENT_DIR, "employee_data.csv")
    employee_data: list[dict[str, str | int]] = []

    with open(employee_path, "r") as employee_csv:
        csv_reader = csv.DictReader(employee_csv)
        employee_data = [row | {"Salary": int(row["Salary"])} for row in csv_reader]
    return employee_data

def calculate_total_sales(sales_data: list[dict[str, str|int]]) -> int:
    """
    Calculates the total sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - total_sales (float): Total sales amount.
    """
    return sum([row["Amount"] for row in sales_data])
        


def calculate_average_sales(sales_data: list[dict[str, str|int]]) -> float:
    """
    Calculates the average sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - average_sales (float): Average sales amount.
    """
    return calculate_total_sales(sales_data) / len(sales_data)

def calculate_median_sales(sales_data: list[dict[str, str|int]]) -> float:
    """
    Calculates the median sales amount.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.

    Returns:
    - median_sales (float): Median sales amount.
    """
    amounts: list[int] = [row["Amount"] for row in sales_data]
    amounts_sorted: list[int] = sorted(amounts)
    mid: int = len(amounts_sorted) // 2
    # return float(amounts_sorted[mid]) if len(amounts_sorted) % 2 == 1 else (amounts_sorted[mid-1] + amounts_sorted[mid]) / 2
    if len(amounts_sorted) % 2 == 1: 
        return float(amounts_sorted[mid]) 
    return (amounts_sorted[mid-1] + amounts_sorted[mid]) / 2

def calculate_total_salary_expenses(employee_data):
    """
    Calculates the total salary expenses.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - total_salary_expenses (float): Total salary expenses.
    """
    return sum([row["Salary"] for row in employee_data])


def calculate_average_salary(employee_data):
    """
    Calculates the average salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - average_salary (float): Average salary.
    """
    return calculate_total_salary_expenses(employee_data) / len(employee_data)

def calculate_median_salary(employee_data):
    """
    Calculates the median salary.

    Arguments:
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - median_salary (float): Median salary.
    """
    import statistics
    return statistics.median([row["Salary"] for row in employee_data])


def find_employee_with_highest_sales(sales_data, employee_data) -> tuple[str, str]:
    """
    Finds the employee with the highest sales amount sum.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - employee_name (str): Name of the employee with the highest sales amount.
    - department_name (str): Name of the department of the employee with the highest sales amount.
    """
    emp_sales: list[dict[str | int, float | int]] = []

    for emp_id in [int(row["EmployeeID"]) for row in employee_data]:
      sum_: float = sum([float(row["Amount"]) for row in sales_data if int(row["EmployeeID"]) == emp_id])
      it: dict[str, int | float] = {}
      it["emp_id"] = emp_id
      it["Amount"] = sum_
      emp_sales.append(it)
    
    max_emp_id: int = int(emp_sales[0]["emp_id"])
    max_sale_sum = float(emp_sales[0]["Amount"])

    for row in emp_sales[1:]:
      if row["Amount"] > max_sale_sum:
          max_emp_id = row["emp_id"]
          max_sale_sum = row["Amount"]
    
    for emp in employee_data:
      if int(emp["EmployeeID"]) == max_emp_id:
          return emp["Name"], emp["Department"]
    return None


def find_department_with_highest_sales(sales_data, employee_data):
    """
    Finds the department with the highest sales sum.

    Arguments:
    - sales_data (list): List of dictionaries representing sales data.
    - employee_data (list): List of dictionaries representing employee data.

    Returns:
    - department_name (str): Name of the department with the highest sales.
    """
    user_dep: dict[str, str] = {}
    for emp in employee_data:
      user_dep[emp["EmployeeID"]] = emp["Department"]

    dep_sales: dict[str, int] = {}
    for sale in sales_data:
      user_department: str = user_dep[sale["EmployeeID"]]
      dep_sales[user_department] = dep_sales.get(user_department, 0) + sale["Amount"]
      
      # if user_department in dep_sales:
      #   dep_sales[user_department] = dep_sales[user_department] + sale["Amount"]
      # else:  
      #   dep_sales[user_department] = 0 + sale["Amount"]
    
    # return max(dep_sales, key=lambda department: dep_sales[department])
    return max(dep_sales, key=dep_sales.get)


# def plot_sales_by_department(sales_data, employee_data):
#     """
#     Plots a bar chart showing the total sales by department.

#     Arguments:
#     - sales_data (list): List of dictionaries representing sales data.
#     - employee_data (list): List of dictionaries representing employee data.

#     Returns: None
#     """
#     pass


# def plot_sales_vs_salary(sales_data, employee_data):
#     """
#     Plots a scatter plot showing the relationship between sales and salary.

#     Arguments:
#     - sales_data (list): List of dictionaries representing sales data.
#     - employee_data (list): List of dictionaries representing employee data.

#     Returns: None
#     """
#     pass


def main():
    # Read sales data
    sales_data: list[dict[str, str | int]] = read_sales_data()

    # Read employee data
    employee_data: list[dict[str, str | int]] = read_employee_data()

    # Calculate total sales amount
    total_sales = calculate_total_sales(sales_data)
    print("Total Sales Amount:", total_sales)

    # Calculate average sales amount
    average_sales = calculate_average_sales(sales_data)
    print("Average Sales Amount:", average_sales)

    # Calculate median sales amount
    median_sales = calculate_median_sales(sales_data)
    print("Median Sales Amount:", median_sales)

    # Calculate total salary expenses
    total_salary_expenses = calculate_total_salary_expenses(employee_data)
    print("Total Salary Expenses:", total_salary_expenses)

    # Calculate average salary
    average_salary = calculate_average_salary(employee_data)
    print("Average Salary:", average_salary)

    # Calculate median salary
    median_salary = calculate_median_salary(employee_data)
    print("Median Salary:", median_salary)

    # Find the employee with the highest sales amount
    highest_sales_employee, highest_sales_employee_dep = find_employee_with_highest_sales(sales_data, employee_data)
    print("Employee with Highest Sales Amount:", highest_sales_employee, highest_sales_employee_dep)

    # Find the department with the highest sales
    highest_sales_department = find_department_with_highest_sales(sales_data, employee_data)
    print("Department with Highest Sales:", highest_sales_department)

    # Plot total sales by department
    # plot_sales_by_department(sales_data, employee_data)

    # Plot sales vs. salary
    # plot_sales_vs_salary(sales_data, employee_data)


if __name__ == '__main__':
    main()
    # d = {"Italy": "Rome", "England": "London", "Germany": "Berlin"}
    # for item in d:
    #     print(item)