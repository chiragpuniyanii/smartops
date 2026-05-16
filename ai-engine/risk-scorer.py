import google.generativeai as genai
import os, subprocess, sys

api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

build_number = os.environ.get("BUILD_NUMBER", "unknown")
docker_image = os.environ.get("DOCKER_IMAGE", "chiragg619/nodejs-app")

# Git diff lena
try:
    diff = subprocess.check_output(
        ["git", "diff", "HEAD~1", "HEAD", "--stat"],
        stderr=subprocess.DEVNULL
    ).decode()
except:
    diff = "Could not get git diff"

# Code review report padhna
review = ""
try:
    with open("ai-code-review-report.txt") as f:
        review = f.read()
except:
    review = "No code review report found"

prompt = f"""
You are a DevOps risk assessment AI.
Based on this deployment info, give a risk score.

Build Number: {build_number}
Docker Image: {docker_image}
Git Changes: {diff}
Code Review: {review}

Respond in EXACTLY this format:
RISK_SCORE: (number 0-100)
RISK_LEVEL: (LOW / MEDIUM / HIGH)
REASONS: (3 bullet points)
RECOMMENDATION: (PROCEED / PROCEED WITH CAUTION / BLOCK)
"""

response = model.generate_content(prompt)
result = response.text

print("=" * 60)
print("🎯 AI DEPLOYMENT RISK SCORE")
print("=" * 60)
print(result)
print("=" * 60)

# HIGH risk pe pipeline rok do
if "RISK_LEVEL: HIGH" in result and "BLOCK" in result:
    print("❌ HIGH RISK detected — blocking deployment!")
    sys.exit(1)

print("✅ Risk assessment complete — deployment approved.")