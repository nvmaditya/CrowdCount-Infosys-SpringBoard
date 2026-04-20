# People Detection Dashboard

A real-time people detection and counting dashboard with zone management, heatmaps, alerts, data export capabilities, **and comprehensive admin panel with role-based access control**.

## Features

-   **Real-time people counting** with YOLOv8 detection and tracking
-   **Zone-based monitoring** with customizable polygonal zones
-   **Live dashboard** with Bootstrap UI
-   **Interactive charts** showing zone distribution and count history
-   **Crowd density heatmap** with periodic updates
-   **Configurable alerts** when crowd thresholds are exceeded
-   **Data export** to CSV and PDF formats
-   **🔐 JWT-based authentication** with role-based access control (RBAC)
-   **👥 User management** with admin and user roles
-   **📹 Camera management** for multi-camera setups
-   **🗺️ Zone configuration** through admin panel
-   **📊 Activity logging** with comprehensive audit trails
-   **⚠️ Alert history tracking** for compliance and analysis

## Project Structure

```
├── backend/
│   ├── __init__.py
│   ├── api.py              # FastAPI server with all endpoints
│   ├── admin.py            # Admin endpoints (users, cameras, zones, logs)
│   ├── auth.py             # JWT authentication and user management
│   ├── middleware.py       # Auth middleware and role checking
│   ├── models.py           # Pydantic models for all entities
│   └── logging_service.py  # Activity logging system
├── frontend/
│   ├── index.html          # Main dashboard UI (Bootstrap + Chart.js)
│   ├── login.html          # Login page
│   ├── admin.html          # Admin panel UI
│   └── admin.js            # Admin panel JavaScript
├── detector/
│   ├── __init__.py
│   └── integrated_detector.py  # Detection with dashboard integration
├── data/                   # Configuration and data storage
│   ├── users.json          # User accounts (default: admin/admin123)
│   ├── config.json         # Camera and threshold configurations
│   ├── activity_logs.json  # Activity log entries
│   └── alerts_history.json # Alert occurrence records
├── shared_state.py         # Thread-safe shared state management
├── run_app.py              # Main entry point to run both services
├── requirements.txt        # Python dependencies
├── zones.json              # Zone configurations
└── yolov8n.pt             # YOLOv8 model weights
```

## Installation

1. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Ensure you have a video source:**
    - Place a video file (e.g., `Camera-Video.mp4`) in the project directory, or
    - Use webcam by specifying `--source 0`

## Quick Start

### Run Everything Together

```bash
python run_app.py
```

This starts both the API server and the detector. Open your browser to:

-   **Dashboard:** http://localhost:8000/static/index.html
-   **Login:** http://localhost:8000/static/login.html
-   **Admin Panel:** http://localhost:8000/static/admin.html (admin only)

**Default admin credentials:** `admin` / `admin123`

### Run Components Separately

**API Server only:**

```bash
python run_app.py --server-only
```

**Detector only:**

```bash
python run_app.py --detector-only
```

### Command Line Options

````bash
python run_app.py --help

Options:
  --source VIDEO    Video source (0 for webcam, or path to file)
  --model PATH      YOLOv8 model path (default: yolov8n.pt)
  --zones PATH      Zones configuration file (default: zones.json)
  --host HOST       API server host (default: 0.0.0.0)
  --port PORT       API server port (default: 8000)
  --no-display      Disable video display window
  --server-only     Run only the API server
  --detector-only   Run only the detector
### Public Endpoints

| Endpoint            | Method    | Description                        |
| ------------------- | --------- | ---------------------------------- |
| `/count`            | GET       | Current total people count         |
| `/zones`            | GET       | Zone-wise counts and visitor stats |
| `/history`          | GET       | Historical count data for charts   |
| `/heatmap`          | GET       | Crowd density heatmap (PNG image)  |
| `/alerts`           | GET       | Current alert status               |
| `/alerts/threshold` | POST      | Set alert thresholds               |
| `/export/csv`       | GET       | Download history as CSV            |
| `/export/pdf`       | GET       | Download summary as PDF            |
| `/summary`          | GET       | Complete state summary             |
| `/coordinates`      | GET       | Current person coordinates         |
| `/heatmap/reset`    | POST      | Reset heatmap accumulator          |
| `/ws`               | WebSocket | Real-time data streaming           |

### Authentication Endpoints

| Endpoint       | Method | Access | Description                |
| -------------- | ------ | ------ | -------------------------- |
| `/auth/login`  | POST   | Public | Login and get JWT token    |
| `/auth/logout` | POST   | Auth   | Logout (invalidate token)  |
| `/auth/me`     | GET    | Auth   | Get current user info      |

