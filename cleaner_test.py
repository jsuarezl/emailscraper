import re


def read(path: str):
    data = []
    with open(path, "r", encoding='latin-1') as file:
        for line in file.readlines():
            data.append(line.split(';'))
    return data


if __name__ == '__main__':
    dataArray = read('data.csv')
    mails: set = set()
    for entry in dataArray:
        usableEntry = entry[5]
        if re.match(r'([\w.]+@\w+\.\w{2,3})', usableEntry):
            mail = usableEntry.replace('\'', '').replace('"', '')
            if '<' in mail:
                mail = mail.split('<')[1].split('>')[0]
            if len(mail) == 0:
                continue
            if re.match(r'[\w.]+@\w+\.\w{2,3} .+', mail):
                for subMail in mail.split(' '):
                    mails.add(subMail)
            else:
                mails.add(mail)
    for mail in mails:
        print(mail)
