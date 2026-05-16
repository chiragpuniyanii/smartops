import google.generativeai as genai
import os, sys
from datetime import datetime

api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

status     = sys.argv[1] if len(sys.argv) > 1 else "failure"
build_num  = os.environ.get("BUILD_NUMBER", "unknown")
image      = os.environ.get("DOCKER_IMAGE", "chiragg619/nodejs-app")
timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

prompt = f"""
Generate a professional DevOps incident report in Markdown format.

Build Number : {build_num}
Status       : {status}
Docker Image : {image}
Timestamp    : {timestamp}

Include these sections:
# Incident Report — Build #{build_num}
## Summary
## Timeline
## Root Cause Analysis
## Impact
## Resolution Steps
## Prevention Measures
## Sign-off
"""

response = model.generate_content(prompt)
report = response.text

filename = f"incident-report-build-{build_num}.md"
with open(filename, "w") as f:
    f.write(report)

print(f"✅ Incident report saved → {filename}")
print(report)