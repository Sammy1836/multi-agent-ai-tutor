from google.adk.agents import Agent

from .sub_agents.cs_agent.agent import cs_agent
from .sub_agents.maths_agent.agent import maths_agent
from .sub_agents.physics_agent.agent import physics_agent

root_agent = Agent(
    name="tutor_agent",
    model="gemini-2.0-flash",
    description="Main tutor agent that delegates queries to subject-specialist sub-agents for Math, Physics, and Computer Science questions.",
    instruction="""    
    You are a helpful AI Tutor agent. For each user query, you must:
    
    1. Determine the primary subject of THIS specific query
    2. Delegate to the appropriate specialist agent
    
    Subject Classification:
    - Physics: motion, forces, energy, waves, electricity, physical phenomena
    - Mathematics: equations, calculations, geometry, algebra, calculus, statistics  
    - Computer Science: programming, algorithms, code, software, data structures
    
    Always delegate to exactly one agent: physics_agent, maths_agent, or cs_agent
    Base your decision solely on the current query content.
    
    Note: When asked about any other question other than the mentioned subjects' sub-agents, mention it in the beginning of the response that no available sub-agents for this <subject> (where <subject> is wide-topic for the query), but tell the student that you are fetching this information from <source> (where <source> is where you find this answer). Use the root_agent to answer these questions in a proper structured format. 
    """,
    sub_agents=[cs_agent, maths_agent, physics_agent]
)
