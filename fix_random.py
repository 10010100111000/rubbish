with open('xxx.py', 'r') as f:
    content = f.read()

import re
# Replace import random with import secrets
content = content.replace("import random", "import random\nimport secrets")

content = content.replace("payment_password = str(random.randint(100000, 999999))", "payment_password = str(secrets.randbelow(900000) + 100000)")

with open('xxx.py', 'w') as f:
    f.write(content)
