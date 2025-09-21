
from django.db import models  # Django's database models framework
from django.contrib.auth.models import User  # Django's built-in User model


class Department(models.Model):
    """
    Department model representing company departments.
    
    This model stores information about company departments such as Engineering, 
    Marketing, HR, etc. Each department can have multiple positions and employees.
    
    Attributes:
        name (CharField): The name of the department (must be unique)
        description (TextField): Optional description of the department
    
    Methods:
        __str__: Returns the department name as string representation
    
    Meta:
        verbose_name: Human-readable name for the model
        verbose_name_plural: Plural form of the verbose_name
    """
    name = models.CharField(max_length=100, unique=True, help_text="Name of the department")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the department")

    def __str__(self):
        """String representation of the Department model."""
        return self.name

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"


class Position(models.Model):
    """
    Position model representing job positions within departments.
    
    This model defines job positions within departments, including salary ranges
    and position descriptions. Each position is associated with a specific department.
    
    Attributes:
        title (CharField): Job title (e.g., "Software Developer")
        department (ForeignKey): Reference to the Department model
        description (TextField): Optional description of the position
        min_salary (DecimalField): Minimum salary for this position
        max_salary (DecimalField): Maximum salary for this position
    
    Methods:
        __str__: Returns formatted position title and department name
    
    Meta:
        verbose_name: Human-readable name for the model
        verbose_name_plural: Plural form of the verbose_name
        unique_together: Ensures position titles are unique within each department
    """
    title = models.CharField(max_length=100, help_text="Job title (e.g., Software Developer)")
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name="positions",
        help_text="Department this position belongs to"
    )
    description = models.TextField(blank=True, null=True, help_text="Optional description of the position")
    min_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="Minimum salary for this position"
    )
    max_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="Maximum salary for this position"
    )

    def __str__(self):
        """String representation of the Position model."""
        return f"{self.title} - {self.department.name}"

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        unique_together = ('title', 'department')


class Employee(models.Model):
    """
    Employee model representing company employees.
    
    This model stores comprehensive information about employees, including personal 
    details, employment information, and organizational relationships.
    
    Attributes:
        employee_id (CharField): Unique employee identifier
        user (OneToOneField): Reference to Django User model (optional)
        first_name (CharField): Employee's first name
        last_name (CharField): Employee's last name
        gender (CharField): Employee's gender with predefined choices
        email (EmailField): Employee's email address (unique)
        phone (CharField): Employee's phone number
        department (ForeignKey): Reference to Department model
        position (ForeignKey): Reference to Position model
        hire_date (DateField): Date when employee was hired
        salary (DecimalField): Employee's current salary
        manager (ForeignKey): Self-referencing field for reporting structure
        is_active (BooleanField): Whether employee is currently active
        profile_image (ImageField): Employee's profile photo
    
    Methods:
        __str__: Returns formatted employee name with ID
        full_name: Property that returns the employee's full name
    
    Meta:
        verbose_name: Human-readable name for the model
        verbose_name_plural: Plural form of the verbose_name
        ordering: Default ordering for employee records
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    employee_id = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Employee ID",
        help_text="Unique employee identifier"
    )
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="employee_profile",
        help_text="Django user account associated with this employee (optional)"
    )
    first_name = models.CharField(
        max_length=50, 
        verbose_name="First Name",
        help_text="Employee's first name"
    )
    last_name = models.CharField(
        max_length=50, 
        verbose_name="Last Name",
        help_text="Employee's last name"
    )
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        null=True, 
        blank=True,
        help_text="Employee's gender"
    )
    email = models.EmailField(
        unique=True, 
        verbose_name="Email",
        help_text="Employee's email address"
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Phone Number",
        help_text="Employee's phone number"
    )
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="employees", 
        verbose_name="Department",
        help_text="Department where employee works"
    )
    position = models.ForeignKey(
        Position, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="employees", 
        verbose_name="Position",
        help_text="Employee's job position"
    )
    hire_date = models.DateField(
        verbose_name="Hire Date",
        help_text="Date when employee was hired"
    )
    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Salary",
        help_text="Employee's current salary"
    )
    manager = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="subordinates", 
        verbose_name="Manager",
        help_text="Employee's direct manager (optional)"
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Employment Status",
        help_text="Whether employee is currently active"
    )
    profile_image = models.ImageField(
        upload_to='profile_images/', 
        null=True, 
        blank=True, 
        verbose_name="Profile Image",
        help_text="Employee's profile photo"
    )

    def __str__(self):
        """String representation of the Employee model."""
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

    @property
    def full_name(self):
        """
        Property that returns the employee's full name.
        
        Returns:
            str: Employee's first and last name combined
        """
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ('last_name', 'first_name')
