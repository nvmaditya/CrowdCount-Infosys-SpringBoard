# Installation & Testing Guide

## Step-by-Step Setup

### 1. Install New Dependencies

The admin panel requires two additional packages:

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

Or install all dependencies at once:

```bash
pip install -r requirements.txt
```

**Verify installation:**

```bash
python -c "from jose import jwt; from passlib.context import CryptContext; print('✓ Dependencies installed successfully')"
```

### 2. Verify File Structure

Ensure all files are in place:

```bash
# Check backend files
ls backend/auth.py
ls backend/middleware.py
ls backend/models.py
ls backend/admin.py
ls backend/logging_service.py

# Check frontend files
ls frontend/login.html
ls frontend/admin.html
ls frontend/admin.js

# Check data directory exists
ls data/
```

### 3. Start the Application

```bash
python run_app.py
```

Expected output:

```
Created default admin user: admin / admin123
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Test the System

#### Test 1: Main Dashboard (No Auth Required)

```bash
# Open browser to:
http://localhost:8000/static/index.html

# Should show:
# - People count dashboard
# - Zone statistics
# - Charts
# - Login button in nav bar
```

#### Test 2: Login Page

```bash
# Open browser to:
http://localhost:8000/static/login.html

# Actions:
# 1. Enter: admin / admin123
# 2. Click Login
# 3. Should redirect to admin panel
```

#### Test 3: Admin Panel

```bash
# URL: http://localhost:8000/static/admin.html

# Should show:
# - Dashboard with stats
# - Sidebar with 7 sections
# - Username in sidebar
# - All sections clickable
```

#### Test 4: API Authentication

```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: $TOKEN"

# Test authenticated endpoint
curl http://localhost:8000/admin/users \
  -H "Authorization: Bearer $TOKEN"

# Should return user list
```

#### Test 5: User Management

```bash
# Create user
curl -X POST http://localhost:8000/admin/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "role": "user"
  }'

# List users (should now show 2 users)
curl http://localhost:8000/admin/users \
  -H "Authorization: Bearer $TOKEN"
```

#### Test 6: Camera Management

```bash
# Add camera
curl -X POST http://localhost:8000/admin/cameras \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Camera",
    "source_url": "0",
    "enabled": true
  }'

# List cameras
curl http://localhost:8000/admin/cameras \
  -H "Authorization: Bearer $TOKEN"
```

#### Test 7: Threshold Configuration

```bash
# Update thresholds
curl -X PUT http://localhost:8000/admin/config/thresholds \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "global_threshold": 25
  }'

# Verify
curl http://localhost:8000/admin/config/thresholds \
  -H "Authorization: Bearer $TOKEN"
```

#### Test 8: Activity Logs

```bash
# Get recent logs
curl "http://localhost:8000/admin/logs?limit=10" \
  -H "Authorization: Bearer $TOKEN"

# Should show:
# - Login events
# - User creation
# - Camera addition
# - Threshold update
```

#### Test 9: Export Functions

```bash
# Export logs as CSV
curl "http://localhost:8000/admin/logs/export/csv" \
  -H "Authorization: Bearer $TOKEN" \
  -o logs.csv

# Check file
cat logs.csv

# Export dashboard data as PDF
curl "http://localhost:8000/export/pdf" -o report.pdf
open report.pdf  # Mac
start report.pdf # Windows
xdg-open report.pdf # Linux
```

#### Test 10: Logout

```bash
# Logout
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer $TOKEN"

# Try to use token again (should fail)
curl http://localhost:8000/admin/users \
  -H "Authorization: Bearer $TOKEN"

# Should return 401 Unauthorized
```

---

## Automated Test Script

Save as `test_admin_panel.sh`:

```bash
#!/bin/bash

echo "=== Admin Panel Test Suite ==="
echo ""

BASE_URL="http://localhost:8000"

# Test 1: API Health
echo "Test 1: API Health Check"
curl -s $BASE_URL/ | python -m json.tool
echo "✓ API is running"
echo ""

# Test 2: Login
echo "Test 2: Authentication"
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

