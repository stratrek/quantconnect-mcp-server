path = 'src/models.py'

# Read the file content
with open(path, 'r', encoding='utf-8') as file:
    content = file.read()

# Add the extra import.
content = 'from pydantic import RootModel\n' + content

# Perform string replacements.
content = content.replace('__root__', 'RootModel').replace('ResponseModel', 'Response')

# Save the new file content.
with open(path, 'w', encoding='utf-8') as file:
    file.write(content)
