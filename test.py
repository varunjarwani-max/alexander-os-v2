import requests

print("Testing Humanities Engine...")
res1 = requests.post("http://127.0.0.1:5000/ask", json={"prompt": "Why did the Roman empire fall?"})
print(res1.json())

print("\nTesting STEM Engine Swap...")
res2 = requests.post("http://127.0.0.1:5000/ask", json={"prompt": "Calculate the velocity of a falling object."})
print(res2.json())