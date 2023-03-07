from __future__ import print_function
import Milter


# import syslog

# TODO: add function to preprocess email for the model
def pre_process_email(email):
    return "0,0,0,0,0"


# TODO: add function to send preprocessed email to the model for prediction
def predict_spam(email):
    bool = False
    if bool:
        return Milter.DISCARD
    else:
        return Milter.CONTINUE


class SpamFilterMilter(Milter.Base):
    """Milter to filter spam based on ML model."""

    def __init__(self):  # A new instance with each new connection.
        self.id = Milter.uniqueID()  # Integer incremented with each call.
