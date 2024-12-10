
import enum
import logging

class TUser:

    class FunctionState(enum.IntEnum):
        Start           = 0,
        Translate       = 1,
        SelectLanguage  = 3
        Chat            = 2

    state: FunctionState = FunctionState.Start
    spokenLanguage: str = ''
    targetLanguage: str = 'English'

    firstName: str = 'N/A'
    lastName: str = 'N/A'
    userName: str = 'N/A'
    id: int = -1

    def __init__(self):
        pass

    def get_user(user):
        global users
        id = user.id
        if id in users:
            tuser = users[id]
        else:
            logging.info('TUser: doesn\'t exist, adding one')
            tuser = TUser()
            tuser.id = id
            tuser.firstName = user.first_name
            tuser.lastName = user.last_name or "N/A"  # Default if no last name
            tuser.userName = user.username or "N/A"   # Default if no username

            users[id] = tuser

        logging.info(f'tUser: {tuser.id}, {tuser.firstName}, {tuser.lastName}, {tuser.userName}')

        return tuser


users = {}