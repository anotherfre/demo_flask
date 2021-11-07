from web_api import *
import redis


class Message_msg:
    def __init__(self, request, rds):
        self.request = request
        self.args = request.args
        self.form = request.form
        self.rds = rds

    def run(self):
        option = self.args.get('type', '')
        if option == '':
            pass
        if not hasattr(self, option):
            return {'ret': 500}
        result = getattr(self, option)()
        return result

    def send(self):
        content = self.form.get('content')
        email = self.form.get('email')
        user_content = {content: content, email: email}
        user_content = json.dumps(user_content)
        self.rds.set("value", user_content, ex=60)
        return "success"


@admin.route('/message_msg', methods=['GET', 'POST'])
def message_msg():
    rds = redis.Redis(host='192.168.31.196', port=6379)
    try:
        if request.args.get('type'):
            _message = Message_msg(request, rds)
            _message.run()
        return render_template('message.html')
    except Exception as e:
        print(e)
        return "500"
