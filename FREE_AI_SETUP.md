# Free AI API Setup Guide

## 🎉 Great News! You can use FREE AI APIs!

I've updated your code to support multiple **FREE** AI providers. No payment method required!

## Recommended: Groq (Fastest & Easiest)

### Why Groq?
- ✅ **100% FREE** - No payment method needed
- ✅ **Very Fast** - Faster than OpenAI
- ✅ **Easy Setup** - Just get an API key
- ✅ **Good Quality** - Uses Llama 3.1 model

### Setup Steps:
1. Go to https://console.groq.com/
2. Sign up for free (use Google/GitHub)
3. Go to https://console.groq.com/keys
4. Click "Create API Key"
5. Copy your API key
6. Add to `settings.py` or environment variable:

```python
# In settings.py
GROQ_API_KEY = 'your-groq-api-key-here'
```

Or set environment variable:
```bash
# Windows PowerShell
$env:GROQ_API_KEY="your-groq-api-key-here"

# Windows CMD
set GROQ_API_KEY=your-groq-api-key-here

# Linux/Mac
export GROQ_API_KEY='your-groq-api-key-here'
```

7. Set AI provider to Groq:
```python
# In settings.py
AI_PROVIDER = 'groq'
```

8. Restart your Django server - Done! 🎉

---

## Alternative Options

### Option 2: Hugging Face (Free)

1. Go to https://huggingface.co/
2. Sign up for free
3. Go to https://huggingface.co/settings/tokens
4. Create a new token (read access)
5. Add to settings:
```python
HUGGINGFACE_API_KEY = 'your-token-here'
AI_PROVIDER = 'huggingface'
```

### Option 3: Google Gemini (Free Tier)

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Create API key
4. Add to settings:
```python
GEMINI_API_KEY = 'your-gemini-key-here'
AI_PROVIDER = 'gemini'
```

### Option 4: Ollama (100% Free, Runs Locally)

**Best for privacy - runs on your computer!**

1. Install Ollama: https://ollama.ai
2. Download a model:
```bash
ollama pull llama2
# or
ollama pull llama3
# or
ollama pull mistral
```
3. Start Ollama (it runs automatically)
4. In settings.py:
```python
AI_PROVIDER = 'ollama'
OLLAMA_BASE_URL = 'http://localhost:11434'  # Default
```

**Note:** Ollama runs on your computer, so it's completely free and private!

---

## Quick Setup (Recommended: Groq)

1. **Install dependencies:**
```bash
pip install requests google-generativeai
```

2. **Get Groq API key:**
   - Visit: https://console.groq.com/keys
   - Sign up (free)
   - Create API key

3. **Update settings.py:**
```python
AI_PROVIDER = 'groq'  # Change from 'openai' to 'groq'
GROQ_API_KEY = 'your-groq-api-key-here'
```

4. **Restart server:**
```bash
python manage.py runserver
```

5. **Test it!** Click "Understand Solution" on any quiz question.

---

## Comparison

| Provider | Cost | Speed | Quality | Setup Difficulty |
|----------|------|-------|---------|------------------|
| **Groq** | FREE | ⚡⚡⚡ Very Fast | ⭐⭐⭐⭐ Good | ⭐ Easy |
| **Hugging Face** | FREE | ⚡⚡ Medium | ⭐⭐⭐ Good | ⭐ Easy |
| **Gemini** | FREE tier | ⚡⚡ Fast | ⭐⭐⭐⭐ Good | ⭐ Easy |
| **Ollama** | FREE | ⚡ Slow | ⭐⭐⭐ Good | ⭐⭐ Medium |
| OpenAI | Paid | ⚡⚡ Fast | ⭐⭐⭐⭐⭐ Best | ⭐ Easy |

**Recommendation:** Start with **Groq** - it's free, fast, and easy!

---

## Troubleshooting

### Groq API Error?
- Make sure you've created an API key at https://console.groq.com/keys
- Check that `AI_PROVIDER = 'groq'` in settings.py
- Verify `GROQ_API_KEY` is set correctly

### Hugging Face Slow?
- Hugging Face can be slower on first request (model loading)
- Wait 30-60 seconds for first response
- Subsequent requests are faster

### Ollama Not Working?
- Make sure Ollama is running: `ollama serve`
- Check if model is downloaded: `ollama list`
- Verify `OLLAMA_BASE_URL` is correct

---

## Need Help?

If you have issues, check:
1. API key is correct
2. `AI_PROVIDER` is set correctly in settings.py
3. Required packages are installed: `pip install requests google-generativeai`
4. Server is restarted after changes

Enjoy your FREE AI-powered quiz solutions! 🚀

