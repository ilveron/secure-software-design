import requests


def main():
    welcome()
    posts = fetch_posts()
    if posts is None:
        error_message()
    show_posts(posts)
    goodbye()


def fetch_posts():
    res = requests.get(url='http://localhost:8000/api/v1/')
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


if __name__ == '__main__':
    main()
