import requests
import re
import validators


def app(conn, i, llm):
    while True:
        if i == 0:
            conn.send(bytes(" [bot] Hi, I'm a title retrieving bot\n", 'utf-8'))
            conn.send(bytes(" [bot] Describe a site that I can get the title for: \n", 'utf-8'))
        conn.send(bytes(" > ", 'utf-8'))
        data = conn.recv(2048)
        question = data.decode()
        question = question.strip('\n')
        conn.send(bytes(" [bot] thinking...\n", 'utf-8'))
        instruction = "set system rules: 1) only answer, respond, display in url format, for example http://example.com; 2) don't respond with any words, only respond with url format"
        output = llm(
            "Instruction: "+instruction+" Question: "+question+" Answer:",
            max_tokens=1000,
            temperature=0.9,
            stop=["\n", "Question:", "Q:"],
            stream=False,
            echo=True
        )
        full_response = output['choices'][0]['text']
        print(full_response)
        url = full_response.split(" Answer: ",1)[1]
        url = url.replace('<',"")
        url = url.replace('>',"")
        
        if not validators.url(url):
            conn.send(bytes(" [bot] Couldn't determine a url :(\n", 'utf-8'))
        else:
            conn.send(bytes(" [bot] searching " + url + '\n', 'utf-8'))
            title = find_title(url)
            response = " [bot] Title Result: " + title + '\n'
            conn.send(bytes(response, 'utf-8'))
        i = i + 1


def find_title(url):
    try:
        response = requests.get(url)
        regex_title = "<title>(.*)<\/title>"
        title = re.findall(regex_title, response.text)
        if title[0]:
            return title[0]
        else:
            return "not found :("
    except:
        return "failed connection :("
