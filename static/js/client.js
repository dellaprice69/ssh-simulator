/**
 * SSH Practice Simulator - Client-side JavaScript
 */

class SSHClient {
    constructor() {
        this.authenticated = false;
        this.username = '';
        this.currentDir = '';
        this.sessionId = '';
        this.terminal = document.getElementById('terminal');
        this.commandInput = document.getElementById('command-input');
        this.commandHistory = [];
        this.historyIndex = -1;
        
        this.init();
    }
    
    init() {
        // Event listeners
        document.getElementById('login-form').addEventListener('submit', (e) => this.handleLogin(e));
        
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
        
        // Command input
        this.commandInput.addEventListener('keydown', (e) => this.handleCommandInput(e));
        
        // Logout
        document.getElementById('logout-btn').addEventListener('click', () => this.logout());
    }
    
    switchTab(tabName) {
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        document.getElementById(`${tabName}-tab`).classList.add('active');
        event.target.classList.add('active');
    }
    
    async handleLogin(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorEl = document.getElementById('login-error');
        
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.authenticated = true;
                this.username = data.username;
                this.sessionId = data.session_id;
                this.currentDir = data.home_dir;
                this.switchScreen('terminal');
                this.addTerminalLine('Welcome to SSH Practice Simulator!', 'output');
                this.addTerminalLine('Type "help" for available commands', 'output');
                this.commandInput.focus();
                this.updatePrompt();
            } else {
                errorEl.textContent = data.error || 'Login failed';
                errorEl.classList.add('show');
            }
        } catch (err) {
            errorEl.textContent = 'Connection error: ' + err.message;
            errorEl.classList.add('show');
        }
    }
    
    switchScreen(screenName) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(`${screenName}-screen`).classList.add('active');
    }
    
    updatePrompt() {
        document.getElementById('prompt-user').textContent = this.username;
        
        let displayDir = this.currentDir;
        if (displayDir === `/home/${this.username}`) {
            displayDir = '~';
        }
        document.getElementById('prompt-dir').textContent = displayDir;
        document.getElementById('term-username').textContent = this.username;
    }
    
    handleCommandInput(e) {
        if (e.key === 'Enter') {
            const command = this.commandInput.value.trim();
            this.commandInput.value = '';
            
            if (command) {
                this.executeCommand(command);
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            this.historyIndex++;
            if (this.historyIndex >= this.commandHistory.length) {
                this.historyIndex = this.commandHistory.length - 1;
            }
            if (this.historyIndex >= 0) {
                this.commandInput.value = this.commandHistory[this.commandHistory.length - 1 - this.historyIndex];
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            this.historyIndex--;
            if (this.historyIndex < 0) {
                this.historyIndex = -1;
                this.commandInput.value = '';
            } else {
                this.commandInput.value = this.commandHistory[this.commandHistory.length - 1 - this.historyIndex];
            }
        }
    }
    
    async executeCommand(command) {
        // Add to history
        if (!this.commandHistory.includes(command)) {
            this.commandHistory.push(command);
        }
        this.historyIndex = -1;
        
        // Show command in terminal
        this.addTerminalLine(`${this.username}@ssh-simulator:${this.currentDir}$ ${command}`, 'command');
        
        try {
            const response = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId, command })
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.addTerminalLine(data.error, 'error');
                return;
            }
            
            // Update working directory
            if (data.working_dir) {
                this.currentDir = data.working_dir;
                this.updatePrompt();
            }
            
            // Show output
            if (data.output) {
                if (data.output === '[CLEAR]') {
                    this.terminal.innerHTML = '';
                } else {
                    const lines = data.output.split('\n');
                    lines.forEach((line, idx) => {
                        if (line || idx < lines.length - 1) {
                            this.addTerminalLine(line, data.exit_code === 0 ? 'output' : 'error');
                        }
                    });
                }
            }
        } catch (err) {
            this.addTerminalLine(`Error: ${err.message}`, 'error');
        }
        
        // Auto-scroll to bottom
        this.terminal.scrollTop = this.terminal.scrollHeight;
    }
    
    addTerminalLine(text, className = 'output') {
        const line = document.createElement('div');
        line.className = `terminal-line ${className}`;
        line.textContent = text;
        this.terminal.appendChild(line);
    }
    
    async logout() {
        try {
            await fetch('/api/auth/logout', { method: 'POST' });
            this.authenticated = false;
            this.username = '';
            this.currentDir = '';
            this.sessionId = '';
            this.commandHistory = [];
            this.historyIndex = -1;
            this.terminal.innerHTML = '';
            this.commandInput.value = '';
            this.switchScreen('login');
            
            document.getElementById('login-error').classList.remove('show');
            document.getElementById('username').value = 'user';
            document.getElementById('password').value = 'password123';
        } catch (err) {
            console.error('Logout error:', err);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new SSHClient();
});
