__author__ = 'Valery'

def private(func):
    def wrapped(bot,update, *args, **kwargs):
        if update.message.chat.type=='private':
            return func(bot,update, *args, **kwargs)
        return
    return wrapped