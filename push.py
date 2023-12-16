import os

files = os.listdir()

os.system(rf"git add .gitignore")
os.system(rf'git commit -m "Update"')
os.system(f"git push -u origin main --force")

for x in files:
    if ".gitignore" not in x and "push.py" not in x:
        os.system(rf'git add "{x}"')
        os.system(f'git commit -m "Update"')
        os.system(f"git push --force")
