# OpenAI API Key Setup Instructions

## ⚠️ SECURITY WARNING
Your API key has been exposed in this conversation. Please regenerate it at:
https://platform.openai.com/api-keys

## Option 1: Environment Variable (Recommended for Production)

### Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY="your-new-api-key-here"
```

### Windows (Command Prompt):
```cmd
set OPENAI_API_KEY=your-new-api-key-here
```

### Windows (Permanent - System Environment Variable):
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to "Advanced" tab → "Environment Variables"
3. Under "User variables", click "New"
4. Variable name: `OPENAI_API_KEY`
5. Variable value: `your-new-api-key-here`
6. Click OK and restart your terminal/IDE

### Linux/Mac:
```bash
export OPENAI_API_KEY='your-new-api-key-here'
```

To make it permanent, add to `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export OPENAI_API_KEY="your-new-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## Option 2: Direct in settings.py (Development Only)

The API key is currently set directly in `settings.py` for quick testing. 
**This is NOT recommended for production!**

To use environment variable instead, remove the hardcoded key from `settings.py` and use Option 1.

## Testing

After setting up, restart your Django development server:
```bash
python manage.py runserver
```

Then test the "Understand Solution" button on any quiz results page.

