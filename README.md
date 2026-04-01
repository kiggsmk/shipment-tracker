# 🚚 Shipment Tracking & Visibility Platform

## 📌 Overview

This project is a **production-grade microservices platform** designed to provide **real-time shipment visibility** for logistics businesses and their customers.

It enables:

* Businesses to manage trucks and shipments
* GPS devices to stream live location data
* Customers to track shipments using a unique shipment ID

The system is built with a strong focus on **scalability, observability, and cloud-native architecture**.

---

## 🎯 Problem Statement

Logistics businesses often lack a simple and scalable way to provide **real-time shipment tracking** to their customers.

Existing systems are either:

* Too complex to integrate
* Not scalable for high-frequency GPS data
* Lacking transparency for end users

---

## 💡 Solution

This platform provides:

* A **centralized system** to manage trucks and shipments
* A **tracking pipeline** to ingest GPS data from devices
* A **customer-facing interface** for shipment tracking

Each shipment is mapped to a truck, and each truck is associated with a GPS device.
The system continuously processes location updates and exposes them via APIs.

---

## 👥 User Roles

### 🏢 Business (Transporters)

* Register trucks
* Assign GPS devices
* Create and manage shipments

### 👤 Customer

* Track shipment using a unique `shipment_id`
* View real-time location updates

---

## 🧱 System Architecture

### 🔹 Frontend

* Next.js (React)
* Business dashboard + Customer tracking page

### 🔹 Backend (Microservices)

* Auth Service
* Truck Service
* Shipment Service
* Tracking Service
* Analytics Service 

### 🔹 Infrastructure

* Kubernetes (EKS / AKS)
* Docker (containerization)
* Helm (deployment templating)
* Terraform (infrastructure as code)

### 🔹 Observability

* Prometheus (metrics)
* Grafana (dashboards)

---

## 🔄 Core System Flows

### 1. Truck Registration

* Business registers a truck with a `device_id`

### 2. Shipment Creation

* Shipment is created and mapped to a truck
* A unique `shipment_id` is generated

### 3. GPS Data Ingestion

* GPS device sends location data periodically
* Tracking service maps:

  ```
  device_id → truck → shipment
  ```
* Latest location is stored

### 4. Customer Tracking

* Customer accesses:

  ```
  /track/{shipment_id}
  ```
* System returns the latest location

---

## 🧮 Data Model 

### trucks

* truck_id
* device_id

### shipments

* shipment_id
* truck_id
* origin
* destination

### gps_logs

* device_id
* latitude
* longitude
* timestamp

### latest_location

* device_id
* latitude
* longitude
* timestamp

---

## ⚙️ Tech Stack

| Layer            | Technology                    |
| ---------------- | ----------------------------- |
| Frontend         | Next.js, Tailwind CSS         |
| Backend          | FastAPI                       |
| Database         | PostgreSQL                    |
| Containerization | Docker                        |
| Orchestration    | Kubernetes                    |
| IaC              | Terraform                     |
| CI/CD            | GitHub Actions                |
| Monitoring       | Prometheus + Grafana          |

---

## 🚀 MVP Scope

* Business can register trucks
* Business can create shipments
* GPS simulator sends location data
* Customer can track shipment
* Basic UI with live updates (polling)

---

## 📁 Project Structure

```
project-root/
├── frontend/
├── services/
│   ├── auth-service/
│   ├── truck-service/
│   ├── shipment-service/
│   ├── tracking-service/
│   ├── analytics-service/
├── infra/
│   ├── terraform/
│   ├── k8s/
│   ├── helm/
├── docs/
├── docker-compose.yml
└── README.md
```

---

## 🧠 Key Architectural Decisions

* Microservices for scalability and separation of concerns
* Dedicated tracking service for high-throughput ingestion
* Use of `latest_location` table for fast reads
* Stateless services for Kubernetes-based scaling

---

## 🔮 Future Enhancements

* Event-driven architecture (Kafka / RabbitMQ)
* Real-time updates via WebSockets
* Redis caching layer
* Route optimization and predictive analytics
* Alerting system for delays and anomalies

---

## 🏁 Summary

This project demonstrates:

* Real-world microservices architecture
* High-frequency data ingestion systems
* Cloud-native deployment practices
* End-to-end DevOps pipeline implementation

It is designed as a **production-ready system**, not just a demo application.
