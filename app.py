#!/usr/bin/env python3
"""
SSH Login Practice Simulator
A web-based tool for practicing SSH login and Linux commands
No external dependencies - uses only Python standard library
"""

import json
import hashlib
import uuid
import threading
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from io import StringIO
import mimetypes

# ==================== User Management ====================

class User:
    """Simulated Linux user with file system and permissions"""
    
    def __init__(self, username, password=None, is_sudo=False):
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest() if password else None
        self.is_sudo = is_sudo
        self.home_dir = f"/home/{username}"
        self.current_dir = self.home_dir
        self.files = {}
        self.create_default_files()
    
    def create_default_files(self):
        """Create default home directory files"""
        self.files = {
            f"{self.home_dir}/.bashrc": "# Bash configuration\nalias ll='ls -la'\nalias la='ls -A'\n",
            f"{self.home_dir}/.bash_profile": "# Bash profile\nexport PATH=/usr/local/bin:/usr/bin:/bin\n",
            f"{self.home_dir}/.ssh/config": "# SSH Configuration\nHost *\n    AddKeysToAgent yes\n",
            f"{self.home_dir}/README.txt": f"Welcome {self.username}!\nThis is a practice SSH environment.\n",
            f"{self.home_dir}/notes.txt": "Linux Practice Notes\n- Learning SSH authentication\n- Practicing common commands\n",
        }
    
    def verify_password(self, password):
        """Verify password"""
        if not self.password_hash:
            return False
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

# ==================== Command Execution ====================

