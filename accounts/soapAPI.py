from random import randint

from zeep import Client


class soapapi:
    basePath = "https://raygansms.com/FastSend.asmx?WSDL"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def SendMessageWithCode(self, ReciptionNumber, Code):
        client = Client(self.basePath)
        result = client.service.SendMessageWithCode(self.username, self.password, ReciptionNumber, Code)
        return result

    @staticmethod
    def send_verification_code_to_phone_number(phone_number: str = '09136025944'):
        code = randint(100000, 999999)
        msa = str("کد اعتبار سنجی شما در چمدون: " + "\n " + str(code))
        soapapi('sorushi', 'Sa129/5890*do').SendMessageWithCode(phone_number, msa)
        return code
