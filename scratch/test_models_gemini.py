import urllib.request, urllib.error, json

GEMINI_KEY = "AIzaSyAGFp6PVh2VrnLOw6tk_jcz5hXjccGaTDM"
models_to_test = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-2.0-flash-lite",
    "gemini-flash-lite-latest",
    "gemma-3-4b-it",
]

test_body = {
    "contents": [{"parts": [{"text": "Return JSON array: [{\"id\": 1, \"test\": \"ok\"}]"}]}],
    "generationConfig": {"responseMimeType": "application/json"}
}

print("Testing Gemini models...")
for model in models_to_test:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
    req = urllib.request.Request(url, data=json.dumps(test_body).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"  OK  : {model}")
    except urllib.error.HTTPError as e:
        print(f"  {e.code} : {model}")
    except Exception as e:
        print(f"  ERR : {model} ({type(e).__name__})")
