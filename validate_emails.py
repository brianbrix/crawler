import asyncio
from datetime import datetime
from functools import partial

import pandas as pd
from verify_email import verify_email, verify_email_async

import multiprocessing

from codes import EmailToName


class EMailValidate:
    """
    @:param
    """

    def __init__(self, mails_list, path):
        super(EMailValidate, self).__init__()
        self.mails_list = mails_list
        self.path2 = path
        pool = multiprocessing.Pool()
        result = pool.map(self.validate, [(k, v) for k, v in self.mails_list.items()])

    def validate(self, email):
        print(email[0])
        if len(email) == 2:
            value = verify_email(str(email[0]))
            if value:
                names = EmailToName(email[0])
                dic = {'email': email[0], "firstname": names["first_name"], "lastname": names["last_name"],
                       "way": email[1]}
                print(dic)
                df = pd.DataFrame(dic, index=["Index"])
                df.to_csv(self.path2, mode='a', header=False, index=True)
