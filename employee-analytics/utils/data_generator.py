
import random
from datetime import datetime, timedelta
from faker import Faker
from django.contrib.auth.models import User

from apps.employees.models import Employee, Department, Position
from apps.attendance.models import Attendance, TimeLog
from apps.performance.models import Performance, Goal, Review

fake = Faker('en_US')

# Department list
DEPARTMENTS = [
    {'name': 'Technology', 'description': 'Responsible for company technology R&D and product innovation'},
    {'name': 'Marketing', 'description': 'Responsible for market promotion and brand building'},
    {'name': 'Sales', 'description': 'Responsible for product sales and customer relationship maintenance'},
    {'name': 'Human Resources', 'description': 'Responsible for human resource management and corporate culture building'},
    {'name': 'Finance', 'description': 'Responsible for company financial management and accounting'},
]

# Position list
POSITIONS = {
    'Technology': ['CTO', 'Senior Engineer', 'Software Engineer', 'Junior Engineer', 'Test Engineer'],
    'Marketing': ['CMO', 'Marketing Manager', 'Marketing Specialist', 'Brand Manager', 'Media Specialist'],
    'Sales': ['Sales Director', 'Sales Manager', 'Sales Representative', 'Account Manager', 'Sales Assistant'],
    'Human Resources': ['HR Director', 'HR Manager', 'Recruitment Specialist', 'Training Specialist', 'Compensation Specialist'],
    'Finance': ['CFO', 'Finance Manager', 'Accountant', 'Cashier', 'Financial Analyst'],
}

# Salary ranges (based on position level)
SALARY_RANGES = {
    'Director': (80000, 150000),
    'Manager': (60000, 100000),
    'Senior': (50000, 80000),
    'Specialist': (40000, 60000),
    'Engineer': (50000, 90000),
    'Assistant': (35000, 50000),
    'Other': (40000, 70000),
}

def get_salary_range(position):
    """Get salary range based on position"""
    for key, value in SALARY_RANGES.items():
        if key in position:
            return value
    return SALARY_RANGES['Other']

def generate_departments():
    """Generate department data"""
    departments = []
    for dept_data in DEPARTMENTS:
        department, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={'description': dept_data['description']}
        )
        departments.append(department)
    return departments

def generate_positions():
    """Generate position data"""
    positions = []
    departments = Department.objects.all()

    for dept in departments:
        if dept.name in POSITIONS:
            for pos_title in POSITIONS[dept.name]:
                min_salary, max_salary = get_salary_range(pos_title)
                position, created = Position.objects.get_or_create(
                    title=pos_title,
                    department=dept,
                    defaults={
                        'description': f'{pos_title} position in {dept.name}',
                        'min_salary': min_salary,
                        'max_salary': max_salary
                    }
                )
                positions.append(position)
    return positions

