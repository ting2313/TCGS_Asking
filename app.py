from bottle import route, run, request, abort, static_file

from fsm import TocMachine
from utils import send_text_message,send_image_url

VERIFY_TOKEN = "1234567890987654321"
machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2',
        'state3',
        'state4',
        'state5',
        'state6'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'go_back',
            'source':  [
                'state2',
                'state5',
                'state6'
            ],
            'dest': 'user'
        },
        {
            'trigger': 'go_input',
            'source': 'state1',
            'dest': 'state3'
        },
        {
            'trigger': 'go_upper',
            'source': 'state3',
            'dest': 'state4',
            'conditions':'is_going_to_state4'
        },
        {
            'trigger': 're_enter',
            'source':  'state4',
            'dest': 'user'
        },
        {
            'trigger': 'advance',
            'source':  'user',
            'dest': 'state5',
            'conditions': 'is_going_to_state5'
        },
        {
            'trigger': 'advance',
            'source':  'user',
            'dest': 'state6',
            'conditions': 'is_going_to_state6'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        if machine.is_state1():
            machine.go_input(event)
        elif machine.is_state2():
            machine.go_back(event)
        elif machine.is_state3():
            machine.go_upper(event)
        elif machine.is_state4():
            machine.re_enter(event)
        else:            
            machine.advance(event)
            if machine.is_user():
                sender_id = event['sender']['id']
                if machine.in_bot_flag:
                    send_image_url(sender_id, "http://pic.pimg.tw/unicorn3q/1413511774-943890435.gif")
                    responese = send_text_message(sender_id, "請問需要什麼服務呢？")
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
