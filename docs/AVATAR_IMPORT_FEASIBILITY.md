# Device-local PNG avatars

Implemented for **0.9.4 / 17** after the owner requested implementation. The
original feasibility assessment used application base
`a5c121d3e3744c395bb6a0580acdcfffb00c9e26`. No costume generation, server upload,
background-removal service or additional Android permission is used.

## Using the feature

In **Settings → parents/adults**, choose the localized import action:

| Language | Parent action | Help |
|---|---|---|
| German | Eigene Spielfigur als Bild laden | Hilfe |
| English | Load your own character image | Help |
| Russian | Выбрать своё изображение персонажа | Помощь |

Select a finished PNG from the device, inspect its preview against light and dark
checkerboards, then confirm. The imported figure becomes an additional eighth
choice; the seven existing family/neutral figures and their looks remain intact.
The selected image can already include any outfit created in the owner's own AI
image tool. Custom figures move as a whole image; body parts, costumes or missing
animation frames are not inferred from a photograph.

The character chooser offers **read-only Help** and selection of an already
imported figure. It has no picker, import, replacement or deletion controls.
Adding/replacing/removing an image is available only through the parents screen.
This navigation boundary is not represented as identity or age verification.

## Validation and local image handling

- PNG signature and chunk boundaries are checked, rather than trusting a name
  or a content URI's extension. Maximum input: **10 MiB, 4096 pixels per side**.
  Dimensions are bounded before full decoding.
- Actual decoded transparency is required; an opaque RGB or all-opaque RGBA PNG
  is rejected. Completely transparent/empty images are rejected too.
- Empty outer padding is trimmed, proportions are preserved, large images are
  reduced to at most **1024 pixels on the longest side**, and transparent padding
  is added. Small images are not enlarged to invent detail.
- White clothing, fur and highlights remain. Transparency checks cannot prove
  every edge is cut out correctly; an otherwise transparent image can still have
  a painted white rectangle. The preview and local Help support trying again.
- Validation errors/cancellation never replace the prior image or reset points.
  The selected file is read, never modified or deleted.

The runtime decodes the selection into pixels and re-encodes a new PNG. **No
original copy, source URI, filename, EXIF/GPS/camera/XMP metadata or separate
metadata record is persisted.** Only normalized pixels are stored under the
private app's `user://avatars/player.png`; no gallery output, network upload or
repository/CI image upload occurs. A temporary normalized file is renamed into
place only after a successful save.

Parent removal deletes this normalized copy and its pending temporary file.
**Reset** also deletes both, invalidates the texture cache and resets selection
and progress. The original device/gallery file is untouched. Missing/corrupt
private avatar data falls back to the default family figure without losing
otherwise valid saved points.

## Permissions and backup controls

The native Android document picker uses the selected document's URI through the
Storage Access Framework. The Android route refuses to open a fallback picker
when native file-dialog support is unavailable; it does not request additional
permissions. A real device still needs to confirm the picker/URI/lifecycle path.
If that path requires a new permission, stop and report it rather than adding one.

The APK/AAB verifier continues to reject **any** Android permission, including
media/storage/camera permissions. Backup remains disabled. In addition,
[the build policy](../scripts/android/backup_policy.py) installs debug/release
manifest overlays and explicit exclusions for root/files/databases/preferences/
external app data in both cloud backup and device transfer. The actual APK's
compiled rule resources and their manifest references are verified with aapt2.
This is technical configuration evidence, not a completed physical-device restore
test or Google Play/Families approval.

## Tests and remaining manual checks

[Runtime regression](../tests/avatar_import.gd) exercises opaque/empty/fake PNGs,
size bounds, proportional resizing, white-clothing preservation, read-only chooser
Help, parent import/replace/remove, task companions, seven sceneries, real
separate-process restart, point preservation and reset deletion.

[The synthetic privacy fixture](../tests/fixtures/avatar/README.md) contains actual
EXIF GPS 0° N / 0° E and synthetic camera/XMP markers. Pillow checks its structured
EXIF fields; the Godot test processes that exact source through the runtime
importer and checks the stored output has none of those metadata markers or an
original copy. This is generated test data, not a person's photo/location.
[Backup regressions](../tests/android/test_backup_policy.py) test both overlays,
incomplete policy rejection and real aapt2-compiled rules/manifest references.
All of these run without personal/family input files.

Use the complete test command documented in the root README. Current actual
results and family APK delivery are recorded in [Android](android.md) and the
[quality overview](QUALITY_ASSURANCE.md); no new run logs belong in Git.

Manual Android acceptance remains: parent-only navigation, system picker and URI
access without a permission request, cancel/back, rotation while selecting,
restart/update with points, deletion/reset and actual backup/restore behavior.
New help/error text has DE/EN/RU translations; no new spoken clips are claimed.

## Pinned engine evidence from the feasibility assessment

Godot `4.7.2.stable.official.ed1daf0bf`; official source inspected at
`ed1daf0bf001b61586d9930840f2f1394092c079`:

- [FileDialog](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/doc/classes/FileDialog.xml): native Android dialog requires `ACCESS_FILESYSTEM`.
- [Android FilePicker](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/platform/android/java/lib/src/main/java/org/godotengine/godot/io/FilePicker.kt): `ACTION_OPEN_DOCUMENT`, local-only sources and cancellation.
- [SAF access](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/platform/android/java/lib/src/main/java/org/godotengine/godot/io/file/SAFData.kt): content resolver/file-descriptor access.

The original read-only installed-engine probe passed 11 API-availability checks;
that probe did not claim an Android device picker round trip.
