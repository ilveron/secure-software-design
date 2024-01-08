import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer


def test_post_title_of_length_51_raises_exception(db):
    post = mixer.blend('posts.Post', title='A'*51)
    with pytest.raises(ValidationError) as err:
        post.full_clean()
    #assert 'at most 50 characters' in '\n'.join(err.value.messages)


def test_post_title_not_capitalized_raises_exception(db):
    post = mixer.blend('posts.Post', title='my wrong title')
    with pytest.raises(ValidationError):
        post.full_clean()
