# account credentials
import email
import imaplib
from email.header import decode_header
from email.message import Message

import emoji as emoji

username = ""
password = ""
ignored = {"trash"}
output = "data.csv"

imap: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(username, password)


def write(folder: str, msg: Message) -> None:
    subject = decode("Subject", msg)
    From = decode("From", msg)
    delivered_to = decode("Delivered-To", msg)
    reply_to = decode("Reply-To", msg)
    to = decode("To", msg)
    file = open(output, "a")
    file.write(
        folder + ";" +
        clean_write(delivered_to) + ";" +
        clean_write(reply_to) + ";" +
        clean_write(to) + ";" +
        clean_write(From) + ";" +
        clean_write(subject) + "\n"
    )
    file.close()


def decode(data: str, msg: Message):
    try:
        d, encoding = decode_header(msg[data])[0]
        if isinstance(d, bytes):
            d = (d.decode(encoding) if encoding is not None else d.decode()).strip().replace('<', '').replace('>', '')
        return d
    except TypeError:
        return msg[data]


def clean_write(text: str) -> str:
    if text is None:
        return ""
    return remove_emojis(text.replace("\n", "").replace(",", ""))


def remove_emojis(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])

    return clean_text


for li in imap.list()[1]:
    folder = li.decode().split(' "/" ')[1]
    skip = False
    for ign in ignored:
        if folder.lower() in ign:
            skip = True
            break
    if skip:
        continue
    print("Reading folder " + folder)
    print("original name: " + li.decode())
    status, messages = imap.select(folder)
    print("status: " + status)
    if status != "OK":
        continue
    N = 100
    messages = int(messages[0])
    for i in range(messages, messages - N if messages > N else 0, -1):
        print("remaining mails: ", i)
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                write(folder, msg)
imap.close()
imap.logout()
