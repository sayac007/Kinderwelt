# Device-local character images

**Current implementation: 0.9.5 / 18, Play-preparation package 4.** The earlier
0.9.4 PNG-only implementation is retained as a compatibility case. Existing
1024-pixel private PNG figures remain readable without re-cropping or loss of
points. No costume generation, background-removal service or new permission.

## Parent workflow

Settings → For adults → Load your own character image (translated DE/EN/RU).
Choose a local **JPEG, PNG or static WebP** through the native system selector.
Opaque photos default to a round portrait. Drag or pinch to adjust it; accessible
zoom/reset buttons provide an alternative. A transparent cutout can keep the
**whole figure**, including its own AI-prepared clothes and white fur, or use a
round crop. No white-pixel removal is attempted. Confirming adds the existing
custom eighth choice; all seven bundled figures and their looks remain intact.
Prepared wardrobe masks remain disabled for custom images, with an explanation.

Adding/replacing/deleting is available only in the existing parents area. Child
chooser Help is read-only and contains no picker, editing or deletion controls.
This navigation boundary is not identity or age verification. Reframing later
requires choosing the original again: the app deliberately retains no original.

## Pixel processing and storage

- Input byte signatures/container boundaries and dimensions are checked before
  full decode: **20 MiB, 4096 pixels per side, 16,777,216 pixels**. File extensions
  and provider MIME strings are not trusted. Unsupported HEIC/GIF/etc., animated
  inputs, truncated or oversized streams produce localized recoverable messages.
- JPEG/PNG/WebP EXIF orientations 1–8, including mirrors, are applied. Decoded
  working pixels are reduced to **1024 pixels maximum** in memory for editing;
  confirmed output is **at most 512 pixels**. Small images are not upscaled.
- The live crop is a lightweight texture/shader preview; panning does not encode
  a new image every frame. Confirmation bakes the selected region into pixels.
  All RGBA data outside a circular frame is cleared, not just hidden by alpha.
- Only a new pixel-only PNG is atomically saved as
  **`user://avatars/player.png`**, in private app storage. No original, URI,
  filename, EXIF/GPS/camera/XMP data or crop sidecar is persisted or logged by
  the importer. The original device/gallery file is never changed or deleted.
- Cancel/rejected replacement preserves the previous figure and earned points.
  Parent deletion and reset delete the normalized PNG, pending `.tmp` and texture
  cache. A missing/invalid private image falls back without discarding points.
- The localized privacy note concerns **the app copy**: no upload/sharing and
  exclusion from app backups. The app does not control the original photo's
  gallery/provider cloud settings or the system picker's own recent selections.

## Permissions and backups

The existing Godot native Android SAF document-selection route is kept. It uses
selected-document URI access, never broad media/storage or camera permissions.
No camera, network, share/export, cloud or analytics path is added. Native-dialog
support is checked before opening on Android; no permission-requesting fallback
is used. If a real device requires an extra permission, stop/report rather than
adding one. System-picker/provider behaviour still needs device acceptance.

The existing [backup policy](../scripts/android/backup_policy.py) and APK/AAB
verifier still require zero permissions, `allowBackup=false` and explicit cloud
and device-transfer exclusions. Compiled APK rule references/contents are checked;
this is not a physical backup/restore certification.

## Regressions and manual acceptance

[Runtime import/restart tests](../tests/avatar_import.gd) preserve earlier cutout,
white-clothing, point, parent-only, reset and seven-scene checks. New
[crop/format regressions](../tests/avatar_crop.gd) use 24 tiny synthetic JPEG/PNG/
WebP inputs with real GPS/camera EXIF and all eight orientation values. Pixel
probes come independently from Pillow ImageOps. Saved PNGs are checked for
metadata removal, private-only output, crop selection and pixel-identical reload.
Actual touch events exercise pinch/drag; rotation cancels stale touches without
resetting crop, and legacy 1024px figures remain intact.

[Fixture provenance and generator](../tests/fixtures/avatar/README.md) contain no
real photographs or locations. Static dependency checks reject network/camera/
permission APIs in the runtime import path. The full tests and render wrapper
use isolated user directories; generated QA renders show synthetic inputs only.
Run through the root README commands, not against a real user's saved figures.

**NOT VERIFIED:** actual selection/URI/cancel/lifecycle on Android 13+ and Android
10–12, hardware rendering/performance, update and real backup/device transfer.
[Device acceptance](ACCEPTANCE.md) specifies these steps. Current actual command
results and artifacts belong in [the central quality overview](QUALITY_ASSURANCE.md),
not new per-run documents under `docs/qa/`. Help/error text is written DE/EN/RU;
no new spoken clips or three-language voice identity are claimed.

## Existing pinned engine evidence

Godot `4.7.2.stable.official.ed1daf0bf`, official commit
`ed1daf0bf001b61586d9930840f2f1394092c079`:

- [Native FileDialog](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/doc/classes/FileDialog.xml), Android `ACCESS_FILESYSTEM`.
- [Android FilePicker](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/platform/android/java/lib/src/main/java/org/godotengine/godot/io/FilePicker.kt), local-only SAF selection/cancel.
- [SAF access](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/platform/android/java/lib/src/main/java/org/godotengine/godot/io/file/SAFData.kt), selected content-resolver file descriptors.

The previous installed-engine API probe passed 11 checks. It did not perform a
physical Android picker round trip; the same limitation applies to desktop tests.
