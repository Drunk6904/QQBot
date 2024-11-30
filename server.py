from flask import *

import Message
import Event
import MessageHandler
app = Flask(__name__)


@app.route('/', methods=['POST'])
def listen_message():
    message = request.json
    print("接收到消息:" + str(message))

    MessageHandler.checkAndReply(message)
    return "200 OK"


if __name__ == '__main__':
    Event.load_plugins()
    app.run(host='0.0.0.0', port=8080, debug=True)
