from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from quotesapp.models import Quote, Author
from quotesapp.forms import AuthorsForm, QuoteForm
from django.contrib.auth.decorators import login_required


def main(request):
    quotes_list = Quote.objects.order_by("id").all()
    paginator = Paginator(quotes_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "quotesapp/index.html",
        {
            "quotes": page_obj,
            "page_obj": page_obj,
            "is_paginated": paginator.num_pages > 1,
        },
    )


@login_required
def create_author(request):
    if request.method == "POST":
        form = AuthorsForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.user = request.user
            author.save()
            return redirect("quotesapp:main")
    else:
        form = AuthorsForm()
    return render(request, "quotesapp/author_form.html", {"form": form})


@login_required
def create_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect("quotesapp:main")
    else:
        form = QuoteForm()
    return render(request, "quotesapp/quote_form.html", {"form": form})


def about(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "quotesapp/about.html", {"author": author})
