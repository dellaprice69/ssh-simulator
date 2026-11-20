# 🔐 SSH Login Practice Simulator

A lightweight, **zero-dependency** web-based SSH login testing and practice environment. Learn SSH authentication, Linux commands, and system administration in a safe sandbox - **no Flask, no npm, no Docker needed!**

## ⚡ Quick Start

```bash
# 1. Navigate to project directory
cd /tmp/ssh_simulator

# 2. Run (Python 3.7+ only requirement)
python3 app.py

# 3. Open browser
# http://localhost:8888

# 4. Login with test credentials:
#    Username: user
#    Password: password123
```

Done! That's it. No dependencies, no installation, just pure Python.

## 🎯 Features

✅ **No External Dependencies** - Uses only Python standard library  
✅ **Full Virtual Linux Environment** - Realistic SSH experience  
✅ **20+ Linux Commands** - pwd, ls, cat, echo, mkdir, ssh-keygen, sudo, etc.  
✅ **Multi-User System** - admin (sudo), user, guest accounts  
✅ **Command History** - Arrow keys to navigate history  
✅ **Virtual File System** - Create, read, modify files  
✅ **User Permissions** - Different privilege levels  
✅ **Realistic Terminal UI** - Authentic hacker-style interface  
✅ **Completely Isolated** - No actual system access  

## 👥 Test Users

| Username | Password | Sudo | Purpose |
|----------|----------|------|---------|
| **admin** | admin123 | ✓ | Superuser with full access |
| **user** | password123 | ✗ | Regular user (no privileges) |
| **guest** | guest123 | ✗ | Guest account (limited access) |

## 📚 Available Commands

### Navigation & Files
```
pwd              Print working directory
cd <dir>         Change directory
ls [-la]         List directory contents
mkdir <dir>      Create directory
touch <file>     Create file
cp <src> <dst>   Copy file
mv <src> <dst>   Move/rename file
rm <file>        Remove file
```

### File Operations
```
cat <file>       Display file contents
echo <text>      Print text
```

### User & System
```
whoami           Current username
id               User ID and groups
sudo <cmd>       Execute as superuser (admin only)
uname            System information
date             Current date/time
df               Disk usage
du <path>        Directory size
ps               Process list
```

### SSH & Utilities
```
ssh-keygen      Generate SSH key pair
history          Show command history
help             Display this help
clear            Clear screen
```

## 🏗️ Project Structure

```
/tmp/ssh_simulator/
├── app.py                      # Main application (Python HTTPServer)
├── index.html                  # HTML interface
├── static/
│   ├── css/
│   │   └── style.css          # Terminal styling
│   └── js/
│       └── client.js          # Client-side logic
└── README.md                   # This file
```

## 🔄 How It Works

### Backend Architecture
- **HTTPServer**: Pure Python standard library HTTP server (no Flask!)
- **CommandExecutor**: Simulates 20+ Linux commands
- **Virtual File System**: In-memory file storage per user
- **Session Management**: Track authenticated users
- **User System**: Multiple users with different permissions

### Frontend Architecture  
- **Login Screen**: Password authentication
- **Terminal Emulator**: Real-time command execution
- **Command History**: Navigate with arrow keys
- **Dynamic Prompt**: Shows username and working directory

### How Commands Work

1. User types command in terminal
2. Frontend sends POST request to `/api/command`
3. Backend parses command and routes to handler
4. Handler simulates command and returns output
5. Frontend displays output in terminal
6. Working directory updates automatically

Example flow:
```
User types: "cd /home/user && ls -la"
         ↓
API Call: {"session_id": "...", "command": "cd /home/user && ls -la"}
         ↓
Backend: Parses commands, executes 'cd' (changes state), then 'ls' (lists files)
         ↓
Response: {"output": "drwxr... file1\ndrwxr... file2\n", "working_dir": "/home/user"}
         ↓
Display: Renders output and updates prompt
```

## 🎓 Learning Objectives

By using this simulator, you'll practice:

### 1. SSH Authentication
- Password-based login
- Understanding session tokens
- User credential validation

