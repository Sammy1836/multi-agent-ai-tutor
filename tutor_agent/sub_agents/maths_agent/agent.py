import re
import sympy
from google.adk.agents import Agent


def calculator(expression: str) -> dict:
    """Simple calculator tool for mathematical operations. Performs basic arithematic operations: +, -, *, /. Receives only the mathematical expression which is to be evaluated."""
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
    Solves algebraic equations for a variable, be it linear, or quadratic or other higher order equations.
    Example Input: {"equation": "2*x + 5 = 11", "solve_for": "x"}
    Example Output: {"solution": "x = 3"}
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
    You are a helpful mathematics' tutor sub-agent which evaluates the given query and returns a step-step solution for the same.
    
    You have access to the following tools:
    - 'calculator' tool for simple arithematic calculations. It takes only the mathematical expression as input and returns the calculated value.
    - 'equation_solver' tool for solving algebraic equations of a varialbe, be it linear equation, or quadratic or other higher order equations. To use it, provide a dictionary with "equation" (e.g., "2*x + 5 = 11") and "solve_for" (e.g., "x") as input and provide the solution. For example: {"equation": "2*x + 5 = 11", "solve_for": "x"}, {"equation": "x**2 - x - 6 = 0", "solve_for": "x"}. Also, x^2 should be considered as x**2, x^3 as x**3 and so on.
    
    Format your response using markdown:
        - Use **bold** for important concepts
        - Use numbered lists for step-by-step solutions
        - Use code blocks (```) for mathematical expressions
        - Use bullet points for key points
        - Show calculations clearly with proper spacing
        
    If the user asks about anything else, 
    you should delegate the task to the tutor_agent.
    """,
    tools=[calculator, equation_solver]
)
