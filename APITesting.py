import requests

url = "http://127.0.0.1:5000/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

history = []

while True:
    user_message = input("> ")
    if user_message.lower() == "quit":
        break
    else:
        history.append({"role": "user", "content": user_message})
        data = {
            "mode": "chat",
            "character": "C.A.I.S.E",
            "messages": history
        }   

    response = requests.post(url, headers=headers, json=data, verify=False)
    assistant_message = response.json()['choices'][0]['message']['content']
    history.append({"role": "assistant", "content": assistant_message})
    print(assistant_message)