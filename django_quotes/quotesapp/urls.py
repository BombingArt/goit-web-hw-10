from django.urls import path
from quotesapp import views

app_name = "quotesapp"

urlpatterns = [
    path("", views.main, name="main"),
    path("author/", views.create_author, name="add_author"),
    path("quote/", views.create_quote, name="add_quote"),
    path("author/<int:author_id>/", views.about, name="about"),
]
