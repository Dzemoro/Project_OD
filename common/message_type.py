import enum

class MessageType(enum.Enum):
    JOIN = 0
    LIST = 1
    QUIT = 2
    GIVE = 3
    SPOX = 4
    DENY = 5
    MESS = 6
    KEYS = 7
    CONN = 8
    CALL = 9
    KEYR = 10
    LEAV = 11
    LEAR = 12