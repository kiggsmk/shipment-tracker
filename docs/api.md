# 📡 API Design – Shipment Tracking Platform

## 🔐 Authentication Service

---

### 🔹 POST /auth/signup

**Description:** Register a new business user

**Request:**

```json
{
  "email": "business@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "message": "User created successfully",
  "user_id": "USER123"
}
```

---

### 🔹 POST /auth/login

**Description:** Authenticate user and return JWT token

**Request:**

```json
{
  "email": "business@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "access_token": "jwt_token_here",
  "token_type": "Bearer"
}
```

---

### 🔹 GET /auth/validate

**Description:** Validate JWT token

**Headers:**

```
Authorization: Bearer <token>
```

**Response:**

```json
{
  "valid": true,
  "user_id": "USER123"
}
```

---

# 🚚 Truck Service

---

### 🔹 POST /trucks

**Description:** Register a new truck

**Headers:**

```
Authorization: Bearer <token>
```

**Request:**

```json
{
  "truck_id": "TRUCK123",
  "device_id": "GPS789"
}
```

**Response:**

```json
{
  "message": "Truck registered successfully",
  "truck_id": "TRUCK123"
}
```

---

### 🔹 GET /trucks

**Description:** Get all trucks for a business

**Headers:**

```
Authorization: Bearer <token>
```

**Response:**

```json
[
  {
    "truck_id": "TRUCK123",
    "device_id": "GPS789",
    "status": "ACTIVE"
  }
]
```

---

### 🔹 GET /trucks/{truck_id}

**Description:** Get details of a specific truck

**Response:**

```json
{
  "truck_id": "TRUCK123",
  "device_id": "GPS789",
  "status": "ACTIVE"
}
```

---

# 📦 Shipment Service

---

### 🔹 POST /shipments

**Description:** Create a new shipment

**Headers:**

```
Authorization: Bearer <token>
```

**Request:**

```json
{
  "truck_id": "TRUCK123",
  "origin": "Bangalore",
  "destination": "Mumbai"
}
```

**Response:**

```json
{
  "shipment_id": "SHIP123",
  "status": "CREATED"
}
```

---

### 🔹 GET /shipments/{shipment_id}

**Description:** Get shipment details

**Response:**

```json
{
  "shipment_id": "SHIP123",
  "truck_id": "TRUCK123",
  "origin": "Bangalore",
  "destination": "Mumbai",
  "status": "IN_TRANSIT"
}
```

---

### 🔹 GET /shipments

**Description:** Get all shipments for a business

**Headers:**

```
Authorization: Bearer <token>
```

**Response:**

```json
[
  {
    "shipment_id": "SHIP123",
    "truck_id": "TRUCK123",
    "origin": "Bangalore",
    "destination": "Mumbai",
    "status": "IN_TRANSIT"
  }
]
```

---

# 📍 Tracking Service

---

### 🔹 POST /tracking/location

**Description:** Ingest GPS location from device (simulated)

**Request:**

```json
{
  "device_id": "GPS789",
  "latitude": 12.9716,
  "longitude": 77.5946
}
```

**Response:**

```json
{
  "message": "Location updated successfully"
}
```

---

### 🔹 GET /tracking/{shipment_id}

**Description:** Get latest location of a shipment

**Response:**

```json
{
  "shipment_id": "SHIP123",
  "truck_id": "TRUCK123",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "timestamp": "2026-04-01T10:00:00Z"
}
```

---

# 🧪 Health Check (All Services)

---

### 🔹 GET /health

**Description:** Check if service is running

**Response:**

```json
{
  "status": "ok"
}
```

---
