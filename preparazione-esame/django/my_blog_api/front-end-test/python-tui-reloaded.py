import requests
import getpass

API_SERVER = 'http://localhost:8000/api/v1'

def main():
    welcome()
    key = login()
    if key is None:
        error_message()
    posts = fetch_posts(key)
    if posts is None:
        error_message()
    show_posts(posts)
    logout(key)
    goodbye()


def fetch_posts(key):
    res = requests.get(url=f'{API_SERVER}/posts/', headers={'Authorization': f'Token {key}'})
    if res.status_code != 200:
        return None
    return res.json()


def welcome():
    print('Hello, Welcome to the Python TUI')


def error_message():
    print('There was an error fetching the posts')


def goodbye():
    print('Goodbye, see you next time!')


def show_posts(posts):
    def sep():
        print('-' * 60)

    fmt = '{:4}\t{:50}'

    print()
    sep()
    print('ALL POSTS FROM THE BLOG')
    sep()
    print(fmt.format('ID', 'TITLE'))
    for post in posts:
        print(fmt.format(post['id'], post['title']))
    sep()
    print()


def login():
    username = input('Username: ')
    password = getpass.getpass('Password: ')

    res = requests.post(url=f'{API_SERVER}/auth/login/', data={'username': username, 'password': password})
    if res.status_code != 200:
        return None
    json = res.json()
    return json['key']


def logout(key):
    res = requests.post(url=f'{API_SERVER}/auth/logout/', headers={'Authorization': f'Token {key}'})
    if res.status_code == 200:
        print('Logged out!')
    else:
        print('Log out failed')
    print()


if __name__ == '__main__':
    main()
