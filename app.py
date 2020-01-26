from flask import Flask, request, jsonify 
from requests_toolbelt import MultipartEncoder
from lsystem import LSystem 
import json, os, requests

import params
import error
from util import Util

app = Flask(__name__)

TEST = ('{"alphabet": "XF-+[]",'
        '"axiom": "X",'
        '"rules": ['
                    '{"in": "F",'
                    '"out": "FF"},'
                    '{"in": "X",'
                    '"out": "F+[[X]-X]-F[-FX]+X"}'
                  '],'
        '"iterations": 5,'
        '"animate": true,'
        '"angle": 25,'
        '"length": 5,'
        '"graphics_class": "PlantHandler"}')

PLANT_BASE = "./settings/plant_example.json"
DEFAULT_SETTINGS = Util.get_settings_from_json_file(PLANT_BASE)


@app.route('/', methods=['GET'])
def verify(): 
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"): 
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/params/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    js = request.args.get("json", None)

    # For debugging
    print("got params {}".format(js))

    response = {}
 
    if not js:
        response["ERROR"] = "no params found, please enter params."
    else:
        response["CONTENT"] = json.loads(js)

    # Return the response in json format
    return response


@app.route('/', methods=['POST'])
def webhook():
    global TEST, DEFAULT_SETTINGS

    # endpoint for processing incoming messaging events

    data = request.get_json() 

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    msg = "" 
                    if is_at_beginning("SETTINGS\n", message_text):
                        oplen = len("SETTINGS\n")

                        print(message_text[oplen:])
                        try:
                            settings = parse_settings(message_text[oplen:])
                            msg = "You provided the following settings:\n" + settings + "\n"
                            send_message(sender_id, msg)
                            image = create_image(settings)
                            if image["status"] == "OK":
                                send_image(sender_id, image["image_name"])
                            else:
                                send_message(sender_id, "Sorry, please try again")
                            break

                        except error.MalformedSettingsError as e:
                            send_message(sender_id, "Error:" + e.message)

                        except error.NegativeFieldError as e:
                            send_message(sender_id, "Error:" + e.message)

                        except error.ParameterError as e:
                            send_message(sender_id, "Error:" + e.message)

                        except error.ParameterDoesNotExistError as e:
                            send_message(sender_id, "Error:" + e.message)

                    elif is_at_beginning("RANDOM", message_text):
                        msg = "Generating random tree...please wait.\n"
                        send_message(sender_id, msg)
                        settings = json.dumps(DEFAULT_SETTINGS)
                        image = create_image(settings, random=True)
                        if image["status"] == "OK":
                            send_image(sender_id, image["image_name"])
                        else:
                            send_message(sender_id, "Sorry, please try again")
                        break

                    elif is_at_beginning("HELP", message_text):
                        msg = help_text()
                    elif is_at_beginning("TEST", message_text):
                        msg = "generating test image"
                        send_message(sender_id, msg)

                        filename = create_image(TEST) 
                        send_image(sender_id, filename)
                        break
                    else:
                        msg = greeting_text()


                    send_message(sender_id, msg)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def field_exists(field, settings):
    if field == "scale":
        field = "length"
    elif field == "fruit" or field == "leaf" or field == "start" or field == "end":
        field += "_colour"

    try:
        settings[field]
        return True
    except KeyError:
        return False

def parse_settings(settings):
    global DEFAULT_SETTINGS
    lines = settings.split("\n") 

    for i, line in enumerate(lines):
        f_v = line.split(":")
        if len(f_v) == 2:
            field = f_v[0].lower()
            value = f_v[1].lower()

            if not field_exists(field, DEFAULT_SETTINGS):
                raise error.ParameterDoesNotExistError(field)


            if field == "iterations":
                if Util.isInteger(value):
                    value = int(value)
                    if value < 0:
                        raise error.NegativeFieldError(field, value)

                    if value > 5:
                        raise error.ParameterError(field, value, "Argument must be between 0 and 5.")    
                else:
                    raise error.ParameterError(field, value, "Argument must be an integer.")

            elif field == "scale":
                if Util.isNumeric(value):
                    field = "length"
                    value = float(value)
                    if value < 0:
                        raise error.NegativeFieldError(field, value)
                else:
                    raise error.ParameterError(field, value, "Scale must be an number.")                    
            
            elif field == "start" or field == "end" or field == "leaf" or field == "fruit":
                try:
                    params.COLOURS[value]
                    field += "_colour"
                except KeyError:
                    raise error.ParameterError(field, value, "This colour does not exist.")

            elif field == "leaf_density" or field == "fruit_density":
                if Util.isNumeric(value):
                    value = float(value)
                    if value < 0 or value > 1:
                        raise error.ParameterError(field, value, "Density must be between 0 and 1.")    
                else:
                    raise error.ParameterError(field, value, "Density must be a number.")


            
            DEFAULT_SETTINGS[field] = value
        else:
            raise error.MalformedSettingsError(i) 

    return json.dumps(DEFAULT_SETTINGS)





def send_message(recipient_id, message_text):

    # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v5.0/me/messages", params=params, headers=headers, data=data)
    # if r.status_code != 200:
    #     log(r.status_code)
    #     log(r.text)

def send_image(recipient_id, filepath):

    # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    data = { 
        'recipient': json.dumps({
            'id': recipient_id
        }), 
        'message': json.dumps({
            'attachment': {
                'type': 'image',
                'payload': {}
            }
        }),
        'filedata': (filepath, open(filepath, 'rb'), 'image/gif')
    }

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }

    multipart_data = MultipartEncoder(data)
 
    multipart_header = {
        'Content-Type': multipart_data.content_type
    }
    r = requests.post("https://graph.facebook.com/v5.0/me/messages", params=params, headers=multipart_header, data=multipart_data)
    print(r.text)

def is_at_beginning(word, string):
    if len(word) > len(string):
        return False

    return string[:len(word)] == word

def create_image(settings, random=False):
    try:
        lsg = LSystem(settings, random, cmd=False)
        image_name = lsg.run()
        print("image created successfully at " + image_name)
        return {"status": "OK", "image_name": image_name}
    except Exception as e:
        print(e.message)
        return{"status": "error"}



def help_text():
    text = ('-LSystemsGifs Help-\n'
            'To supply settings, start your message with "SETTINGS". '
            'Then provide the following parameters, each on a new line:\n'
            'type: Plant OR Dragon OR BTree OR Koch - How to interpret your L-System.\n\n'
            'iterations: positive integer - Number of iterations to run your rules.\n\n'
            'animate: true OR false - Decides whether to return an animated gif or a picture.\n\n'
            'alphabet: string - Each character in this string is a symbol in the alphabet.\n\n'
            'axiom: string - Starting point of the L-system. Must only be made up of '
            'symbols from the previously defined alphabet.\n\n'
            'rules: string > string | ... - String replacement rules that define your '
            'L-System. Can have multiple rules, each separated by "|". '
            'Each rule consists of two strings: The string to replace (left), and its replacement (right), '
            'separated by ">".\n\n'
            'Important:\n'
            'ALL of these parameters must be present for SETTINGS to be processed correctly.\n'
            'User-defined strings should not contain whitespace or the symbols ":", ">" or "|".\n'
            )
    return text

def greeting_text():
    text = ('Hello! To interact with this bot, please provide some settings or type '
            '"HELP" to see how to do so.'
            )
    return text

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)