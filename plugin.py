from __future__ import print_function

import os
import sys
from io import BytesIO
from email_processor import Processor
import Milter

class SpamFilterMilter(Milter.Base):
    """Milter to filter spam based on ML model."""

    def __init__(self, model):  # A new instance with each new connection.
        self.id = Milter.uniqueID()  # Integer incremented with each call.
        self.prediction_model = model
        self.processor = Processor()
        self.fp = None

        self.mail_to = None
        self.mail_from = None
        self.mail_subject = None
        self.mail_date = None  # need
        self.message_id = None

        self.body = None
        self.doby_size = 0
        self.user = None

    @Milter.symlist('{auth_authen}')
    @Milter.noreply
    def envfrom(self, f, *str):
        self.mail_from = f
        self.fp = BytesIO()

        return Milter.CONTINUE

    def envrcpt(self, to, *str):
        self.mail_to = to

        return Milter.CONTINUE

    @Milter.decode('bytes')
    def header(self, name, val):
        lname = name.lower()
        if lname == 'subject':
            self.mail_subject = val
            return Milter.CONTINUE

        if lname == 'message-id' and len(val) < 4:
            self.message_id = val
            return Milter.REJECT

    def eoh(self):
        if not self.fp:
            return Milter.TEMPFAIL  # not seen by envfrom
        return Milter.CONTINUE

    def body(self, chunk):  # copy body to temp file
        if self.fp:
            self.fp.write(chunk)  # IOError causes TEMP-FAIL in milter
            self.bodysize += len(chunk)
        return Milter.CONTINUE

    def _headerChange(self, msg, name, value):
        if value:  # add header
            self.addheader(name, value)
        else:  # delete all headers with name
            h = msg.getheaders(name)
            cnt = len(h)
            for i in range(cnt, 0, -1):
                self.chgheader(name, i - 1, '')

    def eom(self):
        if not self.fp:
            return Milter.ACCEPT
        self.fp.seek(0)
        processed_email = self.processor.process_text(self.fp)
        prediction = self.prediction_model.model.prediction(processed_email)
        if prediction[0] > 0.9:
            return Milter.REJECT  # 90% confident email is spam
        return Milter.ACCEPT  # Email is not spam

    def close(self):
        sys.stdout.flush()  # make log messages visible
        if self.tempname:
            os.remove(self.tempname)  # remove in case session aborted
        if self.fp:
            self.fp.close()
        return Milter.CONTINUE

    def abort(self):
        return Milter.CONTINUE


def run_filter(my_model):
    socket_name = os.getenv("HOME") + "/pythonsock"
    print("""To use this with sendmail, add the following to sendmail.cf:
        O InputMailFilters=pythonfilter
        Xpythonfilter,        S=local:%s
        See the sendmail README for libmilter.
        sample  milter startup""" % socket_name)
    sys.stdout.flush()

    Milter.factory = SpamFilterMilter(my_model)
    Milter.set_flags(Milter.CHGBODY + Milter.CHGHDRS + Milter.ADDHDRS)

    Milter.runmilter("pythonfilter", socket_name, 240)
    print("sample milter shutdown")