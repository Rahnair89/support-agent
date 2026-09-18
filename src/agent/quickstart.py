import os
from strands import Agent
from strands.models import BedrockModel
model = BedrockModel(model_id=os.environ["MODEL_ID"], region_name=os.environ["AWS_REGION"])
agent = Agent(model=model, system_prompt="You are a helpful support agent.")
print(agent("How do I reset my password?"))