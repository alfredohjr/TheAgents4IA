import os
from src.func import read_file, Chat

def run():

    files = []
    for file in os.listdir('data/roles'):
        if file.endswith('.txt'):
            files.append(file)
    
    print('Select a role file: ')
    for i in range(len(files)):
        print(f'{i+1}. {files[i]}')

    choice = int(input('Enter a number: ')) - 1
    role_file = f'data/roles/{files[choice]}'
    print(role_file)

    print('Options:')
    print('1. Enter a message')
    print('2. Enter message using a file')
    print('99. Exit')
    option = input('Enter a number: ')

    option = option.strip()
    if option == '1':
        message = input('Enter a message: ')
    elif option == '2':
        file = input('Enter the file path: ')
        if not os.path.exists(file):
            raise Exception(f"File {file} not found.")
        message = read_file(file)

    if option != '99':
        chat = Chat(role_file=role_file)
        review = True if len(message.split('--[END]--')) == 1 else False
        for m in message.split('--[END]--'):
            chat.post_completions(message=m)
            chat.run(review=review)
    

if __name__ == "__main__":

    run()
