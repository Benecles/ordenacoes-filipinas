# Figure parts

Praised objects turned into reusable instruments (27/10). This answers the 25/10 postmortem, whose first cause was "the
kit made cards the easy path" (a kit of panels, caps labels and tick rules) and whose praised specimen "was a page to
admire, not a part to reuse". A part is an **object** with its own parts and actions, never a layout primitive.

| Part | Object | Reader's action | Source |
|---|---|---|---|
| `calendar` | the month(s) of a prazo, counted day by day | press the start, a holiday or the last day: why it counts or not | specimen 07/10 (praised) |
| `autos` | the case file seen from the side, folhas numbered | press an act: what it does in the case | specimen 07/10 + Processo front 26/10 (praised) |

**Use (writer):** in `lesson.json`, cast the part and give it facts, never positions:
```json
{"type": "figure", "part": "calendar", "caption": "…", "params": {"start": "2015-04-02", "days": 15, "rule": "business", …}}
```
Each module's docstring lists its params. Then:
```
python3 -m tools.figkit.parts.expand lesson.json lesson.expanded.json
python3 tools/lesson_renderer.py --input lesson.expanded.json --output PAGE.html --check-classes
```

**Guarantees:**
- Every count, date and folha number is computed: a 15-business-day prazo from 02/04/2015 ends on 27/04, as in the
  specimen.
- The output passes the renderer's SVG whitelist and its object/state contract.
- Colours are house tokens via `var()`, so light and dark both work.
- The pressed sentence appears in a fixed strip, so page text never moves.

Demo: `specimen/parts.html`, built from `fixtures/demo.json`.

**Adding a part:** only after the chairman praises a bespoke drawing of that object (`work/verdicts/` in the workshop).
Port it from that drawing, give it params, and add a fixture that reproduces the praised drawing. Heroes are not parts:
each hero is drawn for its lesson (postmortem cause 5).

**Not a part:** the litisconsórcio "seating chart" specimen. It is a 2×2 grid of named boxes, the shape the calibration
set calls text dressed as a drawing; it waits for a real seating plan of a hearing.
