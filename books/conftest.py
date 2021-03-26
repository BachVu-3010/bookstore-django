import pytest

from books.models import Book


@pytest.fixture(scope='function')
def add_book():
    def _add_book(title,
                  description,
                  author_name,
                  publiser_name,
                  published_date,
                  unit_price,
                  photo,
                  total_rating_value,
                  total_rating_count):
        book = Book.objects.create(title=title,
                                   description=description,
                                   author_name=author_name,
                                   publiser_name=publiser_name,
                                   published_date=published_date,
                                   unit_price=unit_price,
                                   photo=photo,
                                   total_rating_value=total_rating_value,
                                   total_rating_count=total_rating_count)
        return book
    return _add_book
