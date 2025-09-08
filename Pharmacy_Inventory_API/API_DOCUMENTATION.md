# API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
   - [Authentication](#authentication-1)
   - [Medicines](#medicines)
   - [Suppliers](#suppliers)
   - [Inventory Logs](#inventory-logs)
   - [Alerts](#alerts)
3. [Pagination](#pagination)
4. [Filtering](#filtering)
5. [Searching](#searching)
6. [Sorting](#sorting)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)

## Authentication

All API endpoints require authentication using JWT (JSON Web Tokens).

### Obtaining a Token

```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### Using the Token
Include the token in the `Authorization` header:

```
Authorization: Bearer your.jwt.token.here
```

### Refreshing Token

```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

## Endpoints

### Authentication

#### Login
- **URL**: `/api/token/`
- **Method**: `POST`
- **Body**: 
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response**:
  ```json
  {
      "refresh": "string",
      "access": "string"
  }
  ```

### Medicines

#### List All Medicines
- **URL**: `/api/medicines/`
- **Method**: `GET`
- **Query Parameters**:
  - `search` (string): Search by name or description
  - `category` (string): Filter by category
  - `stock_status` (string): 'low' or 'adequate'
  - `expiry_status` (string): 'expired' or 'not_expired'
  - `page` (int): Page number
  - `page_size` (int): Items per page

#### Create Medicine
- **URL**: `/api/medicines/`
- **Method**: `POST`
- **Body**: 
  ```json
  {
      "name": "string",
      "description": "string",
      "category": "string",
      "quantity": 0,
      "dosage": "string",
      "expiry_date": "2025-12-31",
      "threshold_alert": 10,
      "supplier": 1,
      "batch_number": "string",
      "manufacturer": "string",
      "price": "0.00",
      "is_active": true
  }
  ```

### Suppliers

#### List All Suppliers
- **URL**: `/api/suppliers/`
- **Method**: `GET`
- **Query Parameters**:
  - `search` (string): Search by name, contact person, or email
  - `page` (int): Page number
  - `page_size` (int): Items per page

### Inventory Logs

#### List All Logs
- **URL**: `/api/inventory-logs/`
- **Method**: `GET`
- **Query Parameters**:
  - `action` (string): Filter by action type
  - `medicine` (int): Filter by medicine ID
  - `performed_by` (int): Filter by user ID
  - `start_date` (date): Filter by start date (YYYY-MM-DD)
  - `end_date` (date): Filter by end date (YYYY-MM-DD)

### Alerts

#### Expiry Alerts
- **URL**: `/api/medicines/expiry-alerts/`
- **Method**: `GET`
- **Query Parameters**:
  - `days` (int): Number of days to check for expiry (default: 30)

#### Low Stock Alerts
- **URL**: `/api/medicines/low-stock/`
- **Method**: `GET`

## Pagination

All list endpoints support pagination. The response includes:

```json
{
    "count": 123,
    "next": "http://api.example.org/endpoint/?page=2",
    "previous": null,
    "results": [
        // items
    ]
}
```

## Filtering

Most list endpoints support filtering by model fields. For example:

```
GET /api/medicines/?category=antibiotic&is_active=true
```

## Searching

Endpoints with search support can be queried using the `search` parameter:

```
GET /api/medicines/?search=aspirin
```

## Sorting

Most list endpoints support sorting by using the `ordering` parameter:

```
GET /api/medicines/?ordering=name,-expiry_date
```

## Error Handling

### Common Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
    "status": "error",
    "code": "error_code",
    "message": "Human-readable error message",
    "details": {
        // Additional error details
    }
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage. By default:
- 1000 requests per day
- 100 requests per hour
- 20 requests per minute

If you exceed these limits, you'll receive a `429 Too Many Requests` response.
