import random
from google.adk.agents import Agent

def roll_dice(sides: int) -> dict:
    """Rolls a dice with the specified number of sides and returns the result.
    
    Args:
        sides (int): The number of sides on the dice (must be a positive integer).
    
    Returns:
        dict: status and result containing the dice roll outcome, or error message.
    """
    if not isinstance(sides, int) or sides < 1:
        return {
            "status": "error",
            "error_message": "Number of sides must be a positive integer (1 or greater)."
        }
    
    roll_result = random.randint(1, sides)
    return {
        "status": "success",
        # Changed 'report' to 'result' to match the docstring
        "result": f"Rolled a {sides}-sided dice and got: {roll_result}"
    }


root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='Agent to answer questions and roll dice.',
    instruction='You are a helpful agent who can roll dice with any number of sides for games or random number generation.',
    tools=[roll_dice]
)