import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

config = {
    "default": DevelopmentConfig,
    "debug": False, 
    "enbale_phone_message": False,
    "contacts": [
        "13078990668"
    ], 
    "api": {
        "message_url": "http://127.0.0.1/api/message/", 
        "call_url": "http://127.0.0.1/api/call/", 
        "token": "zjhkwxx0214.C7q7ow.VtSgIJmr8QZfJPddoAMDDhK254Y"
    }, 
    "products": {
        # "radar": {
        #     "prd_type": "radar",
        #     "login": [
        #         "192.2.204.229", 
        #         "administrator", 
        #         "haikou4100", 
        #         "/data/IPZ"
        #     ], 
        #     "platform": "win", 
        #     "time_offset": 0, 
        #     "warn_time": 180, 
        #     "default_warn_messages": "RADAR ALARM!"
        # }, 
        # "satellite": {
        #     "prd_type": "satellite",
        #     "login": [
        #         "192.2.204.51", 
        #         "zjhk", 
        #         "zjhk", 
        #         "/"
        #     ], 
        #     "platform": "linux", 
        #     "time_offset": 0, 
        #     "warn_time": 60, 
        #     "default_warn_messages": "SATELLITE ALARM!"
        # }, 
        # "awos": {
        #     "prd_type": "awos",
        #     "login": [
        #         "172.22.82.2", 
        #         "comm", 
        #         "comm123", 
        #         "/home/comm/temp/awos"
        #     ], 
        #     "platform": "linux", 
        #     "time_offset": 8, 
        #     "warn_time": 3, 
        #     "default_warn_messages": "AWOS ALARM!"
        # }
        # "test-r":{
        #     "prd_type":"radar",
        #     "login":[
        #         "10.0.0.5",
        #         "Xiaoxiao Wang",
        #         "wxx",
        #         "/Users/Xiao/Desktop/test/radar"
        #         ],
        #     "platform": "win", 
        #     "time_offset": 8, 
        #     "warn_time": 3, 
        #     "default_warn_messages": "radar ALARM!"
        # },
        "test-a":{
            "prd_type":"awos",
            "login":[
                "192.168.11.103",
                "Xiaoxiao Wang",
                "wxx",
                "/Users/Xiao/Desktop/test/awos"
                ],
            "platform": "linux", 
            "time_offset": 8, 
            "warn_time": 3, 
            "default_warn_messages": "awos ALARM!"
        },
        # "test-s":{
        #     "prd_type":"satellite",
        #     "login":[
        #         "10.0.0.5",
        #         "Xiaoxiao Wang",
        #         "wxx",
        #         "/Users/Xiao/Desktop/test/sat"
        #         ],
        #     "platform": "linux", 
        #     "time_offset": 8, 
        #     "warn_time": 3, 
        #     "default_warn_messages": "satellite ALARM!"
        # }
    }
}