from apps.employees.models import Department, Position, Employee
from apps.performance.models import Performance, Goal, Review
from django.contrib.auth.models import User
from datetime import date, datetime

def create_sample_data():
    # Create Departments
    dept_sales, _ = Department.objects.get_or_create(name="Sales", defaults={"description": "Sales Department"})
    dept_hr, _ = Department.objects.get_or_create(name="HR", defaults={"description": "Human Resources"})

    # Create Positions
    pos_manager, _ = Position.objects.get_or_create(title="Manager", department=dept_sales, defaults={"min_salary": 50000, "max_salary": 80000})
    pos_executive, _ = Position.objects.get_or_create(title="Executive", department=dept_sales, defaults={"min_salary": 30000, "max_salary": 50000})
    pos_hr_specialist, _ = Position.objects.get_or_create(title="HR Specialist", department=dept_hr, defaults={"min_salary": 35000, "max_salary": 60000})

    # Create Users and Employees
    user1, _ = User.objects.get_or_create(username="jdoe", defaults={"first_name": "John", "last_name": "Doe", "email": "jdoe@example.com"})
    emp1, _ = Employee.objects.get_or_create(employee_id="E001", defaults={
        "user": user1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "jdoe@example.com",
        "department": dept_sales,
        "position": pos_manager,
        "hire_date": date(2020, 1, 15),
        "salary": 70000,
        "is_active": True,
    })

    user2, _ = User.objects.get_or_create(username="asmith", defaults={"first_name": "Alice", "last_name": "Smith", "email": "asmith@example.com"})
    emp2, _ = Employee.objects.get_or_create(employee_id="E002", defaults={
        "user": user2,
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "asmith@example.com",
        "department": dept_sales,
        "position": pos_executive,
        "hire_date": date(2021, 6, 1),
        "salary": 45000,
        "is_active": True,
    })

    # Create Performance records
    perf1, _ = Performance.objects.get_or_create(employee=emp1, reviewer=emp2, review_date=date(2023, 12, 31), defaults={
        "performance_score": 4.5,
        "goals_achievement": 90,
        "comments": "Excellent performance",
        "status": "completed",
    })

    perf2, _ = Performance.objects.get_or_create(employee=emp2, reviewer=emp1, review_date=date(2023, 12, 31), defaults={
        "performance_score": 3.8,
        "goals_achievement": 75,
        "comments": "Good performance",
        "status": "completed",
    })

    # Create Goals
    Goal.objects.get_or_create(employee=emp1, title="Increase sales by 10%", defaults={
        "description": "Achieve a 10% increase in sales by Q4",
        "start_date": date(2023, 1, 1),
        "target_date": date(2023, 12, 31),
        "status": "in_progress",
        "progress": 50,
    })

    Goal.objects.get_or_create(employee=emp2, title="Improve customer satisfaction", defaults={
        "description": "Raise customer satisfaction scores by 15%",
        "start_date": date(2023, 1, 1),
        "target_date": date(2023, 12, 31),
        "status": "in_progress",
        "progress": 60,
    })

    # Create Reviews
    Review.objects.get_or_create(performance=perf1, category="Quality", rating=5, comments="Outstanding quality of work")
    Review.objects.get_or_create(performance=perf1, category="Punctuality", rating=4, comments="Usually on time")
    Review.objects.get_or_create(performance=perf2, category="Quality", rating=3, comments="Meets expectations")
    Review.objects.get_or_create(performance=perf2, category="Punctuality", rating=4, comments="Good attendance")

    print("Sample data created successfully.")
