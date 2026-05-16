import google.generativeai as genai
import os, glob

api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Saare JS files padhna
code = ""
for f in glob.glob("app/src/**/*.js", recursive=True):
    with open(f) as file:
        code += f"\n\n--- File: {f} ---\n" + file.read()

if not code.strip():
    print("No JS files found to review.")
    exit(0)

prompt = f"""
You are a senior DevOps and backend code reviewer.
Review this Node.js code and give feedback in this exact format:

WARNINGS: (security issues, missing validations)
SUGGESTIONS: (improvements, best practices)
PASSED: (things done correctly)
SUMMARY: (2 lines overall assessment)

Code to review:
{code[:8000]}
"""

response = model.generate_content(prompt)
result = response.text

print("=" * 60)
print("🤖 AI CODE REVIEW REPORT")
print("=" * 60)
print(result)
print("=" * 60)

# Report file mein save karo
with open("ai-code-review-report.txt", "w") as f:
    f.write(result)

print("✅ Code review complete — report saved.")