"""
This is the users module and supports all the REST actions for the
users data
"""

from flask import make_response, abort
from config import db
from models import User, UserSchema


def read_all():
    """
    This function responds to a request for /api/users
    with the complete lists of users

    :return:        json string of list of users
    """
    # Create the list of users from our data
    users = User.query.order_by(User.username).all()

    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    data = user_schema.dump(users)
    return data


def read_one(id):
    """
    This function responds to a request for /api/users/{id}
    with one matching user from users

    :param id:   Id of user to find
    :return:            user matching id
    """
    # Get the user requested
    user = User.query.filter(User.id==id).one_or_none()

    # Did we find a user?
    if user is not None:

        # Serialize the data for the response
        user_schema = UserSchema()
        data = user_schema.dump(user)
        return data

    # Otherwise, nope, didn't find that user
    else:
        abort(
            404,
            "User not found for Id: {id}".format(id=id)
        )


def create(user):
    """
    This function creates a new user in the users structure
    based on the passed in user data

    :param user:  user to create in users structure
    :return:        201 on success, 406 on user exists
    """
    username = user.get("username")
    email = user.get("email")

    existing_user_username = (
        User.query.filter(User.username == username)
        .one_or_none()
    )
    existing_user_email = (
        User.query.filter(User.email == email)
        .one_or_none()
    )

    # Can we insert this user?
    if existing_user_username is None and existing_user_email is None:

        # Create a user instance using the schema and the passed in user
        schema = UserSchema()
        new_user = schema.load(user, session=db.session)
        # Add the user to the database
        print(new_user)
        db.session.add(new_user)
        db.session.commit()

        # Serialize and return the newly created user in the response
        data = schema.dump(new_user)

        return data, 201

    # Otherwise, nope, username or email exist already
    elif existing_user_email is not None:
        abort(
            409,
            "Email {email} exists already".format(email=email)
        )
        
    elif existing_user_username is not None:
        abort(
            409,
            "Username {username} exists already".format(username=username)
        )
        

def update(id, user):
    """
    This function updates an existing user in the users structure
    Throws an error if a user with the username or email we want to update to
    already exists in the database.

    :param id:   Id of the user to update in the users structure
    :param user:      user to update
    :return:            updated users structure
    """
    # Get the user requested from the db into session
    update_user = User.query.filter(User.id == id).one_or_none()

    # Try to find an existing user with the same username or email as the update
    username = user.get("username")
    email = user.get("email")

    existing_user_username = (
        User.query.filter(User.username == username)
        .one_or_none()
    )
    existing_user_email = (
        User.query.filter(User.email == email)
        .one_or_none()
    )

    # Are we trying to find a person that does not exist?
    if update_user is None:
        abort(
            404,
            "Person not found for Id: {id}".format(id=id)
        )

    # Would our update create a duplicate of another user already existing?
    elif existing_user_username is not None and existing_user_username.id != id:
        abort(
            409,
            "Username {username} exists already".format(username=username)
        )
    
    elif existing_user_email is not None and existing_user_email.id != id:
        abort(
            409,
            "Email {email} exists already".format(email=email)
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in user into a db object
        schema = UserSchema()
        update = schema.load(user, session=db.session)

        # Set the id to the user we want to update
        update.id = update_user.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated user in the response
        data = schema.dump(update_user)

        return data, 200


def delete(id):
    """
    This function deletes a user from the users structure

    :param id:   Id of the user to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the user requested
    user = User.query.filter(User.id == id).one_or_none()

    # Did we find a user?
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return make_response(
            "User {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that user
    else:
        abort(
            404,
            "User not found for Id: {id}".format(id=id),
        )