from tomgpt.interfaces.interface import Interface


class CMDInterface(Interface):
    def get_input(self):
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        user_input = None
        while not user_input:
            user_input = input('New Message: ')
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        return user_input
    
    def display(self, messages):
        for message in messages:
            print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
            print("{}: {}".format(message.role, message.content[0].text.value))
            print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")

        print("@!@@@@@@@@@@@@@@@@@@@@@@@!@")
        m = list(messages)[-1].content[0].text.value
        print(m)
        print("@!@@@@@@@@@@@@@@@@@@@@@@@!@")
