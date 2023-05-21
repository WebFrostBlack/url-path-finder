import os
import requests
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

valid_urls = []

def show_txt_files():
    base_path = os.path.dirname(os.path.abspath(__file__))
    txt_dir = os.path.join(base_path, 'txt')
    files = [f for f in os.listdir(txt_dir) if os.path.isfile(os.path.join(txt_dir, f)) and f.endswith('.txt')]
    print('Fichiers .txt disponibles :')
    for i, f in enumerate(files):
        print(f'[{i+1}] {f}')
    return txt_dir, files

def test_url(url, path):
    full_url = f'{url}/{path.strip()}'
    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            print(colored('Success [' + str(response.status_code) + ']: ' + full_url, 'green'))
            valid_urls.append(full_url)
        else:
            print(colored('Error   [' + str(response.status_code) + ']: ' + full_url, 'red'))
    except:
        print(colored(f'Error: {full_url}', 'red'))

def test_all_paths(url):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-?!*'
    paths = []
    for i in range(len(chars)):
        paths.append(chars[i])
        for j in range(len(chars)):
            paths.append(f'{chars[i]}{chars[j]}')
            for k in range(len(chars)):
                paths.append(f'{chars[i]}{chars[j]}{chars[k]}')
    with ThreadPoolExecutor(max_workers=20) as executor:
        for path in paths:
            executor.submit(test_url, url, path)
    write_valid_urls(url, valid_urls)

def write_valid_urls(url, valid_urls):
    base_path = os.path.dirname(os.path.abspath(__file__))
    valid_dir = os.path.join(base_path, 'valid_urls')
    if not os.path.exists(valid_dir):
        os.mkdir(valid_dir)
    filename = url.split('//')[1].replace('/', '_') + '.txt'
    file_path = os.path.join(valid_dir, filename)
    with open(file_path, 'w') as f:
        for valid_url in valid_urls:
            f.write(valid_url + '\n')
    print(f'Successfully saved valid URLs to {file_path}')

if __name__ == '__main__':
    input('Crédit FrostBlack ! [Press Enter] ')
    os.system("cls")
    url = input('Enter the URL to test : ')
    if not url.startswith('http://') and not url.startswith('https://'):
        url = f'https://{url}'
        os.system("cls")
    option = input("Test with your .txt [1] | Test with all possibilities [2]\n")
    if option == '1':
        txt_dir, files = show_txt_files()
        file_index = int(input('Enter the file number to use : '))
        file_path = os.path.join(txt_dir, files[file_index-1])
        with open(file_path, 'r') as f:
            words = f.read().split()
        with ThreadPoolExecutor(max_workers=20) as executor:
            for word in words:
                executor.submit(test_url, url, word)
        write_valid_urls(url, valid_urls)
    elif option == '2':
        test_all_paths(url)
    else:
        print('invalid option')
