from flask import Flask, request, jsonify 
from requests_toolbelt import MultipartEncoder
from lsystem import LSystem 
import json, os, requests

import params
import error
from timeout import timeout
from util import Util

app = Flask(__name__) 

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
    js = request.args.get("json", None)

    response = {}
 
    if not js:
        response["ERROR"] = "no params found, please enter params."
    else:
        response["CONTENT"] = json.loads(js) 
    return response


@app.route('/', methods=['POST'])
def webhook():
    global DEFAULT_SETTINGS 

    data = request.get_json() 

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    try:
                        message_text = messaging_event["message"]["text"].strip()  # the message's text
                    except KeyError:
                        #not a text message
                        send_message(sender_id, "Please only send text messages.")
                        break

                    text_cleaned = Util.clean_whitespace(message_text)
                    top_line = text_cleaned.split("\n")[0]
                    message_words = [word.lower() for word in top_line.split(" ")]
                    send_settings =  (len(message_words) > 1) and (message_words[1] == "show")

                    if message_words[0] == "settings":
                        oplen = len(message_text.split("\n")[0]) + 1                         
                        try:
                            random = False
                            s_p = parse_settings(message_text[oplen:])
                            settings = s_p[0] 
                            fields_present = s_p[1]
                            exclude = add_suffixes(fields_present)
                            
                            msg = "Generating tree from settings...please wait."
                            send_message(sender_id, msg) 
                            if len(exclude) > 0:
                                random = True

                            image, params = create_image(settings, random, exclude)()
                            if (send_settings):
                                send_message(sender_id, params)
                            send_image(sender_id, image) 
                            break

                        except error.MalformedSettingsError as e:
                            send_message(sender_id, "Error: " + e.message)

                        except error.NegativeFieldError as e:
                            send_message(sender_id, "Error: " + e.message)

                        except error.ParameterError as e:
                            send_message(sender_id, "Error: " + e.message)

                        except error.ParameterDoesNotExistError as e:
                            send_message(sender_id, "Error: " + e.message)

                        except error.ResponseTimeoutError as e:
                            send_message(sender_id, "Error: " + e.message) 

                    elif is_at_beginning("random", message_text):
                        msg = "Generating random tree...please wait.\n"
                        send_message(sender_id, msg)
                        try:
                            settings = json.dumps(DEFAULT_SETTINGS)
                            settings["seed"] = Util.get_seed(params.SEEDLEN)
                            image, p = create_image(settings, True, [])()
                            if (send_settings):
                                send_message(sender_id, p)
                            send_image(sender_id, image) 
                            break

                        except error.MalformedSettingsError as e:
                            send_message(sender_id, "Error: " + e.message)

                        except error.NegativeFieldError as e:
                            send_message(sender_id, "Error: " + e.message)

                        except error.ParameterError as e:
                            send_message(sender_id, "Error: " + e.message)

                        except error.ParameterDoesNotExistError as e:
                            send_message(sender_id, "Error: " + e.message)

                        except error.ResponseTimeoutError as e:
                            send_message(sender_id, "Error: " + e.message) 

                    elif is_at_beginning("help", message_text):
                        msg = help_text() 
                        example = example_text()
                        send_message(sender_id, msg)
                        send_message(sender_id, example)

                    elif is_at_beginning("colours", message_text):
                        msg = colours_text()
                        send_message(sender_id, msg)

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
    print(lines)
    present = []
    seed = None
    for i, line in enumerate(lines):
        f_v = line.split(":")
        if len(f_v) == 2:
            field = f_v[0].lower().strip()
            value = f_v[1].lower().strip()

            if not field_exists(field, DEFAULT_SETTINGS):
                raise error.ParameterDoesNotExistError(field)


            if field == "iterations":
                present.append(field)
                if Util.isInteger(value):
                    value = int(value)
                    if value < 0:
                        raise error.NegativeFieldError(field, value)
                        
                    if value > 5 or value == 0:
                        raise error.ParameterError(field, value, "Argument must be between 1 and 5.")    
                else:
                    raise error.ParameterError(field, value, "Argument must be an integer.")

            elif field == "scale":
                present.append(field)
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
                    present.append(field)
                except KeyError:
                    raise error.ParameterError(field, value, "This colour does not exist.")

            elif field == "leaf_density" or field == "fruit_density":
                present.append(field)
                if Util.isNumeric(value):
                    value = float(value)
                    if value < 0 or value > 1:
                        raise error.ParameterError(field, value, "Density must be between 0 and 1.")    
                else:
                    raise error.ParameterError(field, value, "Density must be a number.")
            elif field == "finished":
                if Util.isBool(value):
                    value = Util.strToBool(value)
                else:
                    raise error.ParameterError(field, value, "Must be a truthy or falsey string, eg yes/no, y/n etc.")

            elif field == "seed":
                seed = value

            DEFAULT_SETTINGS[field] = value

        else:
            raise error.MalformedSettingsError(i) 

        if seed == None:
            DEFAULT_SETTINGS["seed"] = Util.get_seed(params.SEEDLEN)

    return (json.dumps(DEFAULT_SETTINGS), present)
 

