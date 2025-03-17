from wikipedia import *

# Set the language if needed
wikipedia.set_lang("en")

# Search for a term
result = wikipedia.summary("Python (programming language)", sentences=1)

# Display the result
print(result)
