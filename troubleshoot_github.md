# Troubleshooting GitHub Push Issues

## Current Issue
`fatal: unable to access 'https://github.com/dhruvpd77/quiznjoy.git/': Could not resolve host: github.com`

## Solutions to Try

### Solution 1: Check Internet Connection
```bash
ping github.com
```
If this fails, you have a network connectivity issue.

### Solution 2: Use GitHub's IP Address (Temporary Fix)
Add to `/etc/hosts` (Linux/Mac) or `C:\Windows\System32\drivers\etc\hosts` (Windows):
```
140.82.121.3 github.com
```

### Solution 3: Use SSH Instead of HTTPS
```bash
# Check if you have SSH key
ls -al ~/.ssh

# If no SSH key, generate one:
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add SSH key to GitHub (copy public key)
cat ~/.ssh/id_ed25519.pub

# Then change remote URL to SSH:
git remote set-url origin git@github.com:dhruvpd77/quiznjoy.git
git push origin quiznjoyfinal
```

### Solution 4: Check Proxy Settings
If you're behind a proxy:
```bash
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080
```

### Solution 5: Flush DNS Cache (Windows)
Open Command Prompt as Administrator:
```cmd
ipconfig /flushdns
```

### Solution 6: Use Mobile Hotspot
Try using your phone's mobile hotspot to rule out network/firewall issues.

### Solution 7: Manual Upload via GitHub Web Interface
1. Go to https://github.com/dhruvpd77/quiznjoy
2. Click "uploading an existing file"
3. Drag and drop your project folder
4. Commit to `quiznjoyfinal` branch

