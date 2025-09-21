# Employee Analytics API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [Employee Management API](#employee-management-api)
3. [Attendance Tracking API](#attendance-tracking-api)
4. [Performance Evaluation API](#performance-evaluation-api)
5. [Department Management API](#department-management-api)
6. [Analytics API](#analytics-api)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)

---

## Authentication

### Login
**Endpoint:** `POST /api/auth/login/`

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "token": "your_jwt_token_here"
}
```

### Logout
**Endpoint:** `POST /api/auth/logout/`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

---

## Employee Management API

### List All Employees
**Endpoint:** `GET /api/employees/`

**Parameters:**
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page
- `department` (optional): Filter by department ID
- `position` (optional): Filter by position ID
- `search` (optional): Search by name, employee ID, or email

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/employees/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "employee_id": "EMP001",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "phone": "123-456-7890",
      "hire_date": "2023-01-15",
      "department": {
        "id": 1,
        "name": "Engineering"
      },
      "position": {
        "id": 1,
        "title": "Software Developer"
      },
      "salary": 75000.00,
      "is_active": true
    }
  ]
}
```

### Get Employee by ID
**Endpoint:** `GET /api/employees/{id}/`

**Response:**
```json
{
  "id": 1,
  "employee_id": "EMP001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "123-456-7890",
  "hire_date": "2023-01-15",
  "department": {
    "id": 1,
    "name": "Engineering"
  },
  "position": {
    "id": 1,
    "title": "Software Developer"
  },
  "salary": 75000.00,
  "is_active": true,
  "performance_reviews": [
    {
      "id": 1,
      "review_date": "2023-06-15",
      "reviewer": "Jane Smith",
      "rating": 4,
      "comments": "Good performance with room for improvement in project management."
    }
  ]
}
```

### Create New Employee
**Endpoint:** `POST /api/employees/`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "employee_id": "EMP002",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com",
  "phone": "987-654-3210",
  "hire_date": "2023-02-20",
  "department": 1,
  "position": 2,
  "salary": 85000.00
}
```

**Response:**
```json
{
  "id": 2,
  "employee_id": "EMP002",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com",
  "phone": "987-654-3210",
  "hire_date": "2023-02-20",
  "department": {
    "id": 1,
    "name": "Engineering"
  },
  "position": {
    "id": 2,
    "title": "Senior Developer"
  },
  "salary": 85000.00,
  "is_active": true
}
```

### Update Employee
**Endpoint:** `PUT /api/employees/{id}/`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "employee_id": "EMP002",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith.updated@example.com",
  "phone": "987-654-3210",
  "hire_date": "2023-02-20",
  "department": 1,
  "position": 2,
  "salary": 90000.00
}
```

**Response:**
```json
{
  "id": 2,
  "employee_id": "EMP002",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith.updated@example.com",
  "phone": "987-654-3210",
  "hire_date": "2023-02-20",
  "department": {
    "id": 1,
    "name": "Engineering"
  },
  "position": {
    "id": 2,
    "title": "Senior Developer"
  },
  "salary": 90000.00,
  "is_active": true
}
```

### Delete Employee
**Endpoint:** `DELETE /api/employees/{id}/`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
```

**Response:**
```json
{
  "message": "Employee deleted successfully"
}
```

---

## Attendance Tracking API

### List All Attendance Records
**Endpoint:** `GET /api/attendances/`

**Parameters:**
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page
- `employee_id` (optional): Filter by employee ID
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)
- `status` (optional): Filter by attendance status (present, absent, late, leave)

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/attendances/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "employee": {
        "id": 1,
        "employee_id": "EMP001",
        "first_name": "John",
        "last_name": "Doe"
      },
      "date": "2023-11-01",
      "check_in": "2023-11-01T09:05:00Z",
      "check_out": "2023-11-01T17:30:00Z",
      "status": "present",
      "notes": "Arrived slightly late due to traffic"
    }
  ]
}
```

### Create Attendance Record
**Endpoint:** `POST /api/attendances/`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "employee": 1,
  "date": "2023-11-02",
  "check_in": "2023-11-02T08:55:00Z",
  "check_out": "2023-11-02T17:45:00Z",
  "status": "present",
  "notes": "Regular workday"
}
```

**Response:**
```json
{
  "id": 2,
  "employee": {
    "id": 1,
    "employee_id": "EMP001",
    "first_name": "John",
    "last_name": "Doe"
  },
  "date": "2023-11-02",
  "check_in": "2023-11-02T08:55:00Z",
  "check_out": "2023-11-02T17:45:00Z",
  "status": "present",
  "notes": "Regular workday"
}
```

---

## Performance Evaluation API

### List All Performance Records
**Endpoint:** `GET /api/performances/`

**Parameters:**
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page
- `employee_id` (optional): Filter by employee ID
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)
- `rating` (optional): Filter by rating (1-5)

**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/performances/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "employee": {
        "id": 1,
        "employee_id": "EMP001",
        "first_name": "John",
        "last_name": "Doe"
      },
      "review_date": "2023-10-15",
      "reviewer": "Jane Smith",
      "rating": 4,
      "goals": [
        {
          "id": 1,
          "title": "Complete Project X",
          "description": "Lead the development of Project X to completion",
          "status": "completed",
          "due_date": "2023-09-30"
        }
      ],
      "comments": "Good performance with room for improvement in project management.",
      "improvement_areas": [
        "Project management skills",
        "Team communication"
      ]
    }
  ]
}
```

### Create Performance Record
**Endpoint:** `POST /api/performances/`

**Headers:**
```
Authorization: Bearer your_jwt_token_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "employee": 1,
  "review_date": "2023-11-15",
  "reviewer": "Jane Smith",
  "rating": 4,
  "goals": [
    {
      "title": "Improve Documentation",
      "description": "Create comprehensive documentation for current projects",
      "status": "in_progress",
      "due_date": "2023-12-31"
    }
  ],
  "comments": "Consistent performer with strong technical skills.",
  "improvement_areas": [
    "Documentation practices",
    "Client communication"
  ]
}
```

**Response:**
```json
{
  "id": 2,
  "employee": {
    "id": 1,
    "employee_id": "EMP001",
    "first_name": "John",
    "last_name": "Doe"
  },
  "review_date": "2023-11-15",
  "reviewer": "Jane Smith",
  "rating": 4,
  "goals": [
    {
      "id": 3,
      "title": "Improve Documentation",
      "description": "Create comprehensive documentation for current projects",
      "status": "in_progress",
      "due_date": "2023-12-31"
    }
  ],
  "comments": "Consistent performer with strong technical skills.",
  "improvement_areas": [
    "Documentation practices",
    "Client communication"
  ]
}
```

---

## Department Management API

### List All Departments
**Endpoint:** `GET /api/departments/`

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Engineering",
      "description": "Software development and engineering team",
      "manager": {
        "id": 1,
        "employee_id": "EMP001",
        "first_name": "John",
        "last_name": "Doe"
      },
      "employee_count": 15
    }
  ]
}
```

### Get Department Summary
**Endpoint:** `GET /api/departments/summary/`

**Response:**
```json
{
  "departments": [
    {
      "id": 1,
      "name": "Engineering",
      "employee_count": 15,
      "avg_salary": 85000.00,
      "avg_performance_rating": 4.2,
      "turnover_rate": 0.05
    }
  ],
  "company_stats": {
    "total_employees": 50,
    "avg_salary": 75000.00,
    "avg_performance_rating": 4.0,
    "turnover_rate": 0.08
  }
}
```

---

## Analytics API

### Attendance Summary
**Endpoint:** `GET /api/summary/attendance/`

**Parameters:**
- `start_date` (optional): Start date for the summary (YYYY-MM-DD)
- `end_date` (optional): End date for the summary (YYYY-MM-DD)
- `department` (optional): Filter by department ID

**Response:**
```json
{
  "period": {
    "start_date": "2023-10-01",
    "end_date": "2023-10-31"
  },
  "summary": {
    "total_employees": 50,
    "average_attendance_rate": 95.5,
    "late_arrivals": 12,
    "early_departures": 8,
    "absences": 5,
    "leaves": 15
  },
  "by_department": [
    {
      "department": "Engineering",
      "employee_count": 15,
      "attendance_rate": 96.2,
      "late_arrivals": 3,
      "absences": 1
    }
  ]
}
```

### Performance Summary
**Endpoint:** `GET /api/summary/performance/`

**Parameters:**
- `start_date` (optional): Start date for the summary (YYYY-MM-DD)
- `end_date` (optional): End date for the summary (YYYY-MM-DD)
- `department` (optional): Filter by department ID

**Response:**
```json
{
  "period": {
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "summary": {
    "total_reviews": 50,
    "average_rating": 4.0,
    "rating_distribution": {
      "5": 10,
      "4": 25,
      "3": 10,
      "2": 3,
      "1": 2
    }
  },
  "by_department": [
    {
      "department": "Engineering",
      "review_count": 15,
      "average_rating": 4.2,
      "top_performers": 5
    }
  ]
}
```

---

## Error Handling

The API uses standard HTTP status codes and returns error information in JSON format:

### Common Error Responses

#### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid request data",
  "details": {
    "field_name": ["Error message for this field"]
  }
}
```

#### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Authentication credentials were not provided"
}
```

#### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "You do not have permission to perform this action"
}
```

#### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

---

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Default limit**: 100 requests per day per API key
- **Burst limit**: 10 requests per hour per API key
- **Headers included in responses**:
  - `X-RateLimit-Limit`: Current rate limit
  - `X-RateLimit-Remaining`: Remaining requests in the current period
  - `X-RateLimit-Reset`: Timestamp when the limit resets

When the rate limit is exceeded, the API returns a 429 status code:

```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded",
  "retry_after": 3600
}
```

To increase your rate limit, contact the system administrator.