class CommandExecutor:
    """Execute simulated Linux commands"""
    
    def __init__(self):
        self.history = []
    
    def execute(self, command, user):
        """Execute a command and return output"""
        self.history.append({'user': user.username, 'command': command, 'timestamp': datetime.now().isoformat()})
        
        parts = command.strip().split()
        if not parts:
            return '', 0
        
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Command routing
        handlers = {
            'help': self.cmd_help,
            'whoami': self.cmd_whoami,
            'pwd': self.cmd_pwd,
            'ls': self.cmd_ls,
            'cat': self.cmd_cat,
            'echo': self.cmd_echo,
            'cd': self.cmd_cd,
            'mkdir': self.cmd_mkdir,
            'touch': self.cmd_touch,
            'rm': self.cmd_rm,
            'cp': self.cmd_cp,
            'mv': self.cmd_mv,
            'uname': self.cmd_uname,
            'date': self.cmd_date,
            'id': self.cmd_id,
            'sudo': self.cmd_sudo,
            'ps': self.cmd_ps,
            'df': self.cmd_df,
            'du': self.cmd_du,
            'clear': self.cmd_clear,
            'history': self.cmd_history,
            'ssh-keygen': self.cmd_ssh_keygen,
        }
        
        if cmd in handlers:
            output, code = handlers[cmd](args, user)
            return output, code
        else:
            return f"command not found: {cmd}\n", 127
    
    # Command handlers
    def cmd_help(self, args, user):
        help_text = """SSH Practice Environment - Available Commands:

Navigation:
  pwd              - Print working directory
  cd <dir>         - Change directory
  ls [-la]         - List directory contents
  mkdir <dir>      - Create directory
  touch <file>     - Create file

File Operations:
  cat <file>       - Display file contents
  echo <text>      - Print text
  cp <src> <dst>   - Copy file
  mv <src> <dst>   - Move/rename file
  rm <file>        - Remove file

User & Permissions:
  whoami           - Current username
  id               - User ID and groups
  sudo <cmd>       - Execute as superuser

System Info:
  uname            - System information
  date             - Current date/time
  df               - Disk usage
  du <path>        - Directory size
  ps               - Process list

SSH:
  ssh-keygen      - Generate SSH keys

Other:
  history          - Command history
  clear            - Clear screen"""
        return help_text.strip() + '\n', 0
    
    def cmd_whoami(self, args, user):
        return user.username + '\n', 0
    
    def cmd_pwd(self, args, user):
        return user.current_dir + '\n', 0
    
    def cmd_cd(self, args, user):
        if not args:
            user.current_dir = user.home_dir
            return '', 0
        
        new_dir = args[0]
        if new_dir.startswith('/'):
            user.current_dir = new_dir
        else:
            user.current_dir = f"{user.current_dir}/{new_dir}".replace('//', '/')
        
        return '', 0
    
    def cmd_ls(self, args, user):
        path = user.current_dir
        if args and not args[0].startswith('-'):
            path = args[0]
        
        files = [f for f in user.files.keys() if f.startswith(path)]
        if not files:
            return f"ls: cannot access '{path}': No such file or directory\n", 1
        
        if '-la' in args or '-l' in args or '-a' in args:
            output = "total " + str(len(files)) + "\n"
            for f in files:
                size = str(len(user.files[f])).rjust(10)
                name = f.split('/')[-1]
                output += f"-rw-r--r-- 1 {user.username} users {size} Nov 18 10:00 {name}\n"
        else:
            output = '\n'.join([f.split('/')[-1] for f in files]) + '\n'
        
        return output, 0
    
    def cmd_cat(self, args, user):
        if not args:
            return "cat: missing operand\n", 1
        
        filepath = args[0] if args[0].startswith('/') else f"{user.current_dir}/{args[0]}"
        if filepath in user.files:
            content = user.files[filepath]
            return content if content.endswith('\n') else content + '\n', 0
        
        return f"cat: {args[0]}: No such file or directory\n", 1
    
    def cmd_echo(self, args, user):
        return ' '.join(args) + '\n', 0
    
    def cmd_mkdir(self, args, user):
        if not args:
            return "mkdir: missing operand\n", 1
        return '', 0
    
    def cmd_touch(self, args, user):
        if not args:
            return "touch: missing operand\n", 1
        filepath = args[0] if args[0].startswith('/') else f"{user.current_dir}/{args[0]}"
        user.files[filepath] = ''
        return '', 0
    
    def cmd_rm(self, args, user):
        if not args:
            return "rm: missing operand\n", 1
        return '', 0
    
    def cmd_cp(self, args, user):
        if len(args) < 2:
            return "cp: missing operand\n", 1
        return '', 0
    
    def cmd_mv(self, args, user):
        if len(args) < 2:
            return "mv: missing operand\n", 1
        return '', 0
    
    def cmd_uname(self, args, user):
        return "Linux ssh-simulator 5.10.0 #1 SMP x86_64 GNU/Linux\n", 0
    
    def cmd_date(self, args, user):
        return datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y\n"), 0
    
    def cmd_id(self, args, user):
        gid = "0" if user.is_sudo else "1000"
        return f"uid=1000({user.username}) gid={gid}(users) groups={gid}(users)\n", 0
    
    def cmd_sudo(self, args, user):
        if not user.is_sudo:
            return "user is not in the sudoers file. This incident will be reported.\n", 1
        if args:
            return self.execute(' '.join(args), user)
        return "sudo: no command specified\n", 1
    
    def cmd_ps(self, args, user):
        processes = ["PID TTY TIME CMD", "  1   ?  0:00 init", " 42   ?  0:01 sshd", "100 pts/0 0:00 bash", "150 pts/0 0:00 ps"]
        return '\n'.join(processes) + '\n', 0
    
    def cmd_df(self, args, user):
        output = "Filesystem 1K-blocks Used Available Use% Mounted on\n"
        output += "/dev/sda1 102400000 51200000 51200000 50% /\n"
        return output, 0
    
    def cmd_du(self, args, user):
        path = args[0] if args else user.current_dir
        return f"4096\t{path}\n", 0
    
    def cmd_ssh_keygen(self, args, user):
        output = f"Generated key pair for {user.username}:\n"
        output += f"Private key: ~/.ssh/id_rsa\n"
        output += f"Public key: ~/.ssh/id_rsa.pub\n"
        return output, 0
    
    def cmd_clear(self, args, user):
        return '[CLEAR]', 0
    
    def cmd_history(self, args, user):
        output = ""
        for i, cmd_entry in enumerate(self.history[-20:], 1):
            output += f"{i:4d} {cmd_entry['command']}\n"
        return output, 0

