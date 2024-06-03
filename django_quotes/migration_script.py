import pymongo
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_quotes.settings")
django.setup()

from quotesapp.models import Author, Quote

MONGO_URI = "mongodb+srv://yaroshenkoyarik987:goithw@goit-web-hw.zumkrvb.mongodb.net/?retryWrites=true&w=majority&appName=goit-web-hw"
client = pymongo.MongoClient(MONGO_URI)
mongo_db = client["goit-web-hw"]

author_cache = {}

for mongo_author in mongo_db["author"].find():
    author, created = Author.objects.get_or_create(
        fullname=mongo_author["fullname"],
        defaults={
            "born_date": mongo_author.get("born_date", ""),
            "born_location": mongo_author.get("born_location", ""),
            "description": mongo_author.get("description", ""),
        },
    )
    author_cache[mongo_author["_id"]] = author

for mongo_quote in mongo_db["quote"].find():
    author = author_cache[mongo_quote["author"]]
    Quote.objects.create(
        tags=mongo_quote["tags"], author=author, quote=mongo_quote["quote"]
    )
