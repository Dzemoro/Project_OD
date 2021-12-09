import enum

class MessageType(enum.Enum):
    JOIN = 0
    LIST = 1
    QUIT = 2
    GIVE = 3
    SPOX = 4
    DENY = 5