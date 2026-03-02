# Quick Fix: Add Payment Method to OpenAI

## The Problem
You're seeing "insufficient_quota" error even though you have $0 usage. This is because **OpenAI requires a payment method to be on file**, even if you haven't used any credits yet.

## The Solution (2 Minutes)

### Step 1: Go to Billing
1. Click the **"Go to Billing"** button in the left sidebar (under "Add credits")
   - OR go directly to: https://platform.openai.com/account/billing

### Step 2: Add Payment Method
1. Click **"Add payment method"** or **"Set up billing"**
2. Enter your credit card information:
   - Card number
   - Expiry date
   - CVV
   - Billing address

### Step 3: Set Spending Limits (Optional but Recommended)
1. Go to **"Limits"** in the left sidebar
2. Set a **hard limit** (e.g., $5, $10, $20 per month)
3. This prevents unexpected charges

### Step 4: Test Your API
After adding payment, your API key will work immediately. You can test it:
- Try the "Understand Solution" button in your quiz app
- Or test directly in Python (see below)

## Cost Information
- **GPT-3.5-turbo**: ~$0.001-0.002 per solution
- **Very affordable**: 500-1000 solutions for just $1
- You can set limits to control spending

## Test Your API Key (After Adding Payment)

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key-here")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Say hello"}]
)
print(response.choices[0].message.content)
```

If this works, your API is ready!

## Still Having Issues?

1. **Check your API key** is correct in settings.py
2. **Wait 1-2 minutes** after adding payment (sometimes takes a moment to activate)
3. **Check billing status** at https://platform.openai.com/account/billing
4. **Verify payment method** is active and not expired

## Alternative: Use Free Tier (If Available)
Some accounts get free tier credits. Check:
- https://platform.openai.com/usage
- Look for "Free tier credits" or similar

But even free tier often requires a payment method on file!

