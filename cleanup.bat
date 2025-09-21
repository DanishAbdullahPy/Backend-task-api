@echo off
echo Starting cleanup of old Django project structures...

REM Remove old employee_data directory
if exist "employee_data" (
    echo Removing employee_data directory...
    rmdir /s /q "employee_data"
    echo employee_data directory removed.
) else (
    echo employee_data directory not found.
)

REM Remove old employee_data_project directory
if exist "employee_data_project" (
    echo Removing employee_data_project directory...
    rmdir /s /q "employee_data_project"
    echo employee_data_project directory removed.
) else (
    echo employee_data_project directory not found.
)

REM Remove old health_check directory
if exist "health_check" (
    echo Removing health_check directory...
    rmdir /s /q "health_check"
    echo health_check directory removed.
) else (
    echo health_check directory not found.
)

REM Remove old manage.py file
if exist "manage.py" (
    echo Removing old manage.py file...
    del "manage.py"
    echo Old manage.py file removed.
) else (
    echo Old manage.py file not found.
)

REM Remove old requirements.txt file
if exist "requirements.txt" (
    echo Removing old requirements.txt file...
    del "requirements.txt"
    echo Old requirements.txt file removed.
) else (
    echo Old requirements.txt file not found.
)

echo Cleanup completed successfully!
echo The employee-analytics/ directory now contains the clean, organized project structure.
pause
