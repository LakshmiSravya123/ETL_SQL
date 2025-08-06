# Health Analytics API

A comprehensive health analytics API built with Vapor, providing endpoints for tracking health metrics, insights, goals, and nutrition.

## Authentication

All API endpoints (except registration and login) require authentication using Bearer token.

### Register a New User

```http
POST /register
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword"
}
```

Success Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john@example.com"
}
```

Error Response (Email already exists):
```json
{
    "error": true,
    "reason": "A user with this email already exists"
}
```

### Login

```http
POST /login
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "securepassword"
}
```

Success Response:
```json
{
    "token": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    },
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "John Doe",
        "email": "john@example.com"
    }
}
```

Error Response (Invalid credentials):
```json
{
    "error": true,
    "reason": "Invalid email or password"
}
```

## Health Metrics

### Get Today's Metrics

```http
GET /api/health/metrics
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Success Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2024-03-19T10:30:00Z",
    "steps": 8500,
    "heartRate": 72,
    "sleepHours": 7.5,
    "caloriesBurned": 2100,
    "activeMinutes": 35
}
```

Error Response (No metrics found):
```json
{
    "error": true,
    "reason": "No metrics found for today"
}
```

### Create Metrics

```http
POST /api/health/metrics
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "steps": 10000,
    "heartRate": 75,
    "sleepHours": 7.5,
    "caloriesBurned": 2500,
    "activeMinutes": 45
}
```

Success Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2024-03-19T15:45:00Z",
    "steps": 10000,
    "heartRate": 75,
    "sleepHours": 7.5,
    "caloriesBurned": 2500,
    "activeMinutes": 45
}
```

### Get Historical Metrics

```http
GET /api/health/metrics/history?days=7
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Success Response:
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "date": "2024-03-19T00:00:00Z",
        "steps": 10000,
        "heartRate": 75,
        "sleepHours": 7.5,
        "caloriesBurned": 2500,
        "activeMinutes": 45
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "date": "2024-03-18T00:00:00Z",
        "steps": 8500,
        "heartRate": 72,
        "sleepHours": 8.0,
        "caloriesBurned": 2300,
        "activeMinutes": 40
    }
]
```

### Get Health Statistics

```http
GET /api/health/metrics/stats
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Success Response:
```json
{
    "periodDays": 30,
    "averageSteps": 9200,
    "averageHeartRate": 73,
    "averageSleepHours": 7.8,
    "averageCaloriesBurned": 2400,
    "averageActiveMinutes": 42
}
```

## Health Insights

### Get Today's Insights

```http
GET /api/health/insights
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Success Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2024-03-19T00:00:00Z",
    "stepsGoalMet": true,
    "restingHeartRateStatus": "Normal",
    "sleepQuality": "Good",
    "activityLevel": "Active",
    "recommendations": [
        "Keep up the good work!",
        "Try to get 8 hours of sleep tonight",
        "Consider taking a walk after lunch"
    ]
}
```

### Create Insights

```http
POST /api/health/insights
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "stepsGoalMet": true,
    "restingHeartRateStatus": "Normal",
    "sleepQuality": "Good",
    "activityLevel": "Active",
    "recommendations": [
        "Keep up the good work!",
        "Try to get 8 hours of sleep tonight"
    ]
}
```

Success Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2024-03-19T16:30:00Z",
    "stepsGoalMet": true,
    "restingHeartRateStatus": "Normal",
    "sleepQuality": "Good",
    "activityLevel": "Active",
    "recommendations": [
        "Keep up the good work!",
        "Try to get 8 hours of sleep tonight"
    ]
}
```

## Health Goals

### Get Current Goals

```http
GET /api/health/goals
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Success Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "dailyStepsGoal": 10000,
    "dailyActiveMinutesGoal": 30,
    "dailyCaloriesGoal": 2500,
    "sleepHoursGoal": 8.0
}
```

### Set Goals

```http
POST /api/health/goals
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInT5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "dailyStepsGoal": 10000,
    "dailyActiveMinutesGoal": 30,
    "dailyCaloriesGoal": 2500,
    "sleepHoursGoal": 8.0
}
```

Success Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "dailyStepsGoal": 10000,
    "dailyActiveMinutesGoal": 30,
    "dailyCaloriesGoal": 2500,
    "sleepHoursGoal": 8.0,
    "createdAt": "2024-03-19T16:30:00Z",
    "updatedAt": "2024-03-19T16:30:00Z"
}
```

### Get Progress Report

```http
GET /api/health/goals/progress
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Success Response:
```json
{
    "period": "Last 7 days",
    "stepsProgress": 0.92,
    "activeMinutesProgress": 1.15,
    "caloriesProgress": 0.95,
    "sleepProgress": 0.94
}
```