### 2. Linux Commands
- File navigation (`cd`, `pwd`, `ls`)
- File operations (`cat`, `echo`, `cp`, `mv`)
- User information (`whoami`, `id`)
- System info (`uname`, `date`, `df`, `ps`)

### 3. System Administration
- Sudo privileges and permission handling
- File structure and hierarchy
- User and group concepts
- Directory navigation

### 4. Terminal Skills
- Command syntax and arguments
- Exit codes (0 = success, non-zero = error)
- Command history navigation
- Working directory management

## 💡 Usage Examples

### Basic Navigation
```bash
$ pwd
/home/user

$ cd /
$ pwd
/

$ cd ~
$ pwd
/home/user

$ ls -la
```

### File Operations
```bash
$ echo "Hello World" > greeting.txt
$ cat greeting.txt
Hello World

$ cp greeting.txt greeting_backup.txt
$ mv greeting_backup.txt greeting_copy.txt
$ rm greeting_copy.txt
```

### User Information
```bash
$ whoami
user

$ id
uid=1000(user) gid=1000(users) groups=1000(users)

$ sudo whoami
user is not in the sudoers file. This incident will be reported.
```

### Admin Commands (requires admin user)
```bash
$ sudo whoami
root

$ sudo id
uid=0(root) gid=0(root) groups=0(root)
```

### System Information
```bash
$ uname -a
Linux ssh-simulator 5.10.0 #1 SMP x86_64 GNU/Linux

$ date
Fri Nov 20 12:23:29 UTC 2026

$ df
Filesystem     1K-blocks Used Available Use% Mounted on
/dev/sda1 102400000 51200000 51200000 50% /

$ ps
PID TTY TIME CMD
  1   ?  0:00 init
 42   ?  0:01 sshd
100 pts/0 0:00 bash
150 pts/0 0:00 ps
```

## 🚀 Advanced Features

### Command History
- Press **↑** to go to previous command
- Press **↓** to go to next command
- Commands are saved across the session

### Quick Commands
Buttons on the sidebar for instant access to common commands:
- `help` - Show all available commands
- `whoami` - Current user
- `pwd` - Working directory
- `ls -la` - Detailed file listing
- `id` - User information
- `uname -a` - System info
- `date` - Current date/time
- `history` - Command history

### Tab Completion
Type commands and they'll appear in auto-suggest (future feature)

## 🔧 Extending the Simulator

### Add New Users

Edit `app.py` and modify the `SSHSimulatorHandler` class:

```python
class SSHSimulatorHandler(BaseHTTPRequestHandler):
    users = {
        'admin': User('admin', 'admin123', is_sudo=True),
        'user': User('user', 'password123', is_sudo=False),
        'newuser': User('newuser', 'mypassword', is_sudo=False),  # Add this
    }
```

### Add New Commands

Add a handler method in the `CommandExecutor` class:

```python
def cmd_mycommand(self, args, user):
    """Description of what mycommand does"""
    output = f"Output from mycommand with args: {args}\n"
    return output, 0  # 0 = success, 1+ = error
```

Then register it in the `execute` method:

```python
handlers = {
    'mycommand': self.cmd_mycommand,  # Add this line
    # ... existing commands
}
```

### Add Files to Home Directory

Edit the `User` class:

```python
def create_default_files(self):
    self.files = {
        # ... existing files
        f"{self.home_dir}/myfile.txt": "File contents here\n",
    }
```

## ⚙️ Configuration

### Change Port

Edit the last line of `app.py`:

```python
if __name__ == '__main__':
    run_server(port=9000)  # Change from 8888 to 9000
```

### Change Server Address

Modify the `run_server` function:

```python
def run_server(port=5000):
    server = HTTPServer(('0.0.0.0', port), SSHSimulatorHandler)  # Allow external connections
    # or
    server = HTTPServer(('127.0.0.1', port), SSHSimulatorHandler)  # Localhost only
```

## 🔒 Security Considerations

### ⚠️ For Educational Use Only

This is a **learning tool** and should only be used in educational settings:

