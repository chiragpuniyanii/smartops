from google import genai
import os, subprocess, sys

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

build_number = os.environ.get("BUILD_NUMBER", "unknown")
docker_image = os.environ.get("DOCKER_IMAGE", "chiragg619/nodejs-app")

try:
    diff = subprocess.check_output(
        ["git", "diff", "HEAD~1", "HEAD", "--stat"],
        stderr=subprocess.DEVNULL
    ).decode()
except:
    diff = "Could not get git diff"

review = ""
try:
    with open("ai-code-review-report.txt") as f:
        review = f.read()
except:
    review = "No review found"

prompt = f"""
You are a DevOps risk assessment AI.
Give a deployment risk score.

Build: {build_number}
Image: {docker_image}
Git Changes: {diff}
Code Review: {review}

Respond EXACTLY like this:
RISK_SCORE: (0-100)
RISK_LEVEL: (LOW / MEDIUM / HIGH)
REASONS: (3 bullet points)
RECOMMENDATION: (PROCEED / PROCEED WITH CAUTION / BLOCK)
"""

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

result = response.text
print("=" * 60)
print("AI DEPLOYMENT RISK SCORE")
print("=" * 60)
print(result)

if "RISK_LEVEL: HIGH" in result and "BLOCK" in result:
    print("❌ HIGH RISK — blocking deployment!")
    sys.exit(1)

print("✅ Risk assessment done — deployment approved.")