# ==================== HTTP Server ====================

class SSHSimulatorHandler(BaseHTTPRequestHandler):
    """HTTP request handler for SSH simulator"""
    
    # Class variables shared across all requests
    users = {
        'admin': User('admin', 'admin123', is_sudo=True),
        'user': User('user', 'password123', is_sudo=False),
        'guest': User('guest', 'guest123', is_sudo=False),
    }
    executor = CommandExecutor()
    sessions = {}  # session_id -> {'username': ..., 'created': ...}
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Serve HTML
        if path == '/' or path == '/index.html':
            self.serve_file('index.html', 'text/html')
        # API: Get session status
        elif path == '/api/status':
            self.api_status()
        # API: List users
        elif path == '/api/users':
            self.api_users()
        # Static files
        elif path.startswith('/static/'):
            filepath = path[1:]  # Remove leading slash
            mime_type, _ = mimetypes.guess_type(filepath)
            self.serve_file(filepath, mime_type or 'application/octet-stream')
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Read body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        # Route API calls
        if path == '/api/auth/login':
            self.api_login(data)
        elif path == '/api/auth/logout':
            self.api_logout(data)
        elif path == '/api/command':
            self.api_command(data)
        else:
            self.send_error(404)
    
    # API Handlers
    
    def api_login(self, data):
        """Login with password"""
        username = data.get('username')
        password = data.get('password')
        
        user = self.users.get(username)
        if not user or not user.verify_password(password):
            self.send_json({'success': False, 'error': 'Invalid credentials'}, 401)
            return
        
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {'username': username, 'created': datetime.now().isoformat()}
        
        self.send_json({
            'success': True,
            'username': username,
            'session_id': session_id,
            'home_dir': user.home_dir,
            'is_sudo': user.is_sudo
        })
    
    def api_logout(self, data):
        """Logout"""
        self.send_json({'success': True})
    
    def api_command(self, data):
        """Execute command"""
        session_id = data.get('session_id')
        command = data.get('command', '')
        
        if session_id not in self.sessions:
            self.send_json({'error': 'Not authenticated'}, 401)
            return
        
        username = self.sessions[session_id]['username']
        user = self.users.get(username)
        if not user:
            self.send_json({'error': 'User not found'}, 401)
            return
        
        output, code = self.executor.execute(command, user)
        
        self.send_json({
            'output': output,
            'exit_code': code,
            'working_dir': user.current_dir
        })
    
    def api_status(self):
        """Get session status"""
        session_id = self.path.split('?')[-1] if '?' in self.path else ''
        
        if session_id not in self.sessions:
            self.send_json({'authenticated': False})
            return
        
        username = self.sessions[session_id]['username']
        user = self.users.get(username)
        self.send_json({
            'authenticated': True,
            'username': username,
            'working_dir': user.current_dir,
            'is_sudo': user.is_sudo
        })
    
    def api_users(self):
        """List available users"""
        users_list = []
        for username, user in self.users.items():
            users_list.append({
                'username': username,
                'password': 'See login page',
                'is_sudo': user.is_sudo
            })
        self.send_json({'users': users_list})
    
    # Utilities
    
    def serve_file(self, filepath, mime_type):
        """Serve a static file"""
        base_dir = Path(__file__).parent
        file_path = base_dir / filepath
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', mime_type)
                self.send_header('Content-Length', len(content))
                self.send_header('Cache-Control', 'max-age=3600')
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)
    
    def send_json(self, data, status=200):
        """Send JSON response"""
        response = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response)
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        return

# ==================== Main ====================

def run_server(port=5000):
    """Start the HTTP server"""
    server = HTTPServer(('localhost', port), SSHSimulatorHandler)
    print(f"🚀 SSH Simulator running on http://localhost:{port}")
    print(f"📖 Open in your browser and use test credentials:")
    print(f"   admin / admin123 (with sudo)")
    print(f"   user / password123")
    print(f"   guest / guest123")
    print(f"\n🛑 Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        server.shutdown()

if __name__ == '__main__':
    run_server(port=8888)
