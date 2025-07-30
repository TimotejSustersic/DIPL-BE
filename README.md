# ⚡ System for Optimizing the Routes of Electric Personal Vehicles — Backend

## Project Description

This project is part of a diploma thesis focused on developing a navigation system for electric vehicles. The system considers the locations and availability of charging stations to calculate optimal routes. It also supports infrastructure planning across Slovenia by analyzing spatial data.

The backend provides a RESTful API that serves EV infrastructure data, performs route calculations based on real-time charging availability, and manages related analytics. It connects to a PostgreSQL database and is integrated with a [Next.js Frontend](https://github.com/TimotejSustersic/dipl-fe.git).

---

## 📁 Project Structure

```bash
/DIPL-BE
├── backend/                 # Django Settings
├── graphs/                  # Django Module for route optimization logic
│   ├── migrations/            # Folder with database migration files
│   ├── models/                # Folder with database entities
│   ├── tests/                 # Folder for testing scripts (TestingFactory.py)
│   ├── utils/                 # Folder for utiltity functions. This includes the real content
│   ├── views/                 # Folder for endpoints
│   └── routing.py             # API routing
├── requirements.txt         # Python dependencies
├── manage.py                # Django management script
└── .env                     # Environment variables
```

## 🔧 Tech Stack

| Layer           | Tech                                  |
|-----------------|----------------------------------------|
| Language        | Python 3.12                            |
| Framework       | [Django](https://www.djangoproject.com/) |
| Database        | [PostgreSQL](https://www.postgresql.org/) |
| API Layer       | Django Rest Framework     |
| Dev Tools       | Pandas, requests, Django Admin         |

## ⚙️ Setup & Installation

1. **Clone the repo**

```bash
git clone https://github.com/TimotejSustersic/DIPL-BE.git
```

2. **Set up virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up the database**

Make sure PostgreSQL server is running. Create the database, then configure `.env`:

```env
CLOUD_SQL_CONNECTION_NAME=localhost
DB_NAME=DIPL_DB
DB_USER=postgres
DB_PASSWORD=admin
```

Then run migrations:

```bash
python manage.py migrate
```

5. **Run the server**

```bash
python manage.py runserver
```

API will be accessible at `http://localhost:8000/`

## ⚙️ Functionality Overview

This backend simulates EV routing by dynamically calculating battery consumption and placing charging stops along the route. The core logic is built around geographic data, vehicle parameters, and consumption modeling. You find it in the graphs/util folder.

### 🔑 Key Functionalities

- **Vehicle Registration**
  - Logic: `vehicle.py -> ClassVehicle`
  - Features:
    - Registers EV data
    - Handles battery aging and capacity estimation

- **Route Planning**
  - Entry point: `RoutingFactory.start_route()`
  - Features:
    - Handles start and end point geocoding
    - Initiates routing pipeline via OSRM

- **Battery Consumption Modeling**
  - Logic: `BatteryConsumptionFactory`
  - Features:
    - Simulates usage based on:
      - Base consumption
      - Speed
      - Temperature
      - Elevation
    - Samples temperature and elevation every ~100 km

- **Route Consumption**
  - Logic: `RoutingFactory.new_route()`
  - Features:
    - Processes OSRM route step-by-step
    - Aggregates consumption over intervals
    - Triggers charging logic when battery drops

- **Charging Station Lookup**
  - Key methods:
    - `find_nearest_charging_stations()`
    - `find_next_charging_station()`
  - Features:
    - Uses external API to fetch nearby stations
    - Picks optimal station based on ETA
    - Plans detour and continues route recursively

- **Testing Module**
  - Logic: `test -> TestingFactory`
  - Features:
    - Uses existing routes to test consumption and charging logic
    - Creates combinations of input locations

- **Infrastructure Module**
  - Logic: `InfrastructureFactory`
  - Features:
    - Uses existing test instances to determine, which need additional charging stations
    - Reevaluates optimal charging station placement based on new data


## 📦 Deployment

The backend, built using **Django**, is containerized with **Docker** and hosted using Google Cloud services for maximum scalability and minimal infrastructure overhead.

### 🐳 Docker & Build

- The Django application is packaged into a **Docker container**.
- The container image is stored in **Google Container Registry (GCR)**.
- A `Dockerfile` defines all dependencies and includes a startup command to auto-run migrations:

```bash
python manage.py migrate
```

### ☁️ Hosting: Google Cloud Run

- The Docker image is deployed to Google Cloud Run, a fully managed, serverless platform.
- Cloud Run handles:
  - Automatic scaling based on request load.
  - Resource provisioning.
  - Cost optimization — billing is based on actual usage.

### 🛢️ Database: Google Cloud SQL

- Uses a PostgreSQL instance hosted on Google Cloud SQL.
- The connection between Cloud Run and Cloud SQL uses a secure internal instance connection — no public IP or proxy required.

### 🌐 API Gateway

- To enable secure communication from frontend to backend, an API Gateway is configured.
- Direct CORS requests are blocked by browser security policies, despite SSL.
- The solution involves:
  - Exporting the API schema from Swagger/OpenAPI to JSON, converting it to YAML, and deploying it to API Gateway.
  - The API Gateway:
    - Handles CORS headers.
    - Extends timeout configurations.
    - Provides a secure routing layer for all frontend-backend calls.

## 🌐 API Endpoints

Below is a categorized list of all available backend endpoints, hosted under `/api/` (assuming that your `urls.py` is included under an `/api/` root).

### 🚗 Vehicles

| Endpoint               | Description                             |
|------------------------|------------------------------------------|
| `/api/vehicles/new`    |  Register a new EV (battery, range, etc.) |
| `/api/vehicles/query`  |  Fetch data or status of a specific EV    |
| `/api/vehicles/discard`|   Delete or invalidate a vehicle entry     |

### 🧠 Routing Logic

| Endpoint                |  Description                             |
|-------------------------|-----------------------------------------|
| `/api/routing/new`      | Submit a new route request (start, end, constraints) |
| `/api/routing/query`    | Fetch previously computed routes         |

### 🧪 Testing & Evaluation

| Endpoint                         |  Description                                |
|----------------------------------|--------------------------------------------|
| `/api/tests/query`              | Fetch general test results                 |
| `/api/testing/items/query`      | Get list of test scenarios                 |
| `/api/testing/new`              | Submit new test instance                   |

### ⚡ Infrastructure

| Endpoint                             | Description                                |
|--------------------------------------|--------------------------------------------|
| `/api/infrastructure/query`         |  Fetch infrastructure summary               |
| `/api/infrastructure/items/query`   |  Get individual charger station entries     |
| `/api/infrastructure/new`           |  Add new infrastructure items (DEV only)    |

## 📚 References

- [OpenChargeMap API](https://openchargemap.org/site/develop/api)
- [EU EVSE datasets](https://data.europa.eu/data/datasets)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)

## 👨‍💻 Author

**Timotej Šušteršič**  

- [GitHub](https://github.com/TimotejSustersic/)

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.
