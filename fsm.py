from transitions.extensions import GraphMachine
from utils import spider,send_text_message,send_button_message,is_number


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
        self.in_bot_flag = True
        self.tag = ""
        self.upper = 1

    def is_going_to_state1(self, event):
        if event.get("message"):
            text = event['message']['text']
            if text == 'restart':
                self.in_bot_flag = True
            return text.lower() == '搜尋' and self.in_bot_flag
        return False

    def is_going_to_state2(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '關閉' and self.in_bot_flag
        return False

    def is_going_to_state4(self, event):
        sender_id = event['sender']['id']
        if event.get("message"):
            text = event['message']['text']
            if is_number(text):
                return True
            else:
                responese = send_text_message(sender_id, "輸入錯誤！請輸入正整數")
        return False

    def is_going_to_state5(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'help' and self.in_bot_flag
        return False

    def is_going_to_state6(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'iloveyou' and self.in_bot_flag
        return False    

    def on_enter_state1(self, event):
        print("I'm entering state1")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "請輸入關鍵字")

    def on_exit_state1(self,event):
        print("input tag")
        sender_id = event['sender']['id']
        text = event['message']['text']
        self.tag = text
        print('Leaving state1')

    def on_enter_state2(self, event):
        print("I'm entering state2")

        sender_id = event['sender']['id']
        send_button_message(sender_id,"確定要關閉BOT嗎？")

    def on_exit_state2(self,event):
        print('Leaving state2')
        sender_id = event['sender']['id']
        text = event['postback']['payload']
        if text=='YES':
            self.in_bot_flag = False
            responese = send_text_message(sender_id, "已關閉，直到輸入restart再次開啟")
            print('close bot')
        else:
            print('do not close')
            
    def on_enter_state3(self, event):
        print("I'm entering state1")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "請輸入顯示貼文數的上限")

    def on_exit_state3(self,event):
        print("input upper")
        sender_id = event['sender']['id']
        text = event['message']['text']
        self.upper = int(text)
        #responese = send_text_message(sender_id, text)
        print('Leaving state3')
        
    def on_enter_state4(self, event):
        print("I'm entering state2")

        sender_id = event['sender']['id']
        send_button_message(sender_id,"確定輸入值為{0}，顯示上限為{1}？".format(self.tag, self.upper))

    def on_exit_state4(self,event):
        print('Leaving state4')
        sender_id = event['sender']['id']
        text = event['postback']['payload']
        if text=='YES':
            spider(sender_id,self.upper,self.tag)
            print('spider!')
        else:
            responese = send_text_message(sender_id, "請重新操作")

    def on_enter_state5(self, event):
        print("I'm entering state5")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "輸入<搜尋>開始使用搜尋服務\n\n輸入<關閉>來結束搜尋服務\n\n")
        self.go_back(event)

    def on_exit_state5(self,event):
        print('Leaving state5')

    def on_enter_state6(self, event):
        print("I'm entering state6")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "i love you too")
        self.go_back(event)

    def on_exit_state6(self,event):
        print('Leaving state6')