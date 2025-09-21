
from django.db import models
from apps.employees.models import Employee


class Performance(models.Model):
    """
    Performance model for tracking employee performance reviews.
    """
    STATUS_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('needs_improvement', 'Needs Improvement'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="performances", verbose_name="Employee")
    reviewer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="reviews_given", verbose_name="Reviewer")
    review_date = models.DateField(verbose_name="Review Date")
    performance_score = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Performance Score")
    goals_achievement = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Goals Achievement(%)")
    comments = models.TextField(blank=True, null=True, verbose_name="Comments")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Status")

    def __str__(self):
        return f"{self.employee.full_name} - {self.review_date} - {self.performance_score}"

    class Meta:
        verbose_name = "Performance Record"
        verbose_name_plural = "Performance Records"
        ordering = ['-review_date']


class Goal(models.Model):
    """
    Goal model for tracking employee goals.
    """
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    target_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.employee.full_name} - {self.title}"

    class Meta:
        verbose_name = "Goal"
        verbose_name_plural = "Goals"
        ordering = ['-target_date']


class Review(models.Model):
    """
    Review model for detailed performance reviews.
    """
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name="reviews")
    category = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.performance.employee.full_name} - {self.category} - {self.rating}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['category']
