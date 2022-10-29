
from app.constants.http_status_code import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from flask import request,jsonify,redirect,Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.models.bookmarks import Bookmarks
from app.schemas.BookmarkSchemas import BookmarkCreate, Bookmark
from app.schemas.BookmarkSchemas import Bookmark as bookmarkschem
from . import bookmarks



@bookmarks.route("/",methods=['POST'])
@jwt_required()
def add_bookmark():
    """Apis route for add bookmark"""

    data = request.json or {}
    bookmark_schema = BookmarkCreate(**data)
    test_vookmark  = Bookmarks.filter(url=bookmark_schema.url,is_first=True)
    print("test_vookmark----------------->",test_vookmark)
    if test_vookmark:
            return jsonify({
            'error':"URL already exists"
        }),HTTP_409_CONFLICT
    current_user= get_jwt_identity()
    bookmark_schema_dict = bookmark_schema.__dict__
    bookmark_schema_dict.update({"user_id":current_user})
    bookmark_schema_instance = Bookmarks.create(**bookmark_schema_dict)
    return jsonify({
                       'id':bookmark_schema_instance.id,
                       'url':bookmark_schema_instance.url,
                       'short_url':bookmark_schema_instance.short_url,
                       'visit':bookmark_schema_instance.visits,
                       'body':bookmark_schema_instance.body,
                       'created_at':bookmark_schema_instance.created_at,
                       'upadted_at':bookmark_schema_instance.updated_at })

@bookmarks.route("/", methods=['GET'])
@jwt_required()
def get_all_bookmarks():
    """Apis route for get all bookmarks"""
    current_user = get_jwt_identity()
    bookmarks = Bookmarks.filter(user_id=current_user)
    if not bookmarks:
        return jsonify({
            'error':'Item not found'
        }),HTTP_404_NOT_FOUND
    bookmarks_list=[]
    for bookmark in bookmarks:
        bookmarks_list.append({
            'id':bookmark.id,
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'visit':bookmark.visits,
            'body':bookmark.body,
            'created_at':bookmark.created_at,
            'upadted_at':bookmark.updated_at
        })


    return jsonify(bookmarks_list),HTTP_200_OK


@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmarks(id):
    """Apis route for get bookmarks with particular id"""

    current_user = get_jwt_identity()
    bookmark = Bookmarks.filter(id=id,is_first=True)

    if not bookmark:
        return jsonify({
            'error':'Item not found'
        }),HTTP_404_NOT_FOUND

    return jsonify({
            'id':bookmark.id,
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'visit':bookmark.visits,
            'body':bookmark.body,
            'created_at':bookmark.created_at,
            'upadted_at':bookmark.updated_at
        }),HTTP_200_OK


@bookmarks.put("/<int:id>")
@jwt_required()
def edit_bookmarks(id):
    """Api route for update bookmark"""

    data = request.json or {}
    bookmark_schema = bookmarkschem(**data)
    current_user = get_jwt_identity()
    bookmark = Bookmarks.filter(id=id,user_id=current_user,is_first=True)

    if not bookmark:
        return jsonify({
            'error':'Item not found'
        }),HTTP_404_NOT_FOUND
    updated_bookmark_schema = bookmark_schema.dict()
    updated_bookmark = Bookmarks.update(uid=id, **updated_bookmark_schema)

    return jsonify({
            'id':updated_bookmark.id,
            'url':updated_bookmark.url,
            'short_url':updated_bookmark.short_url,
            'visit':updated_bookmark.visits,
            'body':updated_bookmark.body,
            'created_at':updated_bookmark.created_at,
            'upadted_at':updated_bookmark.updated_at
        }),HTTP_200_OK


@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmarks(id):
    """Api route for delete bookmark"""

    current_user = get_jwt_identity()
    bookmark = Bookmarks.filter(id=id,user_id=current_user,is_first=True)
    if not bookmark:
        return jsonify({
            'error':'Item not found'
        }),HTTP_404_NOT_FOUND

    Bookmarks.delete(uid=id)
    return jsonify({}),HTTP_204_NO_CONTENT

@bookmarks.get('/<short_url>')
# @jwt_required()
def redirect_url(short_url):
    """Api route for redirect to bookmark"""

    bookmark = Bookmarks.filter(short_url=short_url,is_first=True)
    if bookmark:
        bookmark.add_visit_count(bookmark=bookmark)
        return redirect(bookmark.url),HTTP_200_OK

@bookmarks.get('/stats')
@jwt_required()
def get_stats():
    """Api route for stats of bookmark"""
    current_user = get_jwt_identity()
    data =[]
    items = Bookmarks.filter(user_id=current_user)
    
    for item in items:
        data.append({
            'visits':item.visits,
            'url':item.url,
            'id':item.id,
            'short_url':item.short_url
        })

    return jsonify(data)


@bookmarks.errorhandler(HTTP_404_NOT_FOUND)
def handle_404(e):
    return jsonify({'error':'Not Found'}),HTTP_404_NOT_FOUND


@bookmarks.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def handle_404(e):
    return jsonify({'error':'Something went wrong,we are working on it'}),HTTP_500_INTERNAL_SERVER_ERROR