## Nutrition Tracking

### Get Today's Meals

```http
GET /api/health/meals
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Success Response:
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "userId": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Breakfast",
        "date": "2024-03-19T08:00:00Z",
        "calories": 450,
        "protein": 15,
        "carbs": 65,
        "fat": 12,
        "foodItems": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "Oatmeal",
                "calories": 150,
                "protein": 6,
                "carbs": 27,
                "fat": 3,
                "servingSize": "1 cup"
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "name": "Banana",
                "calories": 105,
                "protein": 1.3,
                "carbs": 27,
                "fat": 0.4,
                "servingSize": "1 medium"
            }
        ]
    }
]
```

### Log a Meal

```http
POST /api/health/meals
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "name": "Breakfast",
    "foodItems": [
        {
            "name": "Oatmeal",
            "calories": 150,
            "protein": 6.0,
            "carbs": 27.0,
            "fat": 3.0,
            "servingSize": "1 cup"
        },
        {
            "name": "Banana",
            "calories": 105,
            "protein": 1.3,
            "carbs": 27.0,
            "fat": 0.4,
            "servingSize": "1 medium"
        }
    ]
}
```

Success Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Breakfast",
    "date": "2024-03-19T08:00:00Z",
    "calories": 255,
    "protein": 7.3,
    "carbs": 54.0,
    "fat": 3.4,
    "foodItems": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "name": "Oatmeal",
            "calories": 150,
            "protein": 6.0,
            "carbs": 27.0,
            "fat": 3.0,
            "servingSize": "1 cup"
        },
        {
            "id": "550e8400-e29b-41d4-a716-446655440002",
            "name": "Banana",
            "calories": 105,
            "protein": 1.3,
            "carbs": 27.0,
            "fat": 0.4,
            "servingSize": "1 medium"
        }
    ]
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

### Common Error Responses

#### Authentication Error (401)
```json
{
    "error": true,
    "reason": "Invalid or expired authentication token"
}
```

#### Validation Error (400)
```json
{
    "error": true,
    "reason": "Invalid request parameters",
    "validationErrors": [
        "steps must be a positive number",
        "heartRate must be between 40 and 200"
    ]
}
```

#### Resource Not Found (404)
```json
{
    "error": true,
    "reason": "Requested resource not found"
}
```

#### Rate Limit Exceeded (429)
```json
{
    "error": true,
    "reason": "Rate limit exceeded. Try again in 60 seconds",
    "retryAfter": 60
}
```

## Rate Limiting

The API implements rate limiting of 100 requests per minute per user. Rate limit information is included in response headers:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1623456789
```

## Data Retention

- Metrics data is retained for 1 year
- Daily insights are retained for 90 days
- Meal logs are retained for 1 year

## Best Practices

1. Always include the Authorization header with a valid token
2. Use appropriate HTTP methods for different operations
3. Handle rate limiting by implementing exponential backoff
4. Implement proper error handling in your client application
5. Keep your authentication token secure
6. Cache responses when appropriate
7. Use compression for large requests/responses
8. Implement retry logic for failed requests
9. Monitor API usage and response times
10. Keep your client libraries up to date

## Development Setup

1. Install Swift and Vapor:
   ```bash
   brew install vapor
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/health-analytics.git
   cd health-analytics
   ```

3. Install dependencies:
   ```bash
   swift package resolve
   ```

4. Configure environment variables in `.env`:
   ```env
   JWT_SECRET=your-secret-key
   DATABASE_URL=your-database-url
   ENVIRONMENT=development
   PORT=8080
   LOG_LEVEL=debug
   ```

5. Run the server:
   ```bash
   swift run
   ```

## Testing

Run the test suite:
```bash
swift test
```

Run with coverage:
```bash
swift test --enable-code-coverage
```

## API Versioning

The API uses URL versioning. The current version is v1:
```http
https://api.example.com/v1/health/metrics
```

Future versions will be available at `/v2`, `/v3`, etc.

## Support

For API support, please email:
- Technical issues: api-support@example.com
- Account issues: account-support@example.com

## Rate Plans

| Plan | Requests/minute | Historical Data | Price |
|------|----------------|-----------------|--------|
| Basic | 100 | 30 days | Free |
| Pro | 1000 | 1 year | $29/month |
| Enterprise | Custom | Custom | Contact us | 