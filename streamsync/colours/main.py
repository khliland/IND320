import streamsync as ss

# This is a placeholder to get you started or refresh your memory.
# Delete it or adapt it as necessary.
# Documentation is available at https://streamsync.cloud

# Shows in the log when the app starts
print("Hello world!")

# Its name starts with _, so this function won't be exposed
def _update_message(state):
    is_even = state["counter"] % 2 == 0
    message = ("+Even" if is_even else "-Odd")
    state["message"] = message

def decrement(state):
    state["counter"] -= 1
    if state["counter"] >= 30:
        state["too_high"] = True
    else:
        state["too_high"] = False
    _update_message(state)

def increment(state):
    state["counter"] += 1
    # Shows in the log when the event handler is run
    if state["counter"] >= 30:
        state["too_high"] = True
    _update_message(state)

# Create a matlibplot figure with a line plot
def plot(state):
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    fig = plt.figure()
    plt.plot(x, y)
    plt.close(fig)

    state["plot"] = fig
    
# Initialise the state

# "_my_private_element" won't be serialised or sent to the frontend,
# because it starts with an underscore

initial_state = ss.init_state({
    "my_app": {
        "title": "My App"
    },
    "_my_private_element": 1337,
    "message": None,
    "counter": 26,
    "too_high":False,
})

_update_message(initial_state)
plot(initial_state)
