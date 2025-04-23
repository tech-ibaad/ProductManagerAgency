
from agency_swarm import Agent

class CEO(Agent):
    def __init__(self):
        super().__init__(
            name="CEO",
            description="Chief Executive Officer agent. Oversees product direction and coordinates with AIProductManager.",
            instructions="You are the CEO. Your job is to set strategic direction and ask the AI Product Manager agent to execute product plans, feature prioritization, and market adaptation.",
            temperature=0.4,
            max_prompt_tokens=25000
        )
