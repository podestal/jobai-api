# Fix Gemini API Key Issue

## The Problem
Your API key is being read correctly, but Google says it's invalid. This usually means:

1. **Generative Language API not enabled** - Most common issue
2. **API key restrictions** - IP/domain restrictions blocking access
3. **API key expired/revoked** - Key needs to be regenerated

## How to Fix

### Option 1: Enable Generative Language API (Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create one)
3. Go to **APIs & Services** → **Library**
4. Search for **"Generative Language API"**
5. Click on it and press **Enable**
6. Wait a few minutes for it to activate

### Option 2: Check API Key Restrictions

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Go to **APIs & Services** → **Credentials**
3. Find your API key
4. Click on it to edit
5. Under **API restrictions**, make sure:
   - Either "Don't restrict key" is selected
   - OR "Restrict key" with "Generative Language API" is enabled
6. Under **Application restrictions**, make sure it's not blocking your server

### Option 3: Regenerate API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Update your `.env` file with the new key
4. Restart your Docker container

### Option 4: Use Google AI Studio API Key

If you're using a key from Google AI Studio (makersuite.google.com), make sure:
- The key is not expired
- You're using the correct project
- The API is enabled in that project

## Test Your API Key

After fixing, test it:
```bash
docker compose exec app python -c "from apply.gemini_service import test_gemini_api_key; test_gemini_api_key()"
```

## Temporary Workaround

If you can't fix the API key right now, the resume upload will still work - it just won't parse the data automatically. You can manually populate the data later.

