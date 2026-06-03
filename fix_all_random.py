with open('xxx.py', 'r') as f:
    content = f.read()

# Replace all occurrences of random.* with secrets.choice, secrets.randbelow, etc.
# Actually, since these are dummy data generations, SonarCloud is likely complaining about `random` being imported at all if it suspects security implications.
# Wait, let's just make it secure by replacing `random` with `secrets` module equivalents for the generators.

content = content.replace("import random", "import random\nimport secrets")

content = content.replace("random.choice(", "secrets.choice(")
content = content.replace("random.randint(", "secrets.randbelow(")
# secrets.randbelow(max) returns [0, max-1]. So random.randint(a, b) -> secrets.randbelow(b - a + 1) + a

import re
def replace_randint(match):
    a = int(match.group(1))
    b = int(match.group(2))
    diff = b - a + 1
    return f"secrets.randbelow({diff}) + {a}"

content = re.sub(r"secrets\.randbelow\(\s*(\d+)\s*,\s*(\d+)\s*\)", replace_randint, content)

# random.choices
# secrets doesn't have choices. We can just use [secrets.choice(population) for _ in range(k)]
def replace_choices_k(match):
    pop = match.group(1)
    k = match.group(2)
    return f"''.join(secrets.choice({pop}) for _ in range({k}))"
content = re.sub(r"random\.choices\(\s*(\".*?\")\s*,\s*k\s*=\s*(.*?)\s*\)", replace_choices_k, content)

# For random.choices with weights, let's just hardcode the logic since it's only used once: `random.choices([1, 2], weights=[0.2, 0.8])[0]`
content = content.replace("random.choices([1, 2], weights=[0.2, 0.8])[0]", "1 if secrets.randbelow(10) < 2 else 2")

# random.sample
# we can just write: secrets.choice(...) twice, though it might pick same. For fake name it's fine.
content = content.replace("random.sample(FIRST_NAMES, 2)", "[secrets.choice(FIRST_NAMES), secrets.choice(FIRST_NAMES)]")

# random.random()
content = content.replace("random.random() < 0.8", "secrets.randbelow(10) < 8")

# random.uniform(13, 20)
content = content.replace("random.uniform(13, 20)", "secrets.randbelow(8) + 13")

with open('xxx.py', 'w') as f:
    f.write(content)
