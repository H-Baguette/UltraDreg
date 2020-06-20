# UltraDreg
Sodom Discord bot. Bag's first bot that uses more than 1 .py file, and also their first one that uses git for version control.
## Requirements
- Python 3.8
- pip
- python-setuptools
- discord.py ~= 1.2.5
- mysqlclient

To install all Python dependencies you can use pip. Just do `pip install -r requirements.txt` in the project directory.

## Deployment
To start the bot, do:
```
python3.8 dreg.py <access_token>
```
in the project directory.

## Contribution
If you're going to start making PRs, please try and follow [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) conventions. That means clone the repo and make a new branch for whatever you're doing, i.e if you're making a new feature, call it `feature/name`, or for a hotfix, `hotfix/name`, etc.
