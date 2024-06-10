import time
import uuid


class Utilities:

    @staticmethod
    def generateUUID():
        return str(uuid.uuid4())

    @staticmethod
    def generateTimestampId():
        return int(round(time.time() * 1000))


