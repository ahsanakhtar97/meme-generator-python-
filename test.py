import google.generativeai as genai

# Configure your API key
genai.configure(api_key="AIzaSyDRfcykV09FuCT4SFoQQyO5n4aDxa6YjkY")

# List all models
models = genai.list_models()
for m in models:
    print("Name:", m.name)
    print("Available methods:", m.available_methods)
    print("---")
