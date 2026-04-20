# Admin Panel Setup Guide

Complete guide to setting up and using the Admin Panel for the People Detection Dashboard.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

New dependencies added:

-   `python-jose[cryptography]` - JWT token generation and validation
-   `passlib[bcrypt]` - Secure password hashing

### 2. Start the Application

```bash
python run_app.py
```

This starts both the detection system and the API server with admin endpoints.

### 3. Access the Admin Panel

1. Open browser to: http://localhost:8000/static/login.html
2. Login with default credentials:
    - **Username**: `admin`
    - **Password**: `admin123`
3. You'll be redirected to: http://localhost:8000/static/admin.html

## Default Accounts

The system comes with one default admin account:

| Username | Password | Role  |
| -------- | -------- | ----- |
| admin    | admin123 | admin |

**⚠️ IMPORTANT**: Change the default password immediately after first login!

## User Roles

### Admin Role

Full access to:

-   User management (create/delete users)
-   Camera configuration
-   Zone management
-   Threshold settings
-   Activity logs
-   Alert history
-   System configuration

### User Role

Access to:

-   View dashboard
-   View zones
-   View current counts
-   Export reports (CSV/PDF)

**Note**: Currently only admin role is fully implemented. User role is prepared for future expansion.

## Admin Panel Features

### Dashboard Overview

The admin dashboard provides:

-   Total user count
-   Number of configured cameras
-   Number of zones
-   Recent activity log entries

### User Management

**Create New User**:

1. Navigate to "User Management"
2. Click "Add User" button
3. Fill in:
    - Username (3-50 characters)
    - Password (minimum 6 characters)
    - Role (user/admin)
4. Click "Add User"

**Delete User**:

1. Find user in the table
2. Click trash icon
3. Confirm deletion

-   Cannot delete your own account

### Camera Management

**Add Camera**:

1. Navigate to "Cameras"
2. Click "Add Camera"
3. Configure:
    - **Name**: Descriptive name (e.g., "Entrance Camera")
    - **Source URL**:
        - Webcam: `0`, `1`, `2`, etc.
        - RTSP stream: `rtsp://username:password@ip:port/stream`
        - Video file: `path/to/video.mp4`
    - **Enabled**: Check to enable immediately
4. Click "Add Camera"

**Manage Cameras**:

-   **Enable/Disable**: Click play/pause icon
-   **Delete**: Click trash icon

### Zone Management

Zones are primarily managed through the detector drawing interface:

**Via Detector**:

1. Run detector application
2. Press `d` to enter drawing mode
3. Left-click to add polygon points
4. Right-click to finish zone
5. Press `s` to save to zones.json

**Via Admin Panel**:

-   View all zones
-   Enable/disable zones
-   Delete zones
-   Set zone-specific thresholds

### Threshold Configuration

**Global Threshold**:

-   Sets the maximum total people count before alert
-   Default: 50
-   Updates immediately when saved

**Zone Thresholds**:

-   Set per-zone maximum counts
-   Optional (leave empty for no zone-specific threshold)
-   Overrides global threshold for specific zones

### Activity Logs

All system actions are logged:

**Log Categories**:

-   **AUTH**: Login, logout, failed attempts
-   **CONFIG**: Configuration changes
-   **ALERT**: Threshold breaches
-   **SYSTEM**: System events

**Filtering**:

1. Select category from dropdown
2. Choose date range
3. Click filter
4. Results update automatically

**Export**:

-   CSV: Includes all fields, suitable for analysis
-   PDF: Formatted report for documentation

**Log Retention**:

-   Default: 30 days
-   Configurable in admin settings
-   Old logs automatically cleaned up

### Alert History

Tracks all threshold breach events:

-   Timestamp of alert
-   Alert type (global/zone-specific)
-   Threshold value
-   Actual count that triggered alert
-   Acknowledgment status

## API Usage

### Authentication

**Login**:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Response:

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 86400,
    "user": {
        "id": "admin-default-001",
        "username": "admin",
        "role": "admin",
        "created_at": "2024-01-01T00:00:00",
        "last_login": "2024-01-01T10:30:00"
    }
}
```

**Using Token**:

```bash
TOKEN="your-jwt-token-here"

# List all users
curl http://localhost:8000/admin/users \
  -H "Authorization: Bearer $TOKEN"

# Add camera
curl -X POST http://localhost:8000/admin/cameras \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Main Entrance",
    "source_url": "rtsp://camera.local/stream",
    "enabled": true
  }'
```

**Logout**:

```bash
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer $TOKEN"
```

### Common Admin Operations

**Create User**:

```bash
curl -X POST http://localhost:8000/admin/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "operator1",
    "password": "secure123",
    "role": "user"
  }'
```

**Update Thresholds**:

```bash
curl -X PUT http://localhost:8000/admin/config/thresholds \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "global_threshold": 30,
    "zone_thresholds": {
      "Zone_1": 15,
      "Zone_2": 20
    }
  }'
```

**Query Logs**:

```bash
# All logs
curl http://localhost:8000/admin/logs?limit=100 \
  -H "Authorization: Bearer $TOKEN"

# Filter by category
curl "http://localhost:8000/admin/logs?category=AUTH&limit=50" \
  -H "Authorization: Bearer $TOKEN"

