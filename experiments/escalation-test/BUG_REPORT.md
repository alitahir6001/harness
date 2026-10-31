# Bug: old notes disappear

Reported by a user: they added several notes over a few days, then searched
for one from earlier in the week and got nothing back. Searching for the
note they added five minutes ago works fine.

Steps to reproduce:
```bash
python3 notewell.py add "note one"
python3 notewell.py add "note two"
python3 notewell.py search note
```
Expected: both notes show up. Actual: only "note two" shows up.

Needs a real fix, not a workaround — this is the core add/search path.
