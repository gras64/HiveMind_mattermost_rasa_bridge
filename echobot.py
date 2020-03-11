from mattermost_bridge.mmost import MMostBot
from mattermost_bridge.rasa import RasaConnector
import json

####Mattermost logins
url = "chat.mycroft.ai"
mail = "user"
pswd = "xxxx"
bot = "germanbot"

####Rasalogin
rhost = "192.168.0.100"
ruser = "user"
rpswd = "xxxx"
rport = "5005"

class EchoBot(MMostBot):
    def handle_direct_message(self, message, sender, channel_id):
        self.send_message(channel_id, message)

    def handle_mention(self, message, sender, channel_id):
        #message = "@" + sender + " " + message
        print(message)
        msg = [sender, message, channel_id]
        rpaid = msg[0]
        print("send msg:"+str(msg))
        rasa = Rasa(ruser, rpswd, rhost, rport, rpaid)
        answer = rasa.send_msg(msg)
        answer = answer['text']
        print("answer: "+str(answer))
        self.send_message(channel_id, answer)

class Rasa(RasaConnector):
    def send_msg(self, msg):
        rpaid = msg[0]
        message = msg[1]
        rasa = RasaConnector(ruser, rpswd, rhost, rport, rpaid, debug=False)
        answer = rasa.talk_to_rasa(message)
        print("send to rasa message"+ str(message)+ " become: "+str(answer))
        return answer

echobot = EchoBot(mail, pswd, url, tags=["@"+bot])
echobot.driver.login()
echobot.driver.init_websocket(echobot.event_handler)