# 🗄️ Database Schema – Shipment Tracking Platform

## 📌 Overview

This database is designed to support a **microservices-based shipment tracking system** with:

* Business data (users, trucks, shipments)
* High-frequency tracking data (GPS logs)
* Optimized read performance for real-time tracking

The system uses **PostgreSQL** and follows a **write-optimized + read-optimized dual storage strategy**.

---

# 🧱 Tables

---

## 👤 users

Stores business users (transporters).

```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🧠 Notes:

* `UUID` ensures uniqueness across distributed systems
* `email` is unique for authentication
* Passwords are stored as hashes (never plain text)

---

## 🚚 trucks

Stores trucks registered by businesses.

```sql
CREATE TABLE trucks (
    truck_id TEXT PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    device_id TEXT UNIQUE NOT NULL,
    status TEXT DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🧠 Notes:

* Each truck is owned by a business (`user_id`)
* `device_id` maps to a GPS device (must be unique)
* Enables linking physical device → system

---

## 📦 shipments

Stores shipment details.

```sql
CREATE TABLE shipments (
    shipment_id TEXT PRIMARY KEY,
    truck_id TEXT REFERENCES trucks(truck_id),
    origin TEXT,
    destination TEXT,
    status TEXT DEFAULT 'CREATED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🧠 Notes:

* Core business entity
* Links shipment → truck
* Used by customers for tracking

---

## 📍 gps_logs (High Write Table)

Stores all historical GPS data.

```sql
CREATE TABLE gps_logs (
    id BIGSERIAL PRIMARY KEY,
    device_id TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🧠 Notes:

* High-frequency inserts (every few seconds per device)
* Can grow to millions of rows
* Used for historical analysis (not real-time queries)

---

## ⚡ latest_location (Optimized for Fast Reads)

Stores the latest location per device.

```sql
CREATE TABLE latest_location (
    device_id TEXT PRIMARY KEY,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    timestamp TIMESTAMP
);
```

### 🧠 Notes:

* Contains only the most recent location per device
* Enables **O(1) lookup for tracking API**
* Avoids expensive queries on `gps_logs`

---

# ⚡ Indexing Strategy

Indexes are critical for performance.

---

## 📍 gps_logs Indexes

```sql
CREATE INDEX idx_gps_device_id ON gps_logs(device_id);
CREATE INDEX idx_gps_timestamp ON gps_logs(timestamp);
```

### 🧠 Why:

* Fast lookup by device
* Efficient time-based queries

---

## 📦 shipments Index

```sql
CREATE INDEX idx_shipment_truck ON shipments(truck_id);
```

### 🧠 Why:

* Faster joins between shipment and truck

---

## 🚚 trucks Index

```sql
CREATE INDEX idx_truck_device ON trucks(device_id);
```

### 🧠 Why:

* Fast mapping from device → truck

---

# 🔄 Data Flow in Database

---

## 📍 GPS Ingestion Flow

1. Insert into `gps_logs` (historical storage)
2. Upsert into `latest_location` (fast access)

```sql
INSERT INTO latest_location (device_id, latitude, longitude, timestamp)
VALUES (...)
ON CONFLICT (device_id)
DO UPDATE SET
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude,
    timestamp = EXCLUDED.timestamp;
```

---

## 📡 Customer Tracking Flow

To fetch shipment location:

1. Get truck_id from shipment
2. Get device_id from truck
3. Fetch latest location

```sql
-- Step 1
SELECT truck_id FROM shipments WHERE shipment_id = ?;

-- Step 2
SELECT device_id FROM trucks WHERE truck_id = ?;

-- Step 3
SELECT * FROM latest_location WHERE device_id = ?;
```

---

# 🧠 Key Design Decisions

---

## 🔥 Dual Storage Strategy

* `gps_logs` → full history (write-heavy)
* `latest_location` → fast reads (read-heavy)

---

## 🔥 Separation of Concerns

* Business data and tracking data are separated
* Improves scalability and maintainability

---

## 🔥 Stateless Querying

* No session dependency
* Works efficiently in distributed systems

---

# 🚀 Future Improvements

---

## 📊 Table Partitioning

* Partition `gps_logs` by date
* Improves performance for large datasets

---

## ⏱️ Time-Series Optimization

* TimescaleDB

---

## ⚡ Caching Layer

* Redis for ultra-fast reads

---

# 🏁 Summary

This schema is designed to:

* Handle **high-frequency GPS ingestion**
* Provide **fast real-time tracking**
* Scale with increasing data volume

It reflects **production-grade backend and system design principles**.
