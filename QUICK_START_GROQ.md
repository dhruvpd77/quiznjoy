# 🚀 Quick Start: Groq (FREE AI - 2 Minutes Setup)

## Why Groq?
- ✅ **100% FREE** - No payment method needed
- ✅ **Very Fast** - Faster than OpenAI
- ✅ **Easy Setup** - Just get an API key
- ✅ **Good Quality** - Uses Llama 3.1 model

## Setup Steps (2 Minutes)

### Step 1: Get Free API Key
1. Go to: https://console.groq.com/
2. Click "Sign Up" (use Google/GitHub for quick signup)
3. Go to: https://console.groq.com/keys
4. Click "Create API Key"
5. Copy your API key (starts with `gsk_...`)

### Step 2: Add to Your Project

**Option A: Add to settings.py (Quick)**
```python
# In quiz_project/settings.py
AI_PROVIDER = 'groq'
GROQ_API_KEY = 'your-groq-api-key-here'
```

**Option B: Environment Variable (Recommended)**
```bash
# Windows PowerShell
$env:GROQ_API_KEY="your-groq-api-key-here"
$env:AI_PROVIDER="groq"

# Windows CMD
set GROQ_API_KEY=your-groq-api-key-here
set AI_PROVIDER=groq

# Linux/Mac
export GROQ_API_KEY='your-groq-api-key-here'
export AI_PROVIDER='groq'
```

### Step 3: Install Dependencies
```bash
pip install requests
```

### Step 4: Restart Server
```bash
python manage.py runserver
```

### Step 5: Test It!
1. Complete a quiz
2. Click "Understand Solution" on any question
3. It should work! 🎉

## That's It!

Your quiz app now uses **FREE Groq AI** - no payment required!

## Troubleshooting

**Error: "Groq API key not configured"**
- Make sure you copied the full API key
- Check it starts with `gsk_`
- Verify it's in settings.py or environment variable

**Error: "Invalid API key"**
- Make sure you created the key at https://console.groq.com/keys
- Try creating a new key

**Still not working?**
- Make sure `AI_PROVIDER = 'groq'` in settings.py
- Restart your Django server
- Check the error message for details

## Need Help?

Check `FREE_AI_SETUP.md` for more options and detailed instructions.

