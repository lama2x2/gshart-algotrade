import telebot
import data


def send_ph_net(ph):
    bt.send_photo(data.chtID, ph)


def send_ph_pc(ph):
    with open(ph, 'rb') as photo:
        bt.send_photo(data.chtID, photo)

def send_pr(pr):
    bt.send_message(data.chtID, pr)


bt = telebot.TeleBot(data.BOTTOKEN)
