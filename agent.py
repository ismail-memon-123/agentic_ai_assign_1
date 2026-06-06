from crewai import Agent, Task, Crew, LLM

from mcp_tools import (
    ReadCSVTool,
    ComputeStatsTool
)

llm = LLM(
    model="bedrock/us.anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1"
)

agent = Agent(
    role="Business Analyst",
    goal="Analyze order data",
    backstory="You are an experienced analyst who specializes in interpreting structured datasets and producing clear business insights.",
    tools=[
        ReadCSVTool(),
        ComputeStatsTool()
    ],
    llm=llm
)

task = Task(
    description="""
    Analyze the order CSV
    and summarize order totals.
    """,
    expected_output="Summary",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task]
)

result = crew.kickoff()

print(result)
