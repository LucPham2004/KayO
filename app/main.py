import google.generativeai as genai

genai.configure(api_key="well, it is secret")

model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content("quản lý dự án có những kiến thức nào trọng tâm?")
print(response.text)