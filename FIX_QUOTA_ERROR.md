# Fix OpenAI API Quota Error

## Error Message
```
Error code: 429 - insufficient_quota
You exceeded your current quota, please check your plan and billing details.
```

## What This Means
Your OpenAI API key has either:
1. **No payment method attached** (MOST COMMON - even with $0 budget, you need a payment method)
2. **Exceeded the free tier credits** (if you're on a free plan)
3. **Reached the usage limit** for your current plan

## ⚠️ IMPORTANT: Even with $0 Usage, You Need Billing Setup!

If your usage page shows:
- Total Spend: $0.00
- Total Requests: 0
- But you're still getting quota errors

**This means you need to add a payment method!** OpenAI requires a payment method to be on file, even if you set spending limits to $0 or have free credits.

## How to Fix

### Option 1: Add Payment Method (REQUIRED - Do This First!)
1. Go to https://platform.openai.com/account/billing
2. Click "Add payment method" or "Go to Billing" (from the sidebar)
3. Enter your credit card details
4. **Set up spending limits** (you can set it to $5, $10, or any amount you're comfortable with)
5. Your API should work immediately after adding payment

**Note:** Even if you set a $5 limit, you MUST add a payment method first. The API won't work without it.

### Option 2: Check Usage and Limits
1. Go to https://platform.openai.com/usage
2. Check your current usage and limits
3. If you've exceeded free credits, add a payment method (Option 1)

### Option 3: Use a Different API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key (if you have multiple accounts)
3. Update it in your `settings.py` or environment variables

### Option 4: Wait for Quota Reset (Free Tier Only)
- Free tier quotas reset monthly
- Check when your quota resets at https://platform.openai.com/usage

## Cost Information
- **GPT-3.5-turbo** (used in this app): ~$0.001-0.002 per solution
- Very affordable for educational use
- You can set usage limits in OpenAI billing settings

## Quick Test
After fixing, test the API key:
```python
from openai import OpenAI
client = OpenAI(api_key="your-api-key")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

If this works, your API key is ready to use!

