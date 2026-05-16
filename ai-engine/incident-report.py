from google import genai
import os, sys
from datetime import datetime

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

status    = sys.argv[1] if len(sys.argv) > 1 else "failure"
build_num = os.environ.get("BUILD_NUMBER", "unknown")
image     = os.environ.get("DOCKER_IMAGE", "chiragg619/nodejs-app")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

prompt = f"""
Generate a DevOps incident report in Markdown.

Build : {build_num}
Status: {status}
Image : {image}
Time  : {timestamp}

Sections:
# Incident Report — Build #{build_num}
## Summary
## Timeline
## Root Cause
## Impact
## Resolution Steps
## Prevention
"""

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

report = response.text
filename = f"incident-report-build-{build_num}.md"

with open(filename, "w") as f:
    f.write(report)

print(f"✅ Incident report saved → {filename}")
print(report)