TOKEN=$(echo $LOGIN_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

if [ -z "$TOKEN" ]; then
    echo "✗ Login failed"
    exit 1
fi
echo "✓ Login successful"
echo ""

# Test 3: List Users
echo "Test 3: User Management"
USERS=$(curl -s $BASE_URL/admin/users -H "Authorization: Bearer $TOKEN")
echo $USERS | python -m json.tool
echo "✓ User listing works"
echo ""

# Test 4: List Cameras
echo "Test 4: Camera Management"
CAMERAS=$(curl -s $BASE_URL/admin/cameras -H "Authorization: Bearer $TOKEN")
echo $CAMERAS | python -m json.tool
echo "✓ Camera listing works"
echo ""

# Test 5: Get Thresholds
echo "Test 5: Threshold Configuration"
THRESHOLDS=$(curl -s $BASE_URL/admin/config/thresholds -H "Authorization: Bearer $TOKEN")
echo $THRESHOLDS | python -m json.tool
echo "✓ Threshold retrieval works"
echo ""

# Test 6: Get Logs
echo "Test 6: Activity Logs"
LOGS=$(curl -s "$BASE_URL/admin/logs?limit=5" -H "Authorization: Bearer $TOKEN")
echo $LOGS | python -m json.tool | head -20
echo "✓ Log retrieval works"
echo ""

# Test 7: Get Current User
echo "Test 7: Current User Info"
ME=$(curl -s $BASE_URL/auth/me -H "Authorization: Bearer $TOKEN")
echo $ME | python -m json.tool
echo "✓ User info retrieval works"
echo ""

echo "=== All Tests Passed ✓ ==="
```

Run with:

```bash
chmod +x test_admin_panel.sh
./test_admin_panel.sh
```

---

## Windows PowerShell Test Script

Save as `test_admin_panel.ps1`:

```powershell
Write-Host "=== Admin Panel Test Suite ===" -ForegroundColor Green
Write-Host ""

$baseUrl = "http://localhost:8000"

# Test 1: API Health
Write-Host "Test 1: API Health Check"
$health = Invoke-RestMethod -Uri "$baseUrl/"
$health | ConvertTo-Json
Write-Host "✓ API is running" -ForegroundColor Green
Write-Host ""

# Test 2: Login
Write-Host "Test 2: Authentication"
$loginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "$baseUrl/auth/login" -Method POST -Body $loginBody -ContentType "application/json"
$token = $loginResponse.access_token

if (-not $token) {
    Write-Host "✗ Login failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Login successful" -ForegroundColor Green
Write-Host ""

# Test 3: List Users
Write-Host "Test 3: User Management"
$headers = @{ Authorization = "Bearer $token" }
$users = Invoke-RestMethod -Uri "$baseUrl/admin/users" -Headers $headers
$users | ConvertTo-Json
Write-Host "✓ User listing works" -ForegroundColor Green
Write-Host ""

# Test 4: List Cameras
Write-Host "Test 4: Camera Management"
$cameras = Invoke-RestMethod -Uri "$baseUrl/admin/cameras" -Headers $headers
$cameras | ConvertTo-Json
Write-Host "✓ Camera listing works" -ForegroundColor Green
Write-Host ""

# Test 5: Get Thresholds
Write-Host "Test 5: Threshold Configuration"
$thresholds = Invoke-RestMethod -Uri "$baseUrl/admin/config/thresholds" -Headers $headers
$thresholds | ConvertTo-Json
Write-Host "✓ Threshold retrieval works" -ForegroundColor Green
Write-Host ""

# Test 6: Get Logs
Write-Host "Test 6: Activity Logs"
$logs = Invoke-RestMethod -Uri "$baseUrl/admin/logs?limit=5" -Headers $headers
$logs | ConvertTo-Json -Depth 3
Write-Host "✓ Log retrieval works" -ForegroundColor Green
Write-Host ""

Write-Host "=== All Tests Passed ✓ ===" -ForegroundColor Green
```

Run with:

```powershell
.\test_admin_panel.ps1
```

---

## Manual UI Testing Checklist

### Login Page Testing

-   [ ] Page loads without errors
-   [ ] Username field accepts input
-   [ ] Password field accepts input
-   [ ] Password toggle works (eye icon)
-   [ ] Remember me checkbox works
-   [ ] Login with correct credentials succeeds
-   [ ] Login with wrong credentials shows error
-   [ ] Redirects to admin panel after login
-   [ ] "Back to Dashboard" link works

### Admin Panel Testing

-   [ ] Admin panel loads for admin user
-   [ ] Sidebar shows all 7 sections
-   [ ] Username displays in sidebar
-   [ ] Dashboard section shows stats
-   [ ] Recent activity displays

#### User Management

-   [ ] User table loads
-   [ ] Shows default admin user
-   [ ] "Add User" button opens modal
-   [ ] Can create new user
-   [ ] New user appears in table
-   [ ] Cannot delete own account
-   [ ] Can delete other users

#### Camera Management

-   [ ] Camera list displays
-   [ ] "Add Camera" button opens modal
-   [ ] Can add new camera
-   [ ] Camera card displays with info
-   [ ] Enable/disable toggle works
-   [ ] Can delete camera

#### Zone Management

-   [ ] Zone list displays
-   [ ] Zone cards show info
-   [ ] Enable/disable toggle works
-   [ ] Can delete zones
-   [ ] Info modal explains zone creation

#### Threshold Configuration

-   [ ] Global threshold input works
-   [ ] Can update global threshold
-   [ ] Zone thresholds display
-   [ ] Can update zone thresholds
-   [ ] Success notification appears

#### Activity Logs

-   [ ] Logs display in chronological order
-   [ ] Category filter works
-   [ ] Date filters work
-   [ ] "Clear Filters" button works
-   [ ] Export CSV button works
-   [ ] Export PDF button works
-   [ ] Logs are color-coded by category

#### Alert History

-   [ ] Alert table displays
-   [ ] Shows timestamp and details
-   [ ] Filter by type works
-   [ ] Acknowledged status displays

### Main Dashboard Testing

-   [ ] Dashboard loads for unauthenticated users
-   [ ] "Login" button visible when not logged in
-   [ ] After login, username displays
-   [ ] "Logout" button visible when logged in
-   [ ] "Admin" button visible for admin users
-   [ ] "Admin" button hidden for regular users
-   [ ] All existing features still work
-   [ ] Charts still update
-   [ ] Heatmap still loads

---

## Troubleshooting

### Issue: Dependencies not installed

**Error**: `ModuleNotFoundError: No module named 'jose'` or `'passlib'`

**Solution**:

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

### Issue: data/ directory not found

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'data/users.json'`

**Solution**: The directory will be created automatically on first run. If not:

```bash
mkdir data
```

### Issue: Cannot login

**Error**: 401 Unauthorized or invalid credentials

**Solutions**:

1. Verify default credentials: `admin` / `admin123`
2. Check `data/users.json` exists and contains default admin
3. Check browser console for errors
4. Verify API server is running
5. Clear browser cache and localStorage

### Issue: Admin panel blank

**Error**: White page or JavaScript errors

**Solutions**:

1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify `admin.js` loads (Network tab)
4. Check API server is accessible
5. Verify token in localStorage: `localStorage.getItem('auth_token')`

### Issue: Token expired

**Error**: 401 Unauthorized after being logged in

**Solution**: Tokens expire after 24 hours. Simply log in again.

### Issue: CORS errors

**Error**: CORS policy blocking requests

**Solution**: CORS is configured to allow all origins. If issues persist:

1. Check browser console for specific CORS error
2. Verify API server allows your origin
3. Try accessing from same origin (localhost)

---

## Success Criteria

✅ All tests pass  
✅ Login works with default credentials  
✅ Admin panel loads and displays correctly  
✅ All CRUD operations work  
✅ Activity logs record actions  
✅ Exports generate files  
✅ No console errors  
✅ Backward compatibility maintained

---

## Next Steps After Installation

1. **Change default password** (CRITICAL for production)
2. Create additional user accounts
3. Configure cameras for your environment
4. Set appropriate thresholds
5. Review and test zone configurations
6. Set up regular log exports
7. Configure log retention policy
8. Set JWT_SECRET_KEY environment variable

---

## Getting Help

If you encounter issues:

1. Check this guide first
2. Review ADMIN_SETUP.md for detailed documentation
3. Check QUICK_REFERENCE.md for common tasks
4. Look at activity logs for clues
5. Check browser and server console logs

---

**Ready to go!** 🚀

Your admin panel is now fully installed and ready to use. Login with `admin`/`admin123` and start configuring your system!
