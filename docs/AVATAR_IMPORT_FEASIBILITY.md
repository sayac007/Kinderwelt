# Device-local avatar import: feasibility only

Assessed on 2026-10-24 against application base
`a5c121d3e3744c395bb6a0580acdcfffb00c9e26` and Godot
`4.7.2.stable.official.ed1daf0bf`. No avatar-import feature, picker screen,
image transformation or imported-image APK has been implemented.

## Conclusion and first scope

**Feasible as a small addition.** A first PNG-based version should take roughly
4–8 focused implementation/test hours, followed by a real Android device check.
That is an estimate, not a completed implementation or a delivery guarantee.

The owner supplies the finished AI-modified figure, including its desired clothes.
The app only imports and displays it. It does not need to generate costumes,
remove a photo background or turn a portrait into a full-body animated character.

Recommended first version:

1. Add an image/plus action to the existing character chooser.
2. Open the native Android document picker for one local PNG.
3. Validate its signature, input byte size and dimensions **before full decoding**.
4. Fit it proportionally into a bounded avatar size, preserving transparency;
   show a preview and let the owner confirm it.
5. Save the normalized image in app-private `user://avatars/`, then show an
   additional selectable custom figure. Preserve existing family choices/points.
6. Persist the selection across restart; support replacing/removing the image.

A transparent, upright full-body PNG gives the best result. Different clothes can
already be part of each user-supplied picture. An opaque image retains its
background. Resizing does not create missing detail or improve a blurry source.

## Verified engine support

The official engine source was read at the exact installed commit
`ed1daf0bf001b61586d9930840f2f1394092c079`:

- [FileDialog documentation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/doc/classes/FileDialog.xml):
  native Android dialogs are supported with `use_native_dialog=true` and
  `ACCESS_FILESYSTEM`; image filters should include extensions and MIME types.
- [Android display server](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/platform/android/display_server_android.cpp):
  reports native file-dialog support and forwards selection to the Java picker.
- [Android FilePicker](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/platform/android/java/lib/src/main/java/org/godotengine/godot/io/FilePicker.kt):
  uses `ACTION_OPEN_DOCUMENT`, returns selected URIs, handles cancellation and
  requests local-only sources. This is device selection, not a server upload.
- [Android SAF file access](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/platform/android/java/lib/src/main/java/org/godotengine/godot/io/file/SAFData.kt):
  opens content URIs through `ContentResolver` and a file descriptor.
- [Image documentation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/doc/classes/Image.xml):
  runtime PNG/JPEG/WebP decoding, resizing and PNG saving are available.

A read-only headless probe of the installed binary confirmed **11 API checks**:
four FileDialog properties, PNG/JPEG/WebP loaders, `Image.resize`,
`Image.save_png`, `ImageTexture.create_from_image` and `FileAccess.open`.
This confirms API availability, **not a tested Android picker round trip**.
No extra native plugin appears necessary for the first scope. Broad gallery or
storage permissions should not be needed for an explicitly selected document;
that must still be checked in the resulting APK and on a device.

## Existing architecture and changes needed later

| Component | Current constraint and intended integration |
|---|---|
| [Character chooser](../games/quest/game.gd) | Fixed hero IDs, fixed look controls and localized names; add a custom entry and import/replace action without changing task logic. |
| [Hero renderer](../core/quest/hero.gd) | Preloaded cast, hip slicing for classic humans and continuous meshes for other sprites; use a runtime texture and whole-image idle/movement for imported art. Avoid slicing an arbitrary portrait into legs. |
| [Wardrobe](../core/quest/wardrobe.gd) | Depends on prepared atlas rectangles/masks; custom images bypass this path. The clothes come from the supplied image. |
| [Local saves](../core/save_store.gd) | Seven whitelisted IDs and per-hero looks; add a validated custom selection and fall back safely if its private image is absent/corrupt. Keep all earned points. |

The user-selected document can be copied/normalized while its URI grant is valid.
Persist the app-private copy rather than assuming the external URI remains
accessible after restart. Decode through `FileAccess` and the image's signature,
not by trusting the content URI's extension. Use `ImageTexture`, not editor-only
resource import or a rebuild of `res://`.

Suggested initial limits, to tune during implementation: 10 MiB input, maximum
4096 pixels per side and 16 megapixels, then at most 1024 pixels on the longest
output side. Read PNG header dimensions before allocating a full RGBA image;
a compressed-file limit alone does not bound decoded memory. Downscale without
stretching, keep transparent padding and reject invalid/truncated files cleanly.

No backend or image-search/AI service is required. Re-encoding only the decoded
pixels avoids retaining unrelated photo metadata. Keep imported files out of
logs, repository uploads and build artifacts. Existing Android backup is disabled.

## Acceptance work after implementation is requested

- Import, cancel, replace and delete; corrupt/oversized/tiny images; correct
  proportions/transparency; clear messages in German, Russian and English.
- Avatar selection/restart, missing-file fallback and unchanged points/saves.
- All worlds and both device orientations; avoid wardrobe/mask assumptions for
  arbitrary images and preserve existing family figures.
- A physical Android check of the native picker, content-URI read access,
  cancellation/back navigation and activity lifecycle. No Android device or
  emulator round trip was performed in this assessment.

JPEG/WebP, orientation metadata, adjustable cropping, multiple custom slots or
one imported image per existing look can follow. A broader version would likely
take 1–2 working days including device feedback. None of these additions is in
the current family test APK.
