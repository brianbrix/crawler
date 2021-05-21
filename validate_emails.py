from datetime import datetime
from functools import partial

import pandas as pd
from verify_email import verify_email

import multiprocessing


def validate(emails, all_data={}, path=""):
    print("verify now...")
    count=1
    for email in emails:
        value = verify_email(email)
        print(email, all_data, value)
        if value:
            if email in all_data["email"]:
                dic = {'email': email, 'link': all_data["link"], }
                df = pd.DataFrame(dic, index=[count])
                print(df)
                df.to_csv(path, mode='a', header=False)
                count+=1

    # print(ls)


def main(emails=["mokandubrian@gmail.com", "xyz231312dasdaf@gmail.com", "foo@bar.com", "ex@example.com"], all_data={},
         path=''):
    b = datetime.now()
    # pool = multiprocessing.Pool()
    # result = pool.map(partial(validate, all_data=all_data, path=path), emails)
    validate(emails=emails, all_data=all_data, path=path)
    delta = datetime.now() - b

    print(delta.total_seconds())


def verify_results(all_data, path):
    main(emails=all_data["email"], all_data=all_data, path=path)