def generate_employee_data(count=5):
    """Generate employee data"""
    # Ensure departments and positions exist
    departments = generate_departments()
    positions = generate_positions()

    # Generate employee data
    employees = []
    for i in range(count):
        # Randomly select department and position
        department = random.choice(departments)
        available_positions = Position.objects.filter(department=department)
        position = random.choice(available_positions) if available_positions else None

        # Generate name and user information
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
        email = fake.email()

        # Create Django user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        )

        # Generate employee ID
        employee_id = f"EMP{random.randint(10000, 99999)}"

        # Generate salary
        if position:
            min_salary = position.min_salary
            max_salary = position.max_salary
        else:
            min_salary, max_salary = get_salary_range("Other")
        salary = random.randint(min_salary, max_salary)

        # Generate hire date (1-5 years ago)
        hire_date = datetime.now() - timedelta(days=random.randint(365, 1825))

        # Create employee
        employee, created = Employee.objects.get_or_create(
            employee_id=employee_id,
            defaults={
                'user': user,
                'first_name': first_name,
                'last_name': last_name,
                'gender': random.choice(['M', 'F']),
                'email': email,
                'phone': fake.phone_number()[:20],
                'department': department,
                'position': position,
                'hire_date': hire_date,
                'salary': salary,
                'is_active': True,
            }
        )

        employees.append(employee)

    # Generate attendance records for employees (past 30 days)
    for employee in employees:
        # Randomly generate attendance records for the past 30 days
        for days_ago in range(1, 31):
            date = datetime.now() - timedelta(days=days_ago)

            # Skip weekends
            if date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                continue

            # Randomly determine attendance status
            status_rand = random.random()
            if status_rand < 0.1:  # 10% chance of absence
                status = 'absent'
                check_in = None
                check_out = None
                hours_worked = 0
            elif status_rand < 0.2:  # 10% chance of being late
                status = 'late'
                check_in = datetime.combine(date, datetime.min.time()) + timedelta(hours=9, minutes=random.randint(15, 60))
                check_out = datetime.combine(date, datetime.min.time()) + timedelta(hours=18, minutes=random.randint(0, 30))
                hours_worked = round((check_out - check_in).total_seconds() / 3600, 2)
            elif status_rand < 0.25:  # 5% chance of early leave
                status = 'early_leave'
                check_in = datetime.combine(date, datetime.min.time()) + timedelta(hours=8, minutes=random.randint(0, 30))
                check_out = datetime.combine(date, datetime.min.time()) + timedelta(hours=17, minutes=random.randint(0, 30))
                hours_worked = round((check_out - check_in).total_seconds() / 3600, 2)
            elif status_rand < 0.3:  # 5% chance of leave
                status = 'leave'
                check_in = None
                check_out = None
                hours_worked = 0
            else:  # 70% chance of normal attendance
                status = 'present'
                check_in = datetime.combine(date, datetime.min.time()) + timedelta(hours=8, minutes=random.randint(0, 30))
                check_out = datetime.combine(date, datetime.min.time()) + timedelta(hours=18, minutes=random.randint(0, 60))
                hours_worked = round((check_out - check_in).total_seconds() / 3600, 2)

            # Calculate overtime hours
            overtime_hours = 0
            if hours_worked > 8:
                overtime_hours = round(hours_worked - 8, 2)

            # Create attendance record
            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=date.date(),
                defaults={
                    'check_in': check_in,
                    'check_out': check_out,
                    'status': status,
                    'hours_worked': hours_worked,
                    'overtime_hours': overtime_hours,
                }
            )

            # Create time logs if check-in and check-out times are available
            if check_in:
                TimeLog.objects.create(
                    attendance=attendance,
                    log_type='check_in',
                    timestamp=check_in
                )
            if check_out:
                TimeLog.objects.create(
                    attendance=attendance,
                    log_type='check_out',
                    timestamp=check_out
                )

    # Generate performance records for employees (1-2 times per year)
    for employee in employees:
        hire_date = employee.hire_date
        current_date = datetime.now().date()

        # Calculate years of employment
        years_employed = (current_date - hire_date).days / 365.25

        # Generate 1-2 performance evaluations per year
        for year in range(int(years_employed) + 1):
            review_count = random.randint(1, 2)

            for i in range(review_count):
                # Determine review date (random time within the year)
                if year == 0:  # First year of employment
                    # Conduct reviews at 6 months and 12 months after hiring
                    if i == 0:
                        review_date = hire_date + timedelta(days=180)
                    else:
                        review_date = hire_date + timedelta(days=365)
                else:
                    # Conduct reviews at random times in other years
                    start_date = hire_date + timedelta(days=365 * year)
                    end_date = hire_date + timedelta(days=365 * (year + 1))
                    days_diff = (end_date - start_date).days
                    review_date = start_date + timedelta(days=random.randint(1, days_diff))

                # Ensure review date is not later than current date
                if review_date > current_date:
                    continue

                # Select reviewer (usually another employee in the department or a manager)
                potential_reviewers = Employee.objects.filter(
                    department=employee.department,
                    is_active=True
                ).exclude(id=employee.id)

                if potential_reviewers.exists():
                    reviewer = random.choice(potential_reviewers)
                else:
                    reviewer = None

                # Generate performance score and goals achievement
                performance_score = round(random.uniform(3.0, 5.0), 1)
                goals_achievement = round(random.uniform(70.0, 120.0), 2)

                # Determine status based on performance score
                if performance_score >= 4.5:
                    status = 'excellent'
                elif performance_score >= 4.0:
                    status = 'good'
                elif performance_score >= 3.5:
                    status = 'average'
                else:
                    status = 'needs_improvement'

                # Generate comments
                comments = fake.paragraph(nb_sentences=3)

                # Create performance record
                performance, created = Performance.objects.get_or_create(
                    employee=employee,
                    review_date=review_date,
                    defaults={
                        'reviewer': reviewer,
                        'performance_score': performance_score,
                        'goals_achievement': goals_achievement,
                        'comments': comments,
                        'status': status,
                    }
                )

                # Generate detailed reviews for the performance record
                review_categories = ['Technical Skills', 'Communication', 'Teamwork', 'Problem Solving', 'Leadership']
                for category in review_categories:
                    rating = round(random.uniform(3.0, 5.0), 1)
                    review_comments = fake.sentence()

                    Review.objects.create(
                        performance=performance,
                        category=category,
                        rating=rating,
                        comments=review_comments
                    )

                # Generate goals for the employee
                num_goals = random.randint(1, 3)
                for j in range(num_goals):
                    goal_title = fake.sentence(nb_words=4)
                    goal_description = fake.paragraph(nb_sentences=2)
                    goal_start_date = review_date
                    goal_target_date = goal_start_date + timedelta(days=random.randint(90, 365))

                    # Randomly determine if goal is completed
                    if goal_target_date <= current_date and random.random() < 0.7:  # 70% chance of completion if target date passed
                        goal_status = 'completed'
                        goal_completion_date = goal_target_date - timedelta(days=random.randint(0, 30))
                        goal_progress = 100.0
                    elif goal_target_date > current_date:
                        goal_status = 'in_progress'
                        goal_completion_date = None
                        goal_progress = round(random.uniform(10, 90), 2)
                    else:
                        goal_status = 'on_hold'
                        goal_completion_date = None
                        goal_progress = round(random.uniform(10, 80), 2)

                    Goal.objects.create(
                        employee=employee,
                        title=goal_title,
                        description=goal_description,
                        start_date=goal_start_date,
                        target_date=goal_target_date,
                        completion_date=goal_completion_date,
                        status=goal_status,
                        progress=goal_progress
                    )

    return {
        'employees_created': len(employees),
        'attendances_created': Attendance.objects.count(),
        'performances_created': Performance.objects.count(),
        'goals_created': Goal.objects.count(),
    }
