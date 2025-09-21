
from django.db import models
from apps.employees.models import Employee


class Attendance(models.Model):
    """
    Attendance model for tracking employee attendance.
    """
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('late', 'Late'),
        ('early_leave', 'Early Leave'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendances", verbose_name="Employee")
    date = models.DateField(verbose_name="Date")
    check_in = models.DateTimeField(null=True, blank=True, verbose_name="Check-in Time")
    check_out = models.DateTimeField(null=True, blank=True, verbose_name="Check-out Time")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present', verbose_name="Status")
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Hours Worked")
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Overtime Hours")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"
        unique_together = ('employee', 'date')
        ordering = ('-date',)


class TimeLog(models.Model):
    """
    TimeLog model for detailed time tracking.
    """
    LOG_TYPE_CHOICES = [
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),
        ('break_start', 'Break Start'),
        ('break_end', 'Break End'),
    ]

    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name="time_logs")
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES)
    timestamp = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.attendance.employee.full_name} - {self.log_type} - {self.timestamp}"

    class Meta:
        verbose_name = "Time Log"
        verbose_name_plural = "Time Logs"
        ordering = ('timestamp',)
