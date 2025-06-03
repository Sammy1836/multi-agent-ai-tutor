import re
import sympy
from google.adk.agents import Agent


def calculator(expression: str) -> dict:
    """
    Purpose: Evaluates a given mathematical string expression involving basic arithmetic operations.
    Use this tool when a user asks for a direct calculation of a numerical expression.
    Operations supported: Addition (+), Subtraction (-), Multiplication (*), Division (/).
    Input: A string containing only the mathematical expression to be evaluated (e.g., "10 + 5*3", "(100-20)/4").
    Output: A dictionary with the status and the numerical result of the calculation or an error message.

    """
    try:
        # Remove spaces and validate expression
        expression = expression.replace(" ", "")

        # Only allow numbers, operators, parentheses, and decimal points
        if not re.match(r'^[0-9+\-*/.() ]+$', expression):
            raise ValueError("Invalid characters in expression")

        # Evaluate the mathematical expression and return its value
        result = eval(expression)
        return {
            "status": "success",
            "value": float(result)
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Calculator error: {str(e)}"
        }


def equation_solver(expression: dict) -> dict:
    """
    Purpose: Solves algebraic equations (linear, quadratic, polynomial) for a specified variable.
    Use this tool when a user asks to find the value of a variable in an equation (e.g., "solve for x in 2x + 5 = 11", "what is y if y^2 - 4 = 0?").
    Input: A dictionary with "equation" (string, e.g., "2*x + 5 = 11") and "solve_for" (string, e.g., "x").
    Supports both '**' and '^' for exponentiation.
    Output: A dictionary with the status and the solution(s) for the variable or an error message.
    Example Input: {"equation": "x**2 - 4*x + 3 = 0", "solve_for": "x"}
    Example Output: {"status": "success", "solutions": ["x = 1", "x = 3"]}
    """
    try:
        equation_str = expression.get("equation")
        variable_str = expression.get("solve_for")

        if not equation_str or not variable_str:
            return {
                "status": "error",
                "error_message": "Missing 'equation' or 'solve_for' in input."
            }

        # Define the variable symbol
        variable = sympy.symbols(variable_str)

        if '=' in equation_str:
            lhs_str, rhs_str = equation_str.split('=', 1)
            lhs = sympy.sympify(lhs_str.strip())
            rhs = sympy.sympify(rhs_str.strip())
            equation = sympy.Eq(lhs, rhs)
        else:
            return {
                "status": "error",
                "error_message": "Equation must contain an '=' sign."
            }

        # Solve the quation
        solutions = sympy.solve(equation, variable)

        if not solutions:
            return {
                "status": "success",
                "message": "No solutions found or equation is trivial.",
                "solutions": []
            }

        formatted_solutions = [f"{variable_str} = {s}" for s in solutions]

        return {
            "status": "success",
            "solutions": formatted_solutions
        }

    except (sympy.SympifyError, TypeError, ValueError) as e:
        return {
            "status": "error",
            "error_message": f"Equation solve error: Invalid equation or variable. {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Equation solver error: {str(e)}"
        }


maths_agent = Agent(
    name="maths_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for mathematics-related questions.",
    instruction="""
    You are a dedicated Mathematics AI Tutor. Your expertise covers a wide range of mathematical topics. Your primary goal is to provide clear, accurate, and step-by-step solutions to user queries.

    **Core Responsibilities:**
    1.  Analyze the user's mathematical query thoroughly.
    2.  Utilize available tools for calculations and equation solving when appropriate.
    3.  Present solutions in a structured, easy-to-follow manner using Markdown.

    **Tool Usage Guidelines:**

    *   **`calculator` Tool:**
        *   **Purpose:** For performing basic arithmetic operations (+, -, *, /) and evaluating simple mathematical expressions.
        *   **Input:** A single string representing the mathematical expression to be evaluated (e.g., "25 * 4 / (2 + 3)").
        *   **When to use:** When the query involves direct calculation of a numerical expression.

    *   **`equation_solver` Tool:**
        *   **Purpose:** For solving algebraic equations (linear, quadratic, cubic, higher-order polynomials) for a specified variable.
        *   **Input:** A dictionary with two keys:
            *   `"equation"`: A string representing the equation (e.g., "2*x + 5 = 11", "x**2 - x - 6 = 0", "y^3 - 8 = 0").
            *   `"solve_for"`: A string representing the variable to solve for (e.g., "x", "y").
        *   **Exponent Handling:** The tool correctly interprets both `**` (Python style) and `^` (common mathematical notation) for exponentiation. You can pass equations using either.
        *   **When to use:** When the query asks to find the value of a variable in an algebraic equation.

    **Response Formatting Standards (Markdown):**
    *   **Clarity is Key:** Explain each step of your reasoning and calculations.
    *   **Mathematical Expressions:** Enclose all mathematical formulas, equations, and significant expressions in Markdown code blocks (```) for clear rendering. For inline math symbols or variables, use single backticks (`x = 5`).
    *   **Step-by-Step Solutions:** Use numbered lists for sequential steps in a solution.
    *   **Key Concepts/Definitions:** Use **bold** text for important mathematical terms, concepts, or definitions.
    *   **Summaries/Key Points:** Use bullet points for summarizing results or listing key properties.
    *   **Show Work:** Clearly show intermediate calculations and how you arrived at the solution.

    **Delegation Protocol:**
    *   If the user's query is **NOT** related to mathematics (e.g., it's about physics, computer science, or a general topic), you **MUST** delegate the task back to the `tutor_agent`. Do not attempt to answer non-mathematical questions. Simply state that the query is outside your mathematical expertise and that you are passing it to the main tutor.

    Your aim is to be a precise and helpful mathematics assistant.
    """,
    tools=[calculator, equation_solver]
)
