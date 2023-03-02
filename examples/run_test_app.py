import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from api import ChatGPT, GPT, Example, UIConfig
from api import demo_web_app


# Construct GPT object and show some examples
# gpt = GPT(engine="davinci",
#           temperature=0.92,
#           max_tokens=500)
# ## GPT Examples
# gpt.add_example(Example('What should I do when my boss is being passive aggressive about my work progress?', 'First, try and schedule a one-on-one with your boss and ask them for their honest feedback about your work performance when they are not busy and occupied. Then try and understand whether their irritation is on account of your work performance, or something else.'))

# Construct ChatGPT object
gpt = ChatGPT(model="gpt-3.5-turbo",
                  m_system=["You are a helpful and empathetic assistant that gives advice on how to deal with the user's situation, and gives concrete next steps."],
                  m_user=[],
                  m_assistant=[],
                  memory=True)

# Define UI configuration - todo: modify uiconfig depnding on what model used?
config = UIConfig(description="Workplace Communications Consulation Bot 🤖 - powered by ChatGPT",
                  button_text="Submit",
                  placeholder="What should I do about <workplace concern with someone>? What should I do next?")

demo_web_app(gpt, config)