### Admin Endpoints (Admin Role Required)

| Endpoint                    | Method | Description                     |
| --------------------------- | ------ | ------------------------------- |
| `/admin/users`              | GET    | List all users                  |
| `/admin/users`              | POST   | Create new user                 |
| `/admin/users/{id}`         | DELETE | Delete user                     |
| `/admin/cameras`            | GET    | List cameras                    |
| `/admin/cameras`            | POST   | Add camera                      |
| `/admin/cameras/{id}`       | PUT    | Update camera                   |
| `/admin/cameras/{id}`       | DELETE | Delete camera                   |
| `/admin/zones`              | GET    | List zones                      |
| `

**Login (get JWT token):**

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
````

**Access admin endpoint:**

```bash
curl http://localhost:8000/admin/users \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Admin Panel Features

### 🔐 Authentication System

-   **JWT-based authentication** with secure token management
-   **Role-based access control (RBAC)**: Admin and User roles
-   **Password hashing** using bcrypt for security
-   **Token blacklisting** for logout functionality
-   **Session tracking** with last login timestamps

**Default credentials:**

-   Username: `admin`
-   Password: `admin123`
-   Role: `admin`

### 👥 User Management

-   Create, view, and delete user accounts
-   Assign roles (admin/user)
-   View user creation date and last login
-   Prevent self-deletion
-   Secure password hashing

### 📹 Camera Management

-   Add/remove camera sources
-   Configure camera properties:
    -   Name and description
    -   Source URL (file path, RTSP, webcam ID)
    -   Enable/disable status
-   Support for multiple cameras
-   Real-time enable/disable controls

### 🗺️ Zone Management

-   View all configured zones
-   Enable/disable zones dynamically
-   Set per-zone thresholds
-   Delete zones through UI
-   Zone creation via detector drawing mode

### ⚙️ Threshold Configuration

-   Set global alert threshold
-   Configure per-zone thresholds
-   Real-time threshold updates
-   Visual threshold indicators

### 📊 Activity Logging

-   Comprehensive audit trail of all actions
-   Log categories:
    -   **AUTH**: Login, logout, failed attempts
    -   **CONFIG**: Camera/zone/threshold changes
    -   **ALERT**: Threshold breaches
    -   **SYSTEM**: Detector start/stop, errors
-   Filter logs by:
    -   Category
    -   Date range
    -   User
    -   Action type
-   Export logs to CSV/PDF
-   Automatic log retention management (default: 30 days)

### ⚠️ Alert History

