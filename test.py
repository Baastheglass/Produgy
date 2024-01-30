import time

# Specify the duration in seconds
duration = 60  # 5 seconds as an example

# Record the start time
start_time = time.time()

# Run the event for the specified duration
while time.time() - start_time < duration:
    # Your event or code goes here
    print("Event is happening!")

# Code after the specified duration
print("Event is no longer happening.")
