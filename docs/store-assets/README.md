# Original icon and screenshot drafts

The icon is original repository artwork (same project licence). The 512×512 PNG
has a square opaque background; Play applies its own mask. Regenerate from root
with the pinned Godot and writable XDG directories:
`"$GODOT" --headless --path . --script scripts/android/prepare-icon.gd`.
Adaptive icon masks, monochrome appearance, splash and launcher rendering still
need inspection on actual Android devices. No trademark clearance is implied.

The five 768×1024 PNGs were copied unchanged from synthetic real Godot desktop
renders made for the merged quality work, source files
`/tmp/kinderwelt-quality-renders-checked/{module}_00_768x1024_p00.png`.
The source modules are unchanged by task 05. The capture manifest records task
IDs bridge_01, market_01, garden (language), ramp (autonomy), music (social).
They contain no people or personal data and are explicitly desktop previews,
not Android screenshots. The source capture procedure is tests/qa/render.sh;
it can regenerate current previews on a graphical backend. Store-ready captures
from the eventual signed release on phones/tablets remain a manual gate.
