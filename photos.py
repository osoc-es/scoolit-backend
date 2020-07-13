"""
This is the photos module and supports all the REST actions for the
photos data
"""

from flask import make_response, abort
from config import db
from models import Photo, PhotoSchema


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        json string of list of people
    """
    # Create the list of photos from our data
    photos = Photo.query.order_by(Photo.sample_id).all()

    # Serialize the data for the response
    photo_schema = PhotoSchema(many=True)
    data = photo_schema.dump(photos)
    return data


def read_one(id):
    """
    This function responds to a request for /api/photos/{id}
    with one matching photo from photos

    :param id:   Id of photo to find
    :return:            photo matching id
    """
    # Get the photo requested
    photo = Photo.query.filter(Photo.id == id).one_or_none()

    # Did we find a photo?
    if photo is not None:

        # Serialize the data for the response
        photo_schema = PhotoSchema()
        data = photo_schema.dump(photo)
        return data

    # Otherwise, nope, didn't find that photo
    else:
        abort(
            404,
            "Photo not found for Id: {id}".format(id=id),
        )


def create(photo):
    """
    This function creates a new photo in the photos structure
    based on the passed in photo data

    :param photo:  photo to create in photos structure
    :return:        201 on success, 406 on photo exists
    """
    sample_id = photo.get("sample_id")

    existing_photo = (
        Photo.query.filter(Photo.sample_id == sample_id)
        .one_or_none()
    )

    # Can we insert this photo?
    if existing_photo is None:

        # Create a photo instance using the schema and the passed in photo
        schema = PhotoSchema()
        new_photo = schema.load(photo, session=db.session)
        # Add the photo to the database
        print(new_photo)
        db.session.add(new_photo)
        db.session.commit()

        # Serialize and return the newly created photo in the response
        data = schema.dump(new_photo)

        return data, 201

    # Otherwise, nope, photo exists already
    else:
        abort(
            409,
            "Photo {sample_id} exists already".format(sample_id=sample_id)
        )


def update(id, photo):
    """
    This function updates an existing photo in the photos structure
    Throws an error if a photo with the name we want to update to
    already exists in the database.

    :param id:   Id of the photo to update in the photos structure
    :param photo:      photo to update
    :return:            updated photos structure
    """
    # Get the photo requested from the db into session
    update_photo = Photo.query.filter(Photo.id == id).one_or_none()

    # Try to find an existing photo with the same sample id as the update
    sample_id = photo.get("sample_id")

    existing_photo = (
        Photo.query.filter(Photo.sample_id == sample_id)
        .one_or_none()
    )

    # Are we trying to find a photo that does not exist?
    if update_photo is None:
        abort(
            404,
            "Photo not found for Id: {id}".format(id=id)
        )

    # Would our update create a duplicate of another photo already existing?
    elif existing_photo is not None and existing_photo.id != id:
        abort(
            409,
            "Photo {sample_id} exists already".format(sample_id=sample_id)
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in photo into a db object
        schema = PhotoSchema()
        update = schema.load(photo, session=db.session)

        # Set the id to the photo we want to update
        update.id = update_photo.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated photo in the response
        data = schema.dump(update_photo)

        return data, 200


def delete(id):
    """
    This function deletes a photo from the photos structure

    :param id:   Id of the photo to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the photo requested
    photo = Photo.query.filter(Photo.id == id).one_or_none()

    # Did we find a photo?
    if photo is not None:
        db.session.delete(photo)
        db.session.commit()
        return make_response(
            "Photo {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that photo
    else:
        abort(
            404,
            "Photo not found for Id: {id}".format(id=id),
        )