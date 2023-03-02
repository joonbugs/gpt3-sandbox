"""Creates the Messages and ChatGPT classes for a user to interface with the OpenAI
API."""

import openai
import uuid


def set_openai_key(key):
    """Sets OpenAI key."""
    openai.api_key = key

class Messages:
    def __init__(self, m_system, m_user, m_assistant):
        self.m_system = m_system
        self.m_user = m_user
        self.m_assistant = m_assistant

        self.m_user_original = m_user
        self.m_assistant_original = m_assistant
        self.count = 0 # used to keep track of how many non-priming call-responses

    def get_m_system(self):
        """Returns the system message used to prime."""
        return self.m_system

    def get_m_user(self):
        """Returns all user inputs."""
        return self.m_user

    def get_m_assistant(self):
        """Returns all assistant/ChatGPT output."""
        return self.m_assistant

    def get_all_chat_output(self):
        """returns string of all chat output including system message"""
        ### TODO : still work in progress
        ## eventually add ability to do
        """
            System Prompt: foobar
            User: barfoobar
            Assistant: foo
            -------- (After Priming) ------
            User : bar
            Assistant: foo
            <....>
        """
        # ret_str = ""
        # ## before priming
        # ret_str += "System Prompt: " + ' '.join([str(item) for item in m_system]) + "\n"

        ## after priming

        # return ""
        print("current message status")
        for item in self.as_message():
            print(item)

    def get_count(self):
        return self.count

    def as_dict(self, m_type, content):
        """turns into message dictionary type / ascribes to ChatML syntax"""
        return {
            "role": m_type,
            "content": content
            }

    def as_message(self):
        l_system = lambda c : self.as_dict("system", c)
        dict_m_system = list(map(l_system, self.m_system))

        l_user = lambda c : self.as_dict("user", c)
        dict_m_user = list(map(l_user, self.m_user))

        l_assistant = lambda c : self.as_dict("assistant", c)
        dict_m_assistant = list(map(l_assistant, self.m_assistant))

        ## put to gether lists of dict into one list of dicts
        message = []

        if len(dict_m_user) == 0:
            message =  dict_m_system
        else:
            message = dict_m_system + [item for tpl in zip(dict_m_user, dict_m_assistant) for item in tpl]

        return message

    def as_query_message(self, prompt):
        message = self.as_message()

        message.append(self.as_dict("user", prompt))
        return message

    def update_Message(self, prompt, response):
        self.m_user.append(prompt)
        self.m_assistant.append(response)
        self.count += 1

    def reset_Message(self):
        self.m_user = self.m_user_original
        self.m_assistant = self.m_assistant_original
        self.count = 0

class ChatGPT:
    """The main class for a user to interface with the OpenAI API.

    A user can add different message types and set parameters of the API request.
    """
    def __init__(self, 
                 model="gpt-3.5-turbo", # alternative: "gpt-3.5-turbo-0301"
                 m_system=[],
                 m_user=[],
                 m_assistant=[],
                 memory=False): # memory means that user
        self.model = model
        self.memory = memory
        self.message = Messages(m_system, m_user, m_assistant)

    def get_all_examples(self):
        """Returns all examples as a list of dicts."""
        return self.message.get_all_chat_output()
    def get_model(self):
        """Returns the model specified for the API."""
        return self.model
    def get_m_system(self):
        """Returns the sysem message used to prime the model"""
        return self.message.get_m_system()
    def get_m_user(self):
        """Returns all user inputs."""
        return self.message.get_m_user()
    def get_m_assistant(self):
        """Returns all assistant/ChatGPT output."""
        return self.message.get_m_assistant()
    def craft_query(self, prompt):
        """Creates the query for the API request. Unlike GPT-3 should 
        format as array of dictionaries of different message types
        """
        return self.message.as_query_message(prompt)
    def submit_request(self, prompt):
        """Calls the OpenAI API with the specified parameters."""
        response = openai.ChatCompletion.create(model=self.get_model(),
                                                messages=self.craft_query(prompt))
        return response
    def get_top_reply(self, prompt):
        """Obtains the best result as returned by the API."""
        response = self.submit_request(prompt)
        response_assistant = response['choices'][0]['message']['content']
        if self.memory:
            print("memory true condition")
            self.message.update_Message(prompt, response_assistant)
            self.message.get_all_chat_output()

        return response_assistant