# Date range
curl "http://localhost:8000/admin/logs?start_date=2024-01-01T00:00:00&end_date=2024-01-31T23:59:59" \
  -H "Authorization: Bearer $TOKEN"
```

## Security Best Practices

### Immediate Actions

1. **Change Default Password**:

    ```bash
    # Via admin panel or API
    curl -X POST http://localhost:8000/admin/users \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "username": "myadmin",
        "password": "VerySecurePassword123!",
        "role": "admin"
      }'
    # Then delete default admin account
    ```

2. **Set JWT Secret**:

    ```bash
    # Linux/Mac
    export JWT_SECRET_KEY="your-random-secret-key-at-least-32-chars"

    # Windows
    set JWT_SECRET_KEY=your-random-secret-key-at-least-32-chars
    ```

3. **Review Logs Regularly**:
    - Check for failed login attempts
    - Monitor configuration changes
    - Track unusual activity

### Production Recommendations

1. **Use HTTPS**:

    - Deploy behind nginx/Apache with SSL
    - Configure SSL certificates (Let's Encrypt)
    - Redirect HTTP to HTTPS

2. **Database Migration**:

    - Replace JSON files with PostgreSQL/MySQL
    - Implement connection pooling
    - Add database backups

3. **Enhanced Security**:

    - Implement rate limiting (10 requests/minute on login)
    - Add CAPTCHA for login page
    - Set password complexity requirements
    - Enable two-factor authentication (2FA)
    - Implement token refresh mechanism
    - Add account lockout after 5 failed attempts

4. **Monitoring**:

    - Set up log aggregation (ELK stack)
    - Configure alerts for suspicious activity
    - Monitor API response times
    - Track failed authentication attempts

5. **Backup Strategy**:
    - Regular backups of user database
    - Backup configuration files
    - Store backups securely off-site
    - Test restore procedures

## Troubleshooting

### Cannot Login

**Symptoms**: 401 Unauthorized or Invalid credentials

**Solutions**:

1. Verify credentials (default: admin/admin123)
2. Check `data/users.json` exists
3. Verify API server is running
4. Clear browser localStorage: `localStorage.clear()`
5. Check browser console for errors

### Token Expired

**Symptoms**: 401 Unauthorized after being logged in

**Solutions**:

1. Tokens expire after 24 hours
2. Simply log in again
3. Implement token refresh in production

### Admin Panel Not Loading

**Symptoms**: Blank page or JavaScript errors

**Solutions**:

1. Check browser console for errors
2. Verify `admin.js` is loading
3. Clear browser cache
4. Check API server is accessible
5. Verify CORS settings

### Database/JSON File Errors

**Symptoms**: Cannot save users/cameras/logs

**Solutions**:

1. Check `data/` directory exists and is writable
2. Verify JSON files are valid (use JSON validator)
3. Check file permissions
4. Look for file locks (close other editors)

### Activity Logs Not Recording

**Symptoms**: Empty logs section

**Solutions**:

1. Check `data/activity_logs.json` exists
2. Verify write permissions on data directory
3. Check for disk space
4. Review backend logs for errors

## File Structure Reference

```
data/
├── users.json           # User accounts
│   └── Structure: {"users": [{"id", "username", "password_hash", "role", ...}]}
├── config.json          # System config
│   └── Structure: {"cameras": [...], "thresholds": {...}, "log_retention_days": 30}
├── activity_logs.json   # Activity logs
│   └── Structure: {"logs": [{"id", "timestamp", "category", "action", ...}]}
└── alerts_history.json  # Alert records
    └── Structure: {"alerts": [{"id", "timestamp", "alert_type", ...}]}
```

## Common Admin Tasks

### Daily Tasks

-   Review dashboard overview
-   Check recent activity logs
-   Monitor alert history
-   Verify all cameras operational

### Weekly Tasks

-   Review and acknowledge alerts
-   Check system thresholds
-   Export logs for archival
-   Verify zone configurations

### Monthly Tasks

-   Clean up old logs (automatic)
-   Review user access logs
-   Update camera configurations
-   Backup configuration files
-   Change admin password

### As Needed

-   Add/remove users
-   Add/remove cameras
-   Adjust thresholds
-   Create/delete zones
-   Export reports for compliance

## Support and Maintenance

### Regular Maintenance

1. **Log Cleanup**: Automatic (30-day retention)
2. **Token Cleanup**: Automatic on logout
3. **Database Optimization**: Manual (compact JSON files if large)

### Health Checks

```bash
# Check API health
curl http://localhost:8000/

# Check authentication
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Check detection status
curl http://localhost:8000/count
```

### Performance Tips

1. Limit log queries to specific date ranges
2. Export and archive old logs periodically
3. Monitor JSON file sizes
4. Use appropriate video resolutions for cameras
5. Adjust detection frame rates if needed

## Additional Resources

-   Main Dashboard: http://localhost:8000/static/index.html
-   API Documentation: http://localhost:8000/docs (FastAPI auto-docs)
-   API Alternative Docs: http://localhost:8000/redoc

## Contact and Support

For issues or questions:

1. Check this guide first
2. Review README_DASHBOARD.md
3. Check console logs (browser and terminal)
4. Review activity logs for clues
5. Check GitHub issues (if applicable)

---

**Last Updated**: January 2024  
**Version**: 1.0.0
