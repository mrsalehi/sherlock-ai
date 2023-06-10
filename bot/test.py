import sys

# Check if the prompt argument is provided
if len(sys.argv) > 1:
    prompt = sys.argv[1]
    print("Prompt:", prompt)
else:
    print("No prompt argument provided.")
