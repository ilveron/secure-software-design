import json

import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from rest_framework.test import APIClient


@pytest.fixture()
def posts(db):
    return [
        mixer.blend('posts.Post'),
        mixer.blend('posts.Post'),
        mixer.blend('posts.Post'),
    ]


def get_client(user=None):
    res = APIClient()
    if user is not None:
        res.force_login(user)
    return res


def parse(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)


def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]


def test_post_anon_user_get_nothing():
    path = reverse('posts-list')
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_403_FORBIDDEN
    assert contains(response, 'detail', 'credentials were not provided')


def test_post_user_get_list(posts):
    path = reverse('posts-list')
    user = mixer.blend(get_user_model())
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(posts)


def test_post_retrieve_a_single_post(posts):
    path = reverse('posts-detail', kwargs={'pk': posts[0].pk})
    client = get_client(posts[0].author)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert obj['title'] == posts[0].title
