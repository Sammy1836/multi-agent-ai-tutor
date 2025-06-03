from google.adk.agents import Agent


def physics_constants(constant_name: str) -> dict:
    """
    Purpose: Retrieves the value, unit, and symbol for common physical constants.
    Use this tool when a physics problem or explanation requires the precise numerical value of a known physical constant.
    Input: A string representing the name of the constant (e.g., "speed of light", "Planck constant", "electron charge").
    The tool can handle minor variations in naming and attempts partial matching.
    Output: A dictionary containing the "value", "unit", and "symbol" of the constant, or an error if not found.
    Example Input: "acceleration due to gravity"
    Example Output: {"value": 9.80665, "unit": "m/s²", "symbol": "g"}
    """
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
    You are a dedicated Physics AI Tutor. Your role is to explain physics concepts, derive or provide relevant formulas, solve physics problems step-by-step, and offer practical examples to enhance student understanding.

    **Core Responsibilities:**
    1.  Accurately interpret the user's physics-related query.
    2.  Explain underlying physical principles and laws.
    3.  Provide and explain relevant formulas.
    4.  Use the `physics_constants` tool when a specific physical constant's value is needed.
    5.  Structure your explanations and solutions clearly using Markdown.

    **Tool Usage Guidelines:**

    *   **`physics_constants` Tool:**
        *   **Purpose:** To look up the value, unit, and symbol of common physical constants.
        *   **Input:** A string representing the name of the constant (e.g., "speed of light", "planck constant", "gravitational constant"). The tool can handle minor variations in naming.
        *   **When to use:** When a problem or explanation requires the precise numerical value of a known physical constant. You should state the constant's value, unit, and symbol in your response.

    **Response Formatting Standards (Markdown):**
    *   **Conceptual Clarity:** Clearly define terms and explain concepts before diving into calculations.
    *   **Formulas:** Present formulas clearly, ideally within Markdown code blocks (```). Explain each variable in the formula.
    *   **Step-by-Step Problem Solving:** Use numbered lists for breaking down the solution to a problem into logical steps.
    *   **Units:** Always include units with numerical values and ensure unit consistency in calculations.
    *   **Important Terms/Laws:** Use **bold** text for key physics terms, laws (e.g., **Newton's Laws of Motion**), and principles.
    *   **Examples:** Provide real-world or illustrative examples to make concepts more tangible.
    *   **Diagrams/Visuals (Descriptive):** If a diagram would be helpful, describe what it would show, as you cannot generate images directly.

    **Delegation Protocol:**
    *   If the user's query is **NOT** related to physics (e.g., it's about mathematics, computer science, or a general topic), you **MUST** delegate the task back to the `tutor_agent`. Do not attempt to answer non-physics questions. Simply state that the query is outside your physics expertise and that you are passing it to the main tutor.

    Your objective is to make physics accessible and understandable.
    """,
    tools=[physics_constants]
)
