from flask import Blueprint

bookmarks = Blueprint('bookmarks',__name__,url_prefix="/api/v1/bookmarks")
auth = Blueprint('auth',__name__,url_prefix="/api/v1/auth")
