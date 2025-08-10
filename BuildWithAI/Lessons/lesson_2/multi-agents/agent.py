import random
from typing import List
from google.adk.agents import Agent

# --- Tool Functions ---

def roll_dice(sides: int) -> dict:
    """Rolls a dice with the specified number of sides and returns the result."""
    if not isinstance(sides, int) or sides < 1:
        return {"status": "error", "error_message": "Number of sides must be a positive integer."}
    roll_result = random.randint(1, sides)
    return {"status": "success", "result": f"Rolled a {sides}-sided dice and got: {roll_result}"}

def flip_coin() -> dict:
    """Flips a coin and returns whether it landed on Heads or Tails."""
    result = random.choice(["Heads", "Tails"])
    return {"status": "success", "result": f"The coin landed on: {result}"}

# The type hint for 'options' has been changed from List[Any] to List[str].
def choose_one(options: List[str]) -> dict:
    """Randomly chooses one item from a given list of strings."""
    if not isinstance(options, list) or not options:
        return {"status": "error", "error_message": "Input must be a non-empty list of options."}
    choice = random.choice(options)
    return {"status": "success", "result": f"From your list, I've randomly chosen: {choice}"}

def generate_random_number(min_val: int, max_val: int) -> dict:
    """Generates a random integer within a specified range (inclusive)."""
    if not all(isinstance(v, int) for v in [min_val, max_val]):
         return {"status": "error", "error_message": "Minimum and maximum values must be integers."}
    if min_val >= max_val:
        return {"status": "error", "error_message": "The minimum value must be less than the maximum value."}
    random_num = random.randint(min_val, max_val)
    return {"status": "success", "result": f"Your random number between {min_val} and {max_val} is: {random_num}"}


# --- Agent Definition ---
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='An agent for various random generations like dice, coins, and numbers.',
    instruction='You are a helpful agent. Use your tools to roll dice, flip coins, choose from lists, or generate numbers upon request.',
    tools=[
        roll_dice,
        flip_coin,
        choose_one,
        generate_random_number
    ],
)