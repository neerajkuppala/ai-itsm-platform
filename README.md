# 🎫 AI-Powered ITSM Platform

A cloud-native, microservices-based IT Service Management platform built with Python, React, and AWS — similar to ServiceNow but built from scratch.

## 🚀 Live Demo
- Frontend: - Frontend: https://main.d1ntzsvf5xrdux.amplifyapp.com
- Auth Service: FastAPI + JWT
- Ticket Service: FastAPI + SQLite
- AI Service: Amazon Bedrock (Claude)
- Notification Service: AWS SQS

## 🏗️ Architecture

React Frontend (Port 3000)
        ↓
Auth Service (Port 8000) ←→ JWT Tokens
        ↓
Ticket Service (Port 8001) ←→ SQLite DB
        ↓
AI Service (Port 8002) ←→ Amazon Bedrock
        ↓
Notification Service (Port 8004) ←→ AWS SQS

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React.js, TypeScript |
| Backend | Python, FastAPI |
| Database | SQLite (dev), PostgreSQL (prod) |
| AI/ML | Amazon Bedrock (Claude) |
| Messaging | AWS SQS |
| Containers | Docker, Docker Compose |
| Cloud | AWS (ECR, VPC, ECS) |
| IaC | Terraform |
| CI/CD | GitHub Actions |
| Auth | JWT Tokens |

## 📦 Microservices

### 1. Auth Service (Port 8000)
- User registration and login
- JWT token generation and validation
- Password hashing with SHA256

### 2. Ticket Service (Port 8001)
- Create, read, update IT tickets
- Priority and status management
- JWT protected endpoints

### 3. AI Service (Port 8002)
- Auto-classifies ticket type (hardware/software/network)
- Suggests fixes using Amazon Bedrock (Claude)
- Severity detection (low/medium/high/critical)

### 4. Notification Service (Port 8004)
- Sends notifications via AWS SQS
- Triggered on ticket status changes
- Queue-based async messaging

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker and Docker Compose
- AWS Account
- Node.js 18+

### Run with Docker
git clone https://github.com/neerajkuppala/ai-itsm-platform
cd ai-itsm-platform
docker-compose up

### Run individually
cd services/auth-service
pip install fastapi uvicorn sqlalchemy passlib python-jose python-multipart
uvicorn main:app --port 8000

## 🏗️ Infrastructure (Terraform)
cd infrastructure/terraform
terraform init
terraform plan
terraform apply

Creates:
- VPC with public subnet
- Security groups
- ECR repositories for all services
- Internet Gateway

## 🔄 CI/CD Pipeline
GitHub Actions automatically:
1. Tests all 4 microservices on every push
2. Builds Docker images
3. Pushes to AWS ECR

## 📊 API Documentation
- Auth: http://localhost:8000/docs
- Tickets: http://localhost:8001/docs
- AI: http://localhost:8002/docs
- Notifications: http://localhost:8004/docs

## 👨‍💻 Author
Neeraj Kuppala
- GitHub: https://github.com/neerajkuppala
- Built as a portfolio project to demonstrate cloud-native microservices development