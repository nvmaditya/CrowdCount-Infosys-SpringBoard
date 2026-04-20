# Admin Panel Quick Reference

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start application
python run_app.py

# 3. Access admin panel
# URL: http://localhost:8000/static/login.html
# User: admin
# Pass: admin123
```

## 🔑 Default Credentials

| Username | Password | Role  |
| -------- | -------- | ----- |
| admin    | admin123 | admin |

⚠️ **Change immediately in production!**

## 📍 URLs

-   **Login**: http://localhost:8000/static/login.html
-   **Admin Panel**: http://localhost:8000/static/admin.html
-   **Dashboard**: http://localhost:8000/static/index.html
-   **API Docs**: http://localhost:8000/docs

## 🎯 Key Features

### Authentication

✅ JWT-based with 24-hour expiry  
✅ Role-based access (admin/user)  
✅ Secure password hashing (bcrypt)  
✅ Token blacklisting for logout

### User Management

-   Create/delete users
-   Assign roles
-   View login history

### Camera Management

-   Add/remove cameras
-   Configure sources (webcam/RTSP/file)
-   Enable/disable cameras

### Zone Management

-   View/edit zones
-   Set per-zone thresholds
-   Enable/disable zones

### Activity Logging

-   Filter by category/date
-   Export to CSV/PDF
-   Auto-cleanup (30 days)

### Thresholds

-   Global alert threshold
-   Per-zone thresholds
-   Real-time updates

## 🔐 API Authentication

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Use Token

```bash
TOKEN="your-token-here"
curl http://localhost:8000/admin/users \
  -H "Authorization: Bearer $TOKEN"
```

### Logout

```bash
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer $TOKEN"
```

## 📊 Activity Log Categories

| Category | Actions                        |
| -------- | ------------------------------ |
| AUTH     | Login, logout, failed attempts |
| CONFIG   | Camera/zone/threshold changes  |
| ALERT    | Threshold breaches             |
| SYSTEM   | Detector start/stop, errors    |

## 🛠️ Common Tasks

### Add User

```bash
curl -X POST http://localhost:8000/admin/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123","role":"user"}'
```

### Add Camera

```bash
curl -X POST http://localhost:8000/admin/cameras \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Cam1","source_url":"0","enabled":true}'
```

### Update Thresholds

```bash
curl -X PUT http://localhost:8000/admin/config/thresholds \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"global_threshold":30}'
```

### Query Logs

```bash
# Last 100 logs
curl http://localhost:8000/admin/logs?limit=100 \
  -H "Authorization: Bearer $TOKEN"

# AUTH logs only
curl "http://localhost:8000/admin/logs?category=AUTH" \
  -H "Authorization: Bearer $TOKEN"

# Date range
curl "http://localhost:8000/admin/logs?start_date=2024-01-01T00:00:00" \
  -H "Authorization: Bearer $TOKEN"
```

## 🐛 Troubleshooting

| Issue             | Solution                                     |
| ----------------- | -------------------------------------------- |
| Cannot login      | Check credentials, verify API running        |
| 401 errors        | Token expired, re-login                      |
| Admin panel blank | Check browser console, verify admin.js loads |
| Logs not saving   | Check data/ folder permissions               |

## 🔒 Security Checklist

-   [ ] Change default admin password
-   [ ] Set JWT_SECRET_KEY environment variable
-   [ ] Enable HTTPS in production
-   [ ] Regular password rotation
-   [ ] Monitor failed login attempts
-   [ ] Review activity logs weekly
-   [ ] Backup data/ folder regularly

## 📁 File Locations

```
data/users.json          # User accounts
data/config.json         # System configuration
data/activity_logs.json  # Activity logs
data/alerts_history.json # Alert history
zones.json               # Zone definitions
```

## 🎨 Admin Panel Sections

| Section    | Purpose                    |
| ---------- | -------------------------- |
| Dashboard  | Overview & recent activity |
| Users      | User management            |
| Cameras    | Camera configuration       |
| Zones      | Zone management            |
| Thresholds | Alert configuration        |
| Logs       | Activity logs & export     |
| Alerts     | Alert history              |

## 🆘 Emergency Commands

```bash
# Reset to default admin (if locked out)
# Edit data/users.json and ensure this entry exists:
{
  "id": "admin-default-001",
  "username": "admin",
  "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X.BoS/flUQ3xoGZvu",
  "role": "admin",
  "created_at": "2024-01-01T00:00:00"
}

# Clear all tokens (force all users to re-login)
# Restart the server

# View raw logs
cat data/activity_logs.json | python -m json.tool

# Backup configuration
cp -r data/ data_backup_$(date +%Y%m%d)
```

## 📞 Support

See ADMIN_SETUP.md for detailed documentation.
