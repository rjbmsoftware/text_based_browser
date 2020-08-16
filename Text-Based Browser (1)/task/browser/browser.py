import sys
import os
import requests
from bs4 import BeautifulSoup, Tag
from requests import Response
from colorama import Fore, Style


def is_valid_url(url: str) -> bool:
    return url.find('.') != -1


def setup_tab_directory(directory_name: str) -> str:
    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)

    return f'{os.getcwd()}{os.path.sep}{directory_name}'


def save_tab(url: str, save_to_directory: str, page_text: str) -> None:
    with open(f'{save_to_directory}{os.path.sep}{url}', 'w') as tab:
        tab.write(page_text)


def simplified_url(url: str) -> str:
    return url[:url.rindex('.')]


def list_cached_pages(cache_page_path: str) -> []:
    return os.listdir(cache_page_path)


def print_cached_page(cache_page_path: str, url: str) -> None:
    with open(f'{cache_page_path}{os.path.sep}{url}') as file:
        for line in file:
            print(line.replace('\n', ''))
    print('from cache')


def back() -> None:
    if page_history:
        page_history.pop()  # remove current page from top
        if page_history:
            if current_page != page_history[-1]:
                print_cached_page(save_directory, page_history[-1])
            page_history.pop()


save_directory = setup_tab_directory(sys.argv[1])
# save_directory = setup_tab_directory('tabs')  # local testing

user_url = input()
page_history = []
current_page = ''


def style_text(tag: Tag) -> str:
    return f'{Fore.BLUE}{tag.text}{Style.RESET_ALL}' if tag.name == 'a' else tag.text


def build_filtered_content(response: Response) -> str:
    soup = BeautifulSoup(response.content.decode(response.encoding), 'html.parser')
    filtered_tags = soup.find_all(['title', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
    return ''.join(style_text(tag) for tag in filtered_tags)


def navigate(url: str) -> None:
    https = 'https://'
    tls_url = url
    if not tls_url.startswith(https):
        tls_url = https + url

    response = requests.get(tls_url)
    simple_url = simplified_url(user_url)

    if response:
        body = build_filtered_content(response)
        page_history.append(simple_url)
        save_tab(url, save_directory, body)
        print(body)


while user_url != 'exit':
    cached_page_titles = list_cached_pages(save_directory)
    if user_url == 'back':
        back()
    elif user_url in cached_page_titles:
        print_cached_page(save_directory, user_url)
        page_history.append(user_url)
        current_page = user_url
    elif is_valid_url(user_url):
        navigate(user_url)
        current_page = simplified_url(user_url)
    else:
        print('error invalid URL')

    user_url = input()
