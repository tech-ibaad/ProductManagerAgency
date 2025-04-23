
from agency_swarm import Agent
from tools.ProductDatabaseTool import ProductDatabaseTool

class AIProductManager(Agent):
    def __init__(self):
        super().__init__(
            name="AIProductManager",
            description="A 5000 IQ AI Product Manager who makes expert decisions using SQLite-backed insights.",
            instructions="./Agent/instructions.md",
            tools=[ProductDatabaseTool],
            temperature=0.3,
            max_prompt_tokens=25000
        )