- Credentials are stored in plain text (intentional for learning)
- Not designed for real SSH server functionality
- Do not use for production or sensitive environments
- Keep this running only on trusted networks
- It's completely isolated - no actual system access

### Why It's Safe

✓ No real file system access - everything is simulated in memory  
✓ No actual system commands executed  
✓ No network access beyond localhost (by default)  
✓ Commands are sandboxed and isolated  
✓ User permissions are simulated, not enforced  

## 🐛 Troubleshooting

### "Port already in use"

Another process is using port 8888. Either:
1. Kill the existing process: `lsof -i :8888`
2. Use a different port: Edit `app.py` and change `run_server(port=8888)` to another port

### Cannot login

- Double-check username spelling (case-sensitive)
- Verify password from the About tab
- Credentials: user/password123, admin/admin123, guest/guest123

### Command not working

- Check if command exists: Type `help`
- Check command syntax
- Some commands require sudo (admin user only)

### Pages not loading

- Ensure the server is running: `python3 app.py`
- Check you're accessing http://localhost:8888/
- Look for errors in the terminal where app.py is running

## 📊 Performance

### System Requirements
- **CPU**: Minimal (single-threaded)
- **Memory**: < 50MB
- **Network**: Localhost only (by default)
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)

### Scalability
- Handles multiple concurrent users
- In-memory storage only (data lost on restart)
- Suitable for classroom use (20-30 students)

## 🎨 Customization

### Change Terminal Theme

Edit `/tmp/ssh_simulator/static/css/style.css`:

```css
/* Change these colors */
body {
    background: #0a0e27;  /* Dark background */
    color: #00ff41;       /* Green text */
}
```

### Add Welcome Message

Edit the `cmd_help` method in `app.py` to customize the welcome text.

### Modify Prompt Style

Edit `/tmp/ssh_simulator/static/js/client.js` and modify the `updatePrompt()` method.

## 📖 Educational Curriculum

### Beginner (Session 1)
1. Login with password
2. Learn basic commands: `whoami`, `pwd`, `ls`
3. Navigate directories: `cd`, `ls -la`
4. View files: `cat`

### Intermediate (Session 2)
1. File operations: `cp`, `mv`, `rm`, `touch`
2. File content: `echo`, `cat` with different files
3. User commands: `id`, `whoami`
4. System info: `uname`, `date`, `df`

### Advanced (Session 3)
1. Permissions: Understand `sudo` and privilege levels
2. Login as admin: `admin/admin123`
3. Try privileged commands: `sudo whoami`
4. Explore error messages when permissions denied

### Expert (Session 4)
1. Command history and workflow
2. Creating complex command chains
3. Understanding exit codes
4. Simulating real-world scenarios

## 🤝 Contributing

Want to extend the simulator?

1. Add new commands to `CommandExecutor` class
2. Add new users to the `users` dictionary
3. Modify the HTML/CSS for UI improvements
4. Test thoroughly before deploying

## 📝 License

MIT License - Free for educational use. See LICENSE file for details.

## 🆘 Support & Help

### In-App Help
- Type `help` in the terminal for command list
- Click "About" tab on login screen for user credentials
- Use "Quick Links" sidebar for common commands

### Common Questions

**Q: Can I add more commands?**  
A: Yes! Add handler methods to `CommandExecutor` class (see "Extending" section)

**Q: Can I use this for real SSH?**  
A: No, this is a simulator only. Real SSH needs an actual SSH server.

**Q: Can I run this on the internet?**  
A: Not recommended - it's for local learning only. Use with VPN/firewall.

**Q: How do I save my progress?**  
A: Session data is in-memory. It's reset when server restarts. This is intentional.

**Q: Can I modify the terminal colors?**  
A: Yes! Edit `static/css/style.css` and change the color values.

## 🎯 Next Steps

1. **Install**: Run `python3 app.py`
2. **Explore**: Try all the test users
3. **Learn**: Complete the educational curriculum
4. **Practice**: Create your own scenarios
5. **Extend**: Add new commands or features
6. **Teach**: Use it in your classroom

---

**Made for learning Linux and SSH best practices** 🐧

**Questions?** Check the help system by typing `help` in the terminal!
