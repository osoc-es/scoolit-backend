"""
This is the samples module and supports all the REST actions for the
samples data
"""

from flask import make_response, abort
from config import db
from models import Sample, SampleSchema


def read_all():
    """
    This function responds to a request for /api/samples
    with the complete lists of samples

    :return:        json string of list of samples
    """
    # Create the list of samples from our data
    samples = Sample.query.order_by(Sample.isbn).all()

    # Serialize the data for the response
    sample_schema = SampleSchema(many=True)
    data = sample_schema.dump(samples)
    return data


def read_one(id):
    """
    This function responds to a request for /api/samples/{id}
    with one matching sample from samples

    :param id:   Id of sample to find
    :return:            sample matching id
    """
    # Get the sample requested
    sample = Sample.query.filter(Sample.id == id).one_or_none()

    # Did we find a sample?
    if sample is not None:

        # Serialize the data for the response
        sample_schema = SampleSchema()
        data = sample_schema.dump(sample)
        return data

    # Otherwise, nope, didn't find that sample
    else:
        abort(
            404,
            "Sample not found for Id: {id}".format(id=id),
        )


def create(sample):
    """
    This function creates a new sample in the samples structure
    based on the passed in sample data

    :param sample:  sample to create in samples structure
    :return:        201 on success, 406 on sample exists
    """
    #TODO Add code to increment book.avaible_quantity + 1
    '''
        1º Buscar book correspondiente con  sample.isbn
        2º Añadir book.avaible_quantity += 1
        3º Llamar a la funcion books.py --> update(sample.isbn, book)
    '''
    # Create a sample instance using the schema and the passed in sample
    schema = SampleSchema()
    new_sample = schema.load(sample, session=db.session)
    # Add the sample to the database
    print(new_sample)
    db.session.add(new_sample)
    db.session.commit()

    # Serialize and return the newly created sample in the response
    data = schema.dump(new_sample)

    return data, 201

def update(id, sample):
    """
    This function updates an existing sample in the samples structure

    :param id:   Id of the sample to update in the samples structure
    :param sample:      sample to update
    :return:            updated sample structure
    """
    # Get the sample requested from the db into session
    update_sample = Sample.query.filter(Sample.id == id).one_or_none()

    # Are we trying to find a sample that does not exist?
    if update_sample is None:
        abort(
            404,
            "Sample not found for Id: {id}".format(id=id),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in sample into a db object
        schema = SampleSchema()
        update = schema.load(sample, session=db.session)

        # Set the id to the sample we want to update
        update.id = update_sample.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated sample in the response
        data = schema.dump(update_sample)

        return data, 200


def delete(id):
    """
    This function deletes a sample from the samples structure

    :param id:   Id of the sample to delete
    :return:            200 on successful delete, 404 if not found
    """
    #TODO Same that cerate but deleting -1 
    # Get the sample requested
    sample = Sample.query.filter(Sample.id == id).one_or_none()

    # Did we find a sample?
    if sample is not None:
        db.session.delete(sample)
        db.session.commit()
        return make_response(
            "Sample {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that sample
    else:
        abort(
            404,
            "Sample not found for Id: {id}".format(id=id),
        )