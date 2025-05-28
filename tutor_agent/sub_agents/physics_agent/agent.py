from google.adk.agents import Agent


def physics_constants(constant_name: str) -> dict:
    """Tool for looking up physics' constants."""
    constants = {
        "speed_of_light": {"value": 299792458, "unit": "m/s", "symbol": "c"},
        "gravitational_constant": {"value": 6.67430e-11, "unit": "m³/(kg⋅s²)", "symbol": "G"},
        "planck_constant": {"value": 6.62607015e-34, "unit": "J⋅s", "symbol": "h"},
        "electron_charge": {"value": 1.602176634e-19, "unit": "C", "symbol": "e"},
        "avogadro_number": {"value": 6.02214076e23, "unit": "mol⁻¹", "symbol": "Nₐ"},
        "boltzmann_constant": {"value": 1.380649e-23, "unit": "J/K", "symbol": "k"},
        "gas_constant": {"value": 8.314462618, "unit": "J/(mol⋅K)", "symbol": "R"},
        "acceleration_due_to_gravity": {"value": 9.80665, "unit": "m/s²", "symbol": "g"}
    }

    constant_name = constant_name.lower().replace(" ", "_")

    if constant_name in constants:
        return constants[constant_name]

    # Try partial matching
    matches = [k for k in constants.keys() if constant_name in k]
    if matches:
        return constants[matches[0]]

    available = ", ".join(constants.keys())
    raise ValueError(
        f"Constant '{constant_name}' not found. Available constants: {available}")


physics_agent = Agent(
    name="physics_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for physics-related questions.",
    instruction="""
    You are a helpful physics' tutor sub-agent which explains the physics concepts involved, provide relevant formulas if applicable, and give practical examples to help the student understand.
    
    You have access to 'physics constants' tool for looking up physics constants. For example: speed of light, planck constant, etc.
    
    Format your response using markdown:
        - Use **bold** for important concepts
        - Use numbered lists for step-by-step solutions
        - Use code blocks (```) for mathematical expressions
        - Use bullet points for key points
        - Show calculations clearly with proper spacing
        
    If the user asks about anything else, 
    you should delegate the task to the tutor_agent.
    """,
    tools=[physics_constants]
)
