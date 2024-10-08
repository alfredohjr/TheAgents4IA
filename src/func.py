import requests
import datetime
import os

MODEL = 'lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf'

def now():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def read_file(file_path):
    
    text = None
    with open(file_path, 'r', encoding='utf8') as f:
        text = f.read()
    return ' '.join(text.split('\n'))


def write_file(file_path, text):
   
    with open(file_path, 'w', encoding='utf8') as f:
        f.write('\n'.join(text))

class Chat:

    def __init__(self, model=None, role_file=None):
        self.model = model if model else MODEL
        self.role_file = role_file
        self.roles = {"role": "system", "content": read_file(role_file)}
        self.baseUrl = 'http://127.0.0.1:1234'
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.__start = None
        self.__end = None
        self.__message = None
        self.__score = None
        self.__review = None

    def log(self):
        string = []
        string.append(f"Model: {self.model}")
        string.append(f"Roles: {self.roles}")
        string.append(f"Base URL: {self.baseUrl}")
        string.append(f"Response: {self.__json}")
        string.append(f"Message: {self.__message}")
        string.append(f"Start: {self.__start}")
        string.append(f"End: {self.__end}")
        string.append(f"Duration: {self.__end - self.__start}")
        string.append(f"Score: {self.__score}")
        string.append(f"Review: {self.__review}")

        if not os.path.exists(f'tmp/chat/{self.model}'):
            os.makedirs(f'tmp/chat/{self.model}')

        file_path = f'tmp/chat/{self.model}/{".".join(self.role_file.split("/")[-1].split(".")[:-1])}_{now()}.txt'
        write_file(file_path, string)

    def get_models(self):
        url = self.baseUrl + '/v1/models'
        response = requests.get(url)
        return response.json()
    
    def post_completions(self, message):
        self.__message = message
        self.__start = datetime.datetime.now()
        url = self.baseUrl + '/v1/chat/completions'
        data = {
            "model": self.model,
            "messages": [self.roles, {"role": "user", "content": self.__message}]
        }
        response = requests.post(url, headers=self.headers, json=data)
        self.__json = response.json()
        
        self.__end = datetime.datetime.now()
        return self.__json
    
    def reviewer(self):
        
        self.__score = input('0 to 10, 10 is best:')
        self.__review = input('Review:')

    def document(self):
        text = f"Q: {self.__message}\n\n"
        text += self.__json['choices'][0]['message']['content']
        if not os.path.exists(f'tmp/doc/{self.model}'):
            os.makedirs(f'tmp/doc/{self.model}')

        file_path = f'tmp/doc/{self.model}/{".".join(self.role_file.split("/")[-1].split(".")[:-1])}_{now()}.md'
        write_file(file_path, [text])

    def run(self, review=True):
        print('Chatting...')
        print(self.__json['choices'][0]['message']['content'])
        if review:
            self.reviewer()
        self.log()
        self.document()
        return self.__json