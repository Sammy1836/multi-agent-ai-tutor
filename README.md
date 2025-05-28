# AI Tutor Agent Project

This project implements a multi-agent AI tutor system designed to answer questions across Computer Science, Mathematics, and Physics. It features a root "Tutor Agent" that delegates queries to specialized sub-agents.

## Features

*   **Modular Design:** Uses a root agent and subject-specific sub-agents.
*   **Specialized Sub-Agents:**
    *   **Computer Science Agent:** Handles queries related to programming, algorithms, data structures, etc.
    *   **Mathematics Agent:** Addresses mathematical problems, including algebraic equations and arithmetic calculations.
        *   **Calculator Tool:** Performs basic arithmetic.
        *   **Equation Solver Tool:** Solves linear, quadratic, and higher-order algebraic equations (supports `**` and `^` for exponentiation).
    *   **Physics Agent:** Explains physics concepts and provides formulas.
        *   **Physics Constants Tool:** Looks up common physical constants.
*   **Intelligent Delegation:** The root agent analyzes user queries to route them to the most appropriate sub-agent.
*   **Tool Usage:** Sub-agents can leverage tools to perform specific tasks like calculations or data lookup.
*   **Markdown Formatting:** Agents are instructed to provide responses in a clear, well-formatted markdown structure.

## Project Structure

The project is organized as follows:

```
ai-agents/
├── requirements.txt        # Python dependencies
├── tutor_agent/            # Main application directory
│   ├── __init__.py
│   ├── agent.py            # Root Tutor Agent definition
│   ├── .env                # Environment variables (e.g., API keys)
│   └── sub_agents/
│       ├── __init__.py
│       ├── cs_agent/
│       │   ├── __init__.py
│       │   └── agent.py    # Computer Science sub-agent
│       ├── maths_agent/
│       │   ├── __init__.py
│       │   └── agent.py    # Mathematics sub-agent & tools
│       └── physics_agent/
│           ├── __init__.py
│           └── agent.py    # Physics sub-agent & tool
└── README.md               # This file
```

## Setup and Installation

1.  **Clone the Repository (if applicable):**
    ```bash
    git clone <your-repository-url>
    cd ai-agents
    ```

2.  **Create a Virtual Environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    Make sure you have `pip` installed.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the `tutor_agent` directory (`/Users/sameersaurabh/Web/ai-agents/tutor_agent/.env`).
    This file should contain any necessary API keys or configurations, for example:
    ```env
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    # Add other environment variables if needed
    ```
    *Note: The specific environment variables required will depend on the `google-adk` and `google-generativeai` libraries' authentication mechanisms.*

## Running the Application
    ```bash
    adk web # For running the application in a UI provided by adk
    adk run # For running the application in the terminal
    ```

## Agent Details

### 1. Tutor Agent (`root_agent`)
*   **File:** `/Users/sameersaurabh/Web/ai-agents/tutor_agent/agent.py`
*   **Description:** Acts as the main entry point. It analyzes the user's query to determine the subject matter and delegates the task to the appropriate specialist sub-agent (`cs_agent`, `maths_agent`, or `physics_agent`).
*   **Fallback:** If a query doesn't fit the defined subjects, it's instructed to state that no specialized sub-agent is available and attempt to answer using its own capabilities, mentioning the source of its information.

### 2. Mathematics Agent (`maths_agent`)
*   **File:** `/Users/sameersaurabh/Web/ai-agents/tutor_agent/sub_agents/maths_agent/agent.py`
*   **Description:** Specializes in mathematics-related questions.
*   **Tools:**
    *   `calculator(expression: str)`: Evaluates basic arithmetic expressions.
    *   `equation_solver(expression_data: dict)`: Solves algebraic equations.
        *   Input: `{"equation": "...", "solve_for": "..."}`
        *   Supports `**` and `^` for exponentiation (e.g., `x**2` or `x^2`).

### 3. Physics Agent (`physics_agent`)
*   **File:** `/Users/sameersaurabh/Web/ai-agents/tutor_agent/sub_agents/physics_agent/agent.py`
*   **Description:** Handles physics concepts, formulas, and examples.
*   **Tools:**
    *   `physics_constants(constant_name: str)`: Looks up the value, unit, and symbol of common physical constants (e.g., "speed of light", "planck constant").

### 4. Computer Science Agent (`cs_agent`)
*   **File:** `/Users/sameersaurabh/Web/ai-agents/tutor_agent/sub_agents/cs_agent/agent.py`
*   **Description:** Explains computer science concepts, provides code syntax, and examples.
*   **Tools:** None currently defined (can be extended).

## Dependencies

*   `google-adk`: For agent development.
*   `google-generativeai`: For interacting with Google's generative AI models.
*   `python-dotenv`: For managing environment variables.
*   `sympy`: For symbolic mathematics, used by the `equation_solver` tool.