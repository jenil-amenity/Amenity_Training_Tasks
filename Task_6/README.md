# Django REST API – User Authentication & CRUD

## Features

* **JWT Authentication** (Access + Refresh Token)
* **User Registration** with validation
* **Login** with JWT token generation
* **Password Reset Flow**

  * Request reset token via email (console backend)
  * Confirm new password using token
* **Protected Routes** (e.g., delete account requires authentication)
* **User CRUD** operations

---

# API Endpoints

## Register User

**URL:** `POST /api/register/`

### Request Body

```json
{
  "username": "chandler",
  "email": "chandler@gmail.com",
  "password": "bing123"
}
```

### Success Response

```json
{
  "message": "User registered successfully",
  "username": "chandler",
  "email": "chandler@gmail.com"
}
```

---

## Login (JWT Authentication)

**URL:** `POST /api/login/`

### Request Body

```json
{
  "username": "chandler",
  "password": "chand123"
}
```

### Success Response

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDg1NDEzNSwiaWF0IjoxNzY0NzY3NzM1LCJqdGkiOiIzZWQ2M2RjMzA3YTE0YTA2YjY2MjRlYmE5YTkxYTA2NSIsInVzZXJfaWQiOiI2In0.Rs5xVRYx5_hXAsCk_7ySAHAzi2GhVF0_O_fIHXQWiG8",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0NzY3MzQ0LCJpYXQiOjE3NjQ3NjcwNDQsImp0aSI6IjU1NjhjYzAzZGI1YzQ5Zjg4YzQ2MjNmOWQ4ZjI1Njc3IiwidXNlcl9pZCI6IjYifQ.S4XWq5VmPxZeSDwURcgNI3e8SZ32oqsjoeqcHYC7vz0"
}
```

---

## Delete Account (Protected)

**URL:** `DELETE /api/delete_account/`

### Headers

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0NzY3MzQ0LCJpYXQiOjE3NjQ3NjcwNDQsImp0aSI6IjU1NjhjYzAzZGI1YzQ5Zjg4YzQ2MjNmOWQ4ZjI1Njc3IiwidXNlcl9pZCI6IjYifQ.S4XWq5VmPxZeSDwURcgNI3e8SZ32oqsjoeqcHYC7vz0
```

### Success Response

```json
{
  "message": "Account deleted successfully"
}
```

---

## 4️⃣ Request Password Reset

**URL:** `POST /api/reset_password/`

### Request Body

```json
{
  "email": "chandler@gmail.com"
}
```

### Success Response

```json
{
  "status": "ok"
}
```

in db access the token from admin panel or console output

```
http://127.0.0.1:8000/api/reset_password/confirm
```

---

## 5️⃣ Reset Password Confirm

**URL:** `POST /api/reset_password/confirm/`

### Request Body

```json
{
  "uid": "encoded_uid_here",
  "token": "dee3d176cbd56d881de1945e5d",
  "new_password": "bing@123"
}
```

### Success Response

```json
{
  "message": "Password reset successful"
}
```

