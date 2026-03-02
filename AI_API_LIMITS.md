# AI API Limits & Usage Guide

## 📊 Free Tier Limits Comparison

| Provider | Daily Limit | Rate Limit | Payment Required? | Best For |
|----------|-------------|------------|------------------|----------|
| **Groq** ⭐ | 14,400 requests/day | 600/hour | ❌ No | **Recommended - Fast & Free** |
| **Gemini** | 1,500 requests/day | 15/minute | ❌ No | Good alternative |
| **Hugging Face** | Varies | Limited | ❌ No | Backup option |
| **Ollama** | ♾️ Unlimited | None | ❌ No | Privacy-focused (local) |
| **OpenAI** | Pay-as-you-go | Based on plan | ✅ Yes | Best quality (paid) |

## 🎯 Recommended Setup: Groq

### Why Groq?
- ✅ **14,400 requests per day** - More than enough for educational use
- ✅ **No payment method needed**
- ✅ **Very fast** - Faster than OpenAI
- ✅ **Easy setup** - Just get an API key

### Daily Usage Examples:
- **100 students** × **10 solutions each** = 1,000 requests/day ✅ (Well within limit)
- **500 students** × **5 solutions each** = 2,500 requests/day ✅ (Still within limit)
- **1,000 students** × **3 solutions each** = 3,000 requests/day ✅ (Still within limit)

**You'd need 1,440+ students using 10+ solutions each to hit the limit!**

## 💡 Tips to Stay Within Limits

### 1. **Cache Solutions** (Already Implemented!)
- Solutions are saved to the database after generation
- If a solution exists, it won't call the API again
- This dramatically reduces API usage

### 2. **Use Multiple Providers**
- Set up Groq as primary
- Use Gemini as backup
- Switch providers in settings if needed

### 3. **Monitor Usage**
- Check Groq dashboard: https://console.groq.com/usage
- Monitor daily requests
- Switch to backup provider if needed

## 🔄 What Happens When You Hit Limits?

### Groq (Rate Limit):
- **Error:** "Rate limit exceeded"
- **Solution:** Wait a few minutes or switch to another provider
- **Reset:** Limits reset every hour

### Groq (Daily Limit):
- **Error:** "Daily limit exceeded"
- **Solution:** 
  1. Wait until next day (resets at midnight UTC)
  2. Switch to Gemini or another provider
  3. Use Ollama (unlimited, local)

## 🚀 Setup Multiple Providers (Backup Strategy)

```python
# In settings.py
AI_PROVIDER = 'groq'  # Primary
GROQ_API_KEY = 'your-groq-key'
GEMINI_API_KEY = 'your-gemini-key'  # Backup
```

You can modify the code to automatically fallback to Gemini if Groq fails.

## 📈 Cost Comparison (If Using Paid)

| Provider | Cost per Solution | 1,000 Solutions |
|----------|-------------------|-------------------|
| OpenAI GPT-3.5 | ~$0.001-0.002 | $1-2 |
| OpenAI GPT-4 | ~$0.03-0.06 | $30-60 |

**For educational use, free providers are more than sufficient!**

## ✅ Recommendation

**Start with Groq:**
1. Free and fast
2. 14,400 requests/day is plenty
3. No payment needed
4. Easy setup

**If you need more:**
- Add Gemini as backup (1,500/day)
- Use Ollama for unlimited (local)

## 🎓 For Your Quiz App

With solution caching (already implemented):
- First time: Calls API
- Next time: Uses saved solution (no API call)
- **This means you'll use WAY less than the limits!**

Example:
- 100 programming questions
- Each student clicks "Give Solution" once
- First student: 100 API calls
- Next 1,000 students: 0 API calls (using cached solutions)
- **Total: 100 API calls for 1,000+ students!**

## 📞 Need More?

If you're running a large institution and need higher limits:
1. Contact Groq for enterprise plans
2. Use multiple API keys (rotate them)
3. Set up Ollama for unlimited local use

---

**Bottom Line:** Groq's free tier (14,400/day) is more than enough for educational use, especially with solution caching! 🎉

