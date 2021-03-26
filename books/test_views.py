import json

import pytest

from .models import Book


@pytest.mark.django_db
def test_add_book_invalid_json(client):
    books = Book.objects.all()
    assert len(books) == 0

    resp = client.post(
        "/api/v1/books/",
        {},
        content_type="application/json"
    )
    assert resp.status_code == 400

    books = Book.objects.all()
    assert len(books) == 0


@pytest.mark.django_db
def test_add_book_invalid_json_keys(client):
    books = Book.objects.all()
    assert len(books) == 0

    resp = client.post(
        "/api/v1/books/",
        {
            "title": "Harry Potter",
            "genre": "comedy",
        },
        content_type="application/json"
    )
    assert resp.status_code == 400

    books = Book.objects.all()
    assert len(books) == 0


@pytest.mark.django_db
def test_add_book(client):
    books = Book.objects.all()
    assert len(books) == 0

    resp = client.post(
        "/api/v1/books/",
        {
            "title": "Harry Potter and the Deathly Hallows",
            "description": "Harry Potter and the Deathly Hallows is a fantasy novel \
                    written by British author J. K. Rowling and the seventh and \
                    final novel of the Harry Potter series.",
            "author_name": "J. K. Rowling",
            "publiser_name": "Bloomsbury Publishing",
            "published_date": "2007-07-21",
            "unit_price": 29.99,
            "photo": "a",
            "total_rating_value": 4.5,
            "total_rating_count": 10000,
        },
        content_type="application/json"
    )
    assert resp.status_code == 201
    assert resp.data["title"] == "Harry Potter and the Deathly Hallows"

    books = Book.objects.all()
    assert len(books) == 1


@pytest.mark.django_db
def test_get_single_book(client, add_book):
    # book = Book.objects.create(
    #     title="Harry Potter and the Deathly Hallows",
    #     description="Harry Potter and the Deathly Hallows is a fantasy novel \
    #                 written by British author J. K. Rowling and the seventh and \
    #                 final novel of the Harry Potter series.",
    #     author_name="J. K. Rowling",
    #     publiser_name="Bloomsbury Publishing",
    #     published_date="2007-07-21",
    #     unit_price=29.99,
    #     photo="a",
    #     total_rating_value=4.5,
    #     total_rating_count=10000)
    book = add_book(
        title="Harry Potter and the Deathly Hallows",
        description="Harry Potter and the Deathly Hallows is a fantasy novel \
                    written by British author J. K. Rowling and the seventh and \
                    final novel of the Harry Potter series.",
        author_name="J. K. Rowling",
        publiser_name="Bloomsbury Publishing",
        published_date="2007-07-21",
        unit_price=29.99,
        photo="a",
        total_rating_value=4.5,
        total_rating_count=10000)

    resp = client.get(f"/api/v1/books/{book.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "Harry Potter and the Deathly Hallows"


def test_get_single_book_incorrect_id(client):
    resp = client.get(f"/api/v1/books/foo/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_all_books(client, add_book):
    book_one = add_book(
        title="Harry Potter and the Deathly Hallows",
        description="Harry Potter and the Deathly Hallows is a fantasy novel \
                    written by British author J. K. Rowling and the seventh and \
                    final novel of the Harry Potter series.",
        author_name="J. K. Rowling",
        publiser_name="Bloomsbury Publishing",
        published_date="2007-07-21",
        unit_price=29.99,
        photo="a",
        total_rating_value=4.5,
        total_rating_count=10000)
    book_two = add_book(
        title="Harry Potter and the Deathly Hallows",
        description="Harry Potter and the Deathly Hallows is a fantasy novel \
                    written by British author J. K. Rowling and the seventh and \
                    final novel of the Harry Potter series.",
        author_name="J. K. Rowling",
        publiser_name="Bloomsbury Publishing",
        published_date="2007-07-21",
        unit_price=29.99,
        photo="a",
        total_rating_value=4.5,
        total_rating_count=10000)

    resp = client.get(f"/api/v1/books/")
    assert resp.status_code == 200
    assert resp.data[0]["title"] == book_one.title
    assert resp.data[1]["title"] == book_two.title
