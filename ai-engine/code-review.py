from google import genai
import os, glob

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

code = ""
for f in glob.glob("app/**/*.js", recursive=True):
    with open(f) as file:
        code += f"\n\n--- File: {f} ---\n" + file.read()

if not code.strip():
    print("No JS files found.")
    exit(0)

prompt = f"""
You are a senior code reviewer.
Review this Node.js code:

WARNINGS: (security issues)
SUGGESTIONS: (improvements)
PASSED: (correct things)
SUMMARY: (2 lines)

Code:
{code[:6000]}
"""

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

print("=" * 60)
print("AI CODE REVIEW REPORT")
print("=" * 60)
print(response.text)

with open("ai-code-review-report.txt", "w") as f:
    f.write(response.text)

print("✅ Code review complete.")