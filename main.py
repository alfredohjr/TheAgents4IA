import os
from src.func import read_file, Chat

def run():

    role_file = 'roles/theDevPython.txt'

    files = []
    for file in os.listdir('roles'):
        if file.endswith('.txt'):
            files.append(file)
    
    print('Select a role file: ')
    for i in range(len(files)):
        print(f'{i+1}. {files[i]}')

    choice = int(input('Enter a number: ')) - 1
    role_file = f'roles/{files[choice]}'
    print(role_file)

    message = input('Enter a message: ')

    chat = Chat(role_file=role_file)
    chat.post_completions(message=message)
    chat.run()
    

if __name__ == "__main__":

    run()
