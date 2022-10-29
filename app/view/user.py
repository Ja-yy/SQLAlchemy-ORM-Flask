
from app.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import request,jsonify,Blueprint
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from app.schemas.UserSchemas import UserBase
from app.models.user import User
from . import auth


@auth.route("/register",methods=["POST"])
def register():
    """Api route for register user"""

    data = request.json or {}
    user_schemas = UserBase(**data)
    if User.filter(email=user_schemas.email,is_first=True):
        return jsonify({'error':'Email is taken'}),HTTP_409_CONFLICT
    
    if User.filter(username=user_schemas.username,is_first=True):
        return jsonify({'error':'Username is taken'}),HTTP_409_CONFLICT

    user_schemas.password = generate_password_hash(user_schemas.password)
    user_schemas = user_schemas.__dict__
    user_created = User.create(**user_schemas)
    return jsonify({
        'message':f'User created ',
        'user': {
            'username':user_schemas['username'],'email':user_schemas['email']
        }
    }),HTTP_201_CREATED


@auth.post("/login")
def login():
    """Api route for user login"""

    data = request.json or {}
    user_schemas = UserBase(**data)
    user = User.filter(email=user_schemas.email,is_first=True)
    if user:
        is_password_correct = check_password_hash(user.password,user_schemas.password)

        if is_password_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user':{
                    'refresh':refresh,
                    "access":access,
                    'username':user.username,
                    'email':user.email
                }
            }),HTTP_200_OK
            
    return jsonify({'error':'Wrong credentials'}),HTTP_401_UNAUTHORIZED


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    """Api route to create refresh token"""

    identity= get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access':access
    }),HTTP_200_OK


    