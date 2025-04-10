# personal-budget-manager

A robust backend system for managing and tracking expenses, developed using **Flask**, **MySQL**, and **SQLAlchemy**. This API includes integrated testing capabilities and Docker-based deployment support.

---

##  Key Features

- User registration and management
- Category-wise and monthly budgeting
- Expense tracking and categorization
- Automatic monthly expenditure summaries
- Budget usage notifications (at or above 90%)
- Group-based expense sharing and settlement functionality
- Optional email notifications
- HTML-based test UI interface
- Full Docker integration for seamless deployment

---

## 🛠️ How to Run the Application

### ▶️ Method 1: Running Locally

#### 1. Clone the repository and initialize a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
```

#### 2. Install required Python packages:

```bash
pip install -r requirements.txt
```

#### 3. Configure environment variables:

Create a `.env` file in the root directory with the following content:

```env
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_NAME=expense_db
```

#### 4. Create the MySQL database manually (skip if using Docker):

```sql
CREATE DATABASE expense_db;
```

#### 5. Launch the application:

```bash
python -m app.main
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

#### 6. Optional: Run the HTML-based testing interface:

```bash
python -m http.server 8000
```

Then visit: [http://localhost:8000/test.html](http://localhost:8000/test.html)

---

### 🐳 Method 2: Using Docker

#### 1. Start services using Docker Compose:

```bash
docker-compose up --build
```

#### 2. Access the API at:

[http://localhost:5000](http://localhost:5000)

#### 3. Default MySQL credentials:

- Port: `3306`
- Username: `root`
- Password: `root`
- Database: `expense_db`

---

## 🧪 Testing the API

### 🧷 Example CURL Commands

#### ➕ Create a New User

```bash
curl -X POST http://localhost:5000/user \
     -H "Content-Type: application/json" \
     -d '{"name": "bardawal", "email": "bardawal@gmail.com"}'
```

#### 💰 Set Budget for a Category

```bash
curl -X POST http://localhost:5000/budget \
     -H "Content-Type: application/json" \
     -d '{"user_id": 100, "category": "Food", "month": "2024-01", "limit": 1000}'
```

#### 🧾 Add an Expense

```bash
curl -X POST http://localhost:5000/expense \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "category": "Food", "amount": 3450}'
```

#### 📊 Generate Monthly Report

```bash
curl http://localhost:5000/report/1/2024-01
```

#### 🚨 Check Budget Alerts

```bash
curl http://localhost:5000/alerts/1/2024-01
```

Alternatively, interact via the provided HTML test interface.

---

## 📘 SQL and ORM Overview

- Utilizes `SQLAlchemy` for all database models
- Leverages ORM methods: `db.session.query`, `.filter_by()`, `.group_by()`
- Aggregations like `get_monthly_spending()` use `func.sum()` for summaries

---

## 🗒️ Code Documentation

- Routes include descriptive inline comments
- Helper functions such as `check_alerts` are thoroughly documented
- Clean, modular code structure spread across: `routes.py`, `utils.py`, `models.py`

---

## 🐋 Docker Configuration

### 📄 `Dockerfile`

```Dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "app.main"]
```

### 📄 `docker-compose.yml`

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      - DB_USER=root
      - DB_PASSWORD=root
      - DB_HOST=db
      - DB_NAME=expense_db

  db:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: expense_db
    volumes:
      - mysqldata:/var/lib/mysql

volumes:
  mysqldata:
```

---

All core functionalities implemented. Ready for deployment or submission. 🎯
Need help with GitHub or deployment? Just ask!

