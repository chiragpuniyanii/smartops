import google.generativeai as genai
import os, json, sys
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import urllib.request

api_key = os.environ.get("GEMINI_API_KEY")
slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Alert data stdin se ya argument se lo
alert_data = sys.argv[1] if len(sys.argv) > 1 else '{"alert": "High CPU usage on prod-server-01", "value": "92%"}'

prompt = f"""
You are a DevOps incident responder AI.
Analyze this Prometheus alert and respond in this format:

ALERT SUMMARY: (1 line what happened)
ROOT CAUSE: (most likely cause)
IMMEDIATE FIX: (step by step commands to fix)
PREVENTION: (how to prevent this in future)

Alert data: {alert_data}
"""

response = model.generate_content(prompt)
summary = response.text

print("🤖 AI Alert Analysis:")
print(summary)

# Slack pe bhejo
if slack_webhook:
    message = {
        "text": f"🔴 *SmartOps Alert — AI Analysis*\n```{summary}```"
    }
    data = json.dumps(message).encode("utf-8")
    req = Request(slack_webhook, data=data,
                  headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)
    print("✅ Alert summary sent to Slack!")
else:
    print("⚠ SLACK_WEBHOOK_URL not set — skipping Slack notification")