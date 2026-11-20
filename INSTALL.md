# INSTALLATION & SETUP GUIDE

## System Requirements

- **Python**: 3.7 or higher
- **OS**: macOS, Linux, Windows (with WSL), or any Unix-like system
- **Browser**: Chrome, Firefox, Safari, Edge, or any modern browser
- **Network**: Localhost (localhost:8888)
- **Disk**: ~5MB free space

## Installation (3 Easy Steps)

### Step 1: Verify Python Installation

```bash
python3 --version
```

Expected output: Python 3.7.0 or higher

If not installed:
- **macOS**: `brew install python3`
- **Ubuntu/Debian**: `sudo apt-get install python3`
- **Windows**: Download from https://www.python.org/downloads/ (use WSL)
- **Other**: https://www.python.org/downloads/

### Step 2: Navigate to Project

```bash
cd /tmp/ssh_simulator
```

Or wherever you extracted the files.

### Step 3: Run the Application

```bash
python3 app.py
```

You should see:
```
🚀 SSH Simulator running on http://localhost:8888
📖 Open in your browser and use test credentials:
   admin / admin123 (with sudo)
   user / password123
   guest / guest123

🛑 Press Ctrl+C to stop
```

## Opening in Browser

1. Open your web browser
2. Navigate to: **http://localhost:8888**
3. You should see the login screen

## First Time Login

1. **Username**: `user`
2. **Password**: `password123`
3. Click: **Login with Password**

If successful, you'll see the terminal interface with the prompt:
```
user@ssh-simulator:~$ 
```

## Running Commands

### Try These Commands

```bash
# Show current user
whoami

# Show current directory
pwd

# List files
ls -la

# Show system information
uname

# Show current date/time
date

# Display help
help

# Show command history
history
```

### Stop the Server

Press **Ctrl+C** in the terminal where `python3 app.py` is running.

## Troubleshooting

### "Address already in use" Error

Port 8888 is already in use. Either:

**Option A**: Stop the existing process

```bash
# Find process using port 8888
lsof -i :8888

# Kill it (replace XXXX with the PID)
kill -9 XXXX
```

**Option B**: Use a different port

Edit `app.py` and change:
```python
run_server(port=8888)
```
to:
```python
run_server(port=9000)
```

### "Python not found" Error

Python isn't installed or not in your PATH. Install it:

- **macOS**: `brew install python3`
- **Ubuntu**: `sudo apt-get install python3`
- **Windows**: Use WSL and install Python there

### Cannot login

- Check username spelling (case-sensitive)
- Verify password from About tab
- Try: **user** / **password123**

### Browser won't connect

- Ensure server is running (`python3 app.py`)
- Check you're using `http://` not `https://`
- Try: **http://localhost:8888**
- Wait 2-3 seconds after starting server

### Commands not working

- Type `help` to see available commands
- Check command syntax
- Some commands need admin user (sudo)

## Using Different Test Users

### Regular User (No Sudo)
```
Username: user
Password: password123
```

### Administrator (With Sudo)
```
Username: admin
Password: admin123
```

### Guest Account
```
Username: guest
Password: guest123
```

## Network Access (Advanced)

By default, only localhost can access the simulator. To allow network access:

**Edit `app.py` and change:**

```python
def run_server(port=5000):
    server = HTTPServer(('localhost', port), SSHSimulatorHandler)
```

**To:**

```python
def run_server(port=5000):
    server = HTTPServer(('0.0.0.0', port), SSHSimulatorHandler)
```

Then access from other computers: `http://your_ip:8888`

**Warning**: Only do this on trusted networks!

## Running as Background Process

### macOS/Linux

```bash
# Start in background
nohup python3 app.py > ssh_simulator.log 2>&1 &

# Stop the process
pkill -f "python3 app.py"
```

### Windows (PowerShell)

```powershell
# Start in background
Start-Process python3 "app.py"

# Stop the process
Stop-Process -Name python -Force
```

## Docker (Optional)

Create a `Dockerfile` to run in Docker:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
EXPOSE 8888
CMD ["python3", "app.py"]
```

Build and run:

```bash
docker build -t ssh-simulator .
docker run -p 8888:8888 ssh-simulator
```

## Multiple Instances

Run on different ports:

```bash
# Terminal 1
python3 app.py  # Uses port 8888

# Terminal 2
sed 's/run_server()/run_server(port=8889)/' app.py > app2.py
python3 app2.py  # Uses port 8889
```

Access:
- http://localhost:8888
- http://localhost:8889

## Development Mode

For development with auto-reload:

```bash
# Install watchdog
pip3 install watchdog

# Run with auto-reload
python3 -m watchdog.auto_reload app.py
```

## Production Considerations

For classroom or production use:

1. **Use a proper WSGI server** (Gunicorn, uWSGI)
2. **Add reverse proxy** (Nginx, Apache)
3. **Enable HTTPS** with SSL certificates
4. **Add authentication** for access control
5. **Monitor memory usage** (might grow with many users)
6. **Back up session data** if needed

Example with Gunicorn:

```bash
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:8888 app:SSHSimulatorHandler
```

## Configuration Files

No configuration files needed! Everything is hardcoded for simplicity.

To customize:
1. Edit `app.py` for backend changes
2. Edit `static/css/style.css` for UI changes
3. Edit `static/js/client.js` for client behavior

## Performance Optimization

For large classroom deployments:

```python
# In app.py, increase limits
# Max concurrent connections
max_connections = 100

# Session timeout
session_timeout = 3600  # 1 hour
```

## Uninstallation

Just delete the directory:

```bash
rm -rf /tmp/ssh_simulator
```

No system-wide changes were made.

## Support

If you have issues:

1. Check the terminal output for error messages
2. Review this guide for your specific error
3. Try a fresh installation
4. Verify Python version is 3.7+

## Next Steps

After successful installation:

1. ✓ Login with test credentials
2. ✓ Try basic commands (`help`, `whoami`, `pwd`)
3. ✓ Explore file system (`ls`, `cd`)
4. ✓ Read the full README.md for complete documentation
5. ✓ Try admin user and sudo commands

---

**Happy learning! 🐧**
