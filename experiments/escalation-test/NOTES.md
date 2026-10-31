# Open question: storage format

Notes currently live in a single flat file (`notes.txt`), one note per line,
plain text. That's the whole storage layer right now.

We're about to add tagging and a "search by date" filter, and before building
either on top of the current format I need a call on this: keep the flat
file, or migrate to SQLite now.

- **Keep the flat file.** Dead simple, human-editable, diffable in git, zero
  dependencies. But tagging means encoding structure into plain text lines
  (some kind of delimiter or inline syntax), and date filtering means parsing
  a string on every search instead of querying an index. Gets slower and
  uglier as the note count grows.
- **Move to SQLite now.** Real schema for tags and dates, indexed search,
  transactional writes. But it's a real migration — existing users already
  have `notes.txt` files with real notes in them, so this means writing a
  one-time import step, and once tags/dates are modeled relationally, going
  back to flat-file would mean throwing that structure away again.

I need this decided before I build tagging on top of whichever one we pick —
whichever way we go, unwinding it after the fact means redoing both the
storage layer and the tagging feature together. Need a final call on this,
not just a lean.
