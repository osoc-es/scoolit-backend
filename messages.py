"""
This is the messages module and supports all the REST actions for the
messages data
"""

from flask import make_response, abort
from config import db
from models import Message, MessageSchema


def read_all():
    """
    This function responds to a request for /api/messages
    with the complete lists of messages

    :return:        json string of list of messages
    """
    # Create the list of messages from our data
    messages = Message.query.order_by(Message.send_date).all()

    # Serialize the data for the response
    message_schema = MessageSchema(many=True)
    data = message_schema.dump(messages)
    return data


def read_one(id):
    """
    This function responds to a request for /api/messages/{id}
    with one matching message from messages

    :param id:   Id of message to find
    :return:            message matching id
    """
    # Get the message requested
    message = Message.query.filter(Message.id == id).one_or_none()

    # Did we find a message?
    if message is not None:

        # Serialize the data for the response
        message_schema = MessageSchema()
        data = message_schema.dump(message)
        return data

    # Otherwise, nope, didn't find that message
    else:
        abort(
            404,
            "Message not found for Id: {id}".format(id=id)
        )


def create(message):
    """
    This function creates a new message in the messages structure
    based on the passed in message data

    :param message:  message to create in messages structure
    :return:        201 on success, 406 on message exists
    """

    # Create a message instance using the schema and the passed in message
    schema = MessageSchema()
    new_message = schema.load(message, session=db.session)
    # Add the message to the database
    print(new_message)
    db.session.add(new_message)
    db.session.commit()

    # Serialize and return the newly created message in the response
    data = schema.dump(new_message)

    return data, 201


def update(id, message):
    """
    This function updates an existing message in the messages structure

    :param id:   Id of the message to update in the messages structure
    :param message:      message to update
    :return:            updated messages structure
    """
    # Get the message requested from the db into session
    update_message = Message.query.filter(Message.id == id).one_or_none()

    # Are we trying to find a message that does not exist?
    if update_message is None:
        abort(
            404,
            "Message not found for Id: {id}".format(id=id)
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in message into a db object
        schema = MessageSchema()
        update = schema.load(message, session=db.session)

        # Set the id to the message we want to update
        update.id = update_message.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated message in the response
        data = schema.dump(update_message)

        return data, 200


def delete(id):
    """
    This function deletes a message from the messages structure

    :param id:   Id of the message to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the message requested
    message = Message.query.filter(Message.id == id).one_or_none()

    # Did we find a message?
    if message is not None:
        db.session.delete(message)
        db.session.commit()
        return make_response(
            "Message {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that message
    else:
        abort(
            404,
            "Message not found for Id: {id}".format(id=id),
        )