def send_message(recipient_id, message_text): 

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

def send_image(recipient_id, filepath): 

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

    return string.lower()[:len(word.lower())] == word.lower()

@timeout
def create_image(settings, random, exclude): 
    lsg = LSystem(settings, random=random, cmd=False, exclude=exclude)
    image_name = lsg.run()
    image_settings = lsg.get_settings_string()
    print("image created successfully at " + image_name) 
    return (image_name, image_settings)

def add_suffixes(l):
    words = []
    for word in l:
        if word == "start" or word == "end" or word == "fruit" or word == "leaf":
            word += "_colour"
        elif word == "scale":
            word = "length"
        words.append(word)

    return words

def help_text():
    text = ('-TreeGifs Help-\n'
            'To supply settings, start your message by typing SETTINGS.'
            'Then provide the following parameters in any order, each on a new line:\n\n' 
            'iterations: positive integer - Number of iterations between 1 and 5.\n'
            'start: colour - Starting colour of the tree (roots).\n'
            'end: colour - Ending colour of the tree (branch tips).\n'
            'fruit: colour - Colour of fruits, if any.\n'
            'leaf: colour - Colour of leaves, if any.\n'
            'scale: positive real number - Size multiplier for tree segments.\n'
            'fruit_density: positive real number - Relative frequency of fruits.\n'
            'leaf_density: positive real number - Relative frequency of leaves.\n\n'
            'If any of these fields are left out, they will automatically be filled in '
            'with random values.\n\n'
            'Or you can forgo SETTINGS completely and generate a completely random tree '
            'by just typing RANDOM.\n\n'
            'If you type SHOW on the same line right after either RANDOM or SETTINGS, '
            'the bot will send an additional message with a copyable settings list you '
            'can save and share!\n\n'
            'To see an exhaustive list of all the colours supported, type COLOURS.\n\n'
            'The following message will have an example that you can copy and try out:'
            )
    return text

def example_text():
    text = ('SETTINGS\n'
            'iterations:5\n'
            'start:blue\n'
            'end:pink\n'
            'fruit:yellow\n'
            'leaf:pink\n'
            'scale:5.5\n'
            'fruit_density:0.01\n'
            'leaf_density:0.1\n'
            )
    return text

def greeting_text():
    text = ('Hello! To interact with this bot, please provide some settings or type '
            'HELP to see how to do so. To see an exhaustive list of all the '
            'colours supported, type COLOURS.'
            )
    return text

def colours_text():
    text = "VALID COLOURS:\n"
    for colour in sorted(params.COLOURS.keys()):
        text += "{}\n".format(colour)
    return text





if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support 
    app.run(threaded=True, port=5000)
    # lsg = LSystem(PLANT_BASE, random=False, cmd=True)
    # lsg.run()
    # print(lsg.get_settings_string())


