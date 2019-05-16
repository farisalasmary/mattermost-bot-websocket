# Mattermost Bot
Listening for direct messages in Mattermost chatting system and reply to them automatically using a websockt through Mattermost API. You can edit the function `get_bot_response` that receives the direct message `message` from the user `sender_name` and reply with `my_message`. Also, you can use an intellegent chatbot like [Rasa Chatbot](https://rasa.com/) inside `get_bot_response` to find the best reply for the message `message`.

**Example:**
This is an example of using Rasa chatbot in `get_bot_response` function. The code is based on [this link](https://rasa.com/docs/core/quickstart/#id3).

change:
```python
def get_bot_response(message, sender_name):
    my_message = 'welcome!!!!!!!!!'
    send_message(my_message, sender_name)
    return my_message
```
to the following:
```python
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter

def get_bot_response(message, sender_name):
    responses = agent.handle_message(message)
    for r in responses:
        messages.append(r.get("text"))
    
    for my_message in messages:
      send_message(my_message, sender_name)
    return my_message
```
