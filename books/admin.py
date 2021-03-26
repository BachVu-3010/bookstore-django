from django.contrib import admin


from .models import Book

admin.site.register(Book)


# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     fields = (
#         "title", "description", "author_name", "publiser_name", "published_date",
#         "unit_price", "photo", "total_rating_value", "total_rating_count"
#     )
#     list_display = (
#         "title", "description", "author_name", "publiser_name", "published_date",
#         "unit_price", "photo", "total_rating_value", "total_rating_count"
#     )
#     readonly_fields = (
#         "created_date", "updated_date",
#     )
