from google import genai
import os, sys, json
import urllib.request

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")

alert_data = sys.argv[1] if len(sys.argv) > 1 else '{"alert":"High CPU","value":"92%"}'

prompt = f"""
You are a DevOps incident responder.
Analyze this alert:

ALERT SUMMARY: (1 line)
ROOT CAUSE: (most likely reason)
IMMEDIATE FIX: (commands to run)
PREVENTION: (future steps)

Alert: {alert_data}
"""

response = client.models.generate_content(
    model="gemini-2.0-flash-lite-lite",
    contents=prompt
)

summary = response.text
print("AI Alert Analysis:")
print(summary)

if slack_webhook:
    message = {"text": f"🔴 *SmartOps AI Alert*\n```{summary}```"}
    data = json.dumps(message).encode("utf-8")
    req = urllib.request.Request(
        slack_webhook, data=data,
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)
    print("✅ Sent to Slack!")
