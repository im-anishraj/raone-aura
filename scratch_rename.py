import os

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping {file_path}: {e}")
        return

    new_content = content.replace('AURA_HOME', 'AURA_HOME')
    new_content = new_content.replace('AURA_ROOT', 'AURA_ROOT')
    new_content = new_content.replace('aura_home', 'aura_home')
    new_content = new_content.replace('aurahistory', 'aurahistory')
    new_content = new_content.replace('.aura', '.aura')

    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

def walk_dir(directory):
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '.venv' in root or '__pycache__' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith(('.py', '.toml', '.md', '.txt', '.yaml', '.yml', '.css', '.tcss', '.json')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    walk_dir('.')