-   Track all threshold breach events
-   View alert timestamps and details
-   Filter by alert type (global/zone)
-   Export for compliance reporting/admin/zones`             | POST   | Create zone                     |
|`/admin/zones/{name}`      | PUT    | Update zone                     |
|`/admin/zones/{name}`      | DELETE | Delete zone                     |
|`/admin/config/thresholds` | GET    | Get thresholds                  |
|`/admin/config/thresholds` | PUT    | Update thresholds               |
|`/admin/logs`              | GET    | Query activity logs             |
|`/admin/logs/export/csv`   | GET    | Export logs as CSV              |
|`/admin/logs/export/pdf`   | GET    | Export logs as PDF              |
|`/admin/alerts/history`    | GET    | Get alert history               |
|`/summary`         | GET       | Complete state summary             |
|`/coordinates`     | GET       | Current person coordinates         |
|`/heatmap/reset`   | POST      | Reset heatmap accumulator          |
|`/ws` | WebSocket | Real-time data streaming |

### API Examples

**Get current count:**

```bash
curl http://localhost:8000/count
```

**Get zone statistics:**

```bash
curl http://localhost:8000/zones
```

**Set alert threshold:**

### Cannot access admin panel

-   Login with admin credentials (admin/admin123)
-   Check user role in browser console: `localStorage.getItem('user_role')`
-   Verify JWT token is present: `localStorage.getItem('auth_token')`

### 401 Unauthorized errors

-   Token may have expired (24 hour expiry)
-   Re-login to get a new token
-   Check Authorization header is being sent

## Security Notes

### For Production Deployment

**⚠️ IMPORTANT: Change these before production:**

1. **JWT Secret Key**: Set environment variable

    ```bash
    export JWT_SECRET_KEY="your-secure-random-key-here"
    ```

2. **Change default admin password**:

    - Login as admin
    - Create new admin user
    - Delete default admin account
    - Or manually edit `data/users.json`

3. **Enable HTTPS**:

    - Use reverse proxy (nginx/Apache)
    - Configure SSL certificates
    - Update CORS settings

4. **Database Migration**:

    - Replace JSON file storage with PostgreSQL/MySQL
    - Implement proper connection pooling
    - Add database migrations

5. **Additional Security**:

-   Production-ready authentication patterns
-   Industry-standard RBAC implementation
-   Comprehensive logging for security audits

For production use, consider:

-   Database persistence (PostgreSQL/MySQL)
-   Redis for session management
-   Message queue for event processing
-   Authentication for API (OAuth2/OIDC)
-   HTTPS/WSS for security
-   Load balancing for scale
-   Container orchestration (Docker/Kubernetes)
-   Monitoring and alerting (Prometheus/Grafana)

## API Authentication Flow

```
1. User submits credentials → /auth/login
2. Server validates credentials
3. Server generates JWT token (24h expiry)
4. Client stores token in localStorage
5. Client includes token in Authorization header
6. Server validates token on each request
7. Middleware checks user role for admin endpoints
8. User logs out → /auth/logout → token blacklisted
```

## Data Storage

All data is stored in JSON files for simplicity:

-   `data/users.json` - User accounts with hashed passwords
-   `data/config.json` - System configuration (cameras, thresholds)
-   `data/activity_logs.json` - Activity log entries
-   `data/alerts_history.json` - Alert occurrence records
-   `zones.json` - Zone polygon definitions

**Note**: For production, migrate to a proper database system.s

✅ Password hashing with bcrypt  
✅ JWT token authentication  
✅ Role-based access control  
✅ Token blacklisting for logout  
✅ Activity logging for audit trails  
✅ Input validation with Pydantic  
✅ CORS configuration

```bash
curl -X POST "http://localhost:8000/alerts/threshold?global_threshold=30"
```

## Dashboard Features

### Total Count Card

-   Displays current total people detected
-   Shows last update timestamp
-   Detection status indicator (running/stopped)

### Zone Cards

-   Individual cards for each defined zone
-   Shows current count and total unique visitors
-   Dynamically updates every second

### Bar Chart

-   Zone-wise distribution visualization
-   Color-coded bars for each zone
-   Updates in real-time

### Line Chart

-   People count over time
-   Shows last 60 data points
-   Smooth animated transitions

### Heatmap

-   Color-coded density visualization
-   Shows crowd accumulation patterns
-   Updates every 5 seconds
-   Can be reset via button

### Alert System

-   Configurable global threshold
-   Visual alert banner when threshold exceeded
-   Optional sound notification (toggleable)
-   Red pulsing animation for visibility

### Export Options

-   **CSV:** Timestamped count data with zone breakdown
-   **PDF:** Summary report with statistics and tables

## Detection Controls

When the detection window is active:

-   Press `q` to quit
-   Press `s` to save zones
-   Press `d` to toggle drawing mode
-   Press `c` to clear current zone
-   Press `z` to print zone statistics

### Drawing Zones

1. Press `d` to enter drawing mode
2. Left-click to add points
3. Right-click to finish zone
4. Press `s` to save zones to file

## Architecture Notes

### Thread-Safety

The `shared_state.py` module uses `threading.RLock` to ensure thread-safe access between:

-   The detector (running in main thread)
-   The API server (running in separate thread)

### Data Flow

1. Detector processes video frames
2. Detection results update `shared_state`
3. API endpoints read from `shared_state`
4. Dashboard polls API every 1 second

### Performance

-   Detection runs at video frame rate
-   Dashboard updates at ~1 second intervals
-   Heatmap updates every 5 seconds
-   History stores up to 3600 entries (1 hour)

## Assumptions & Design Decisions

1. **Polling over WebSocket:** While WebSocket is implemented, polling is used by default for reliability
2. **Video looping:** Video files loop continuously for demo purposes
3. **Simple alerts:** Rule-based threshold alerts (no ML)
4. **Memory limits:** History limited to 3600 entries to prevent memory issues
5. **Heatmap resolution:** Uses frame dimensions from video source

## Troubleshooting

### "Cannot open video source"

-   Ensure video file exists in project directory
-   For webcam, use `--source 0`

### Dashboard shows "Detection Stopped"

-   Make sure detector is running (`run_app.py` or `--detector-only`)
-   Check terminal for error messages

### Heatmap not showing

-   Heatmap generates after detection processes frames
-   Wait a few seconds after starting detection

### PDF export fails

-   Install reportlab: `pip install reportlab`

## Academic Notes

This project is designed for **academic milestone evaluation** with:

-   Clean, readable code structure
-   Minimal external dependencies
-   Well-documented assumptions
-   No over-engineering

For production use, consider:

-   Database persistence for history
-   Authentication for API
-   HTTPS/WSS for security
-   Load balancing for scale
