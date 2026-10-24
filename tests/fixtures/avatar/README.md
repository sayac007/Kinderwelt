# Synthetic avatar privacy fixture

`gps-source.png` is a programmatically drawn geometric figure with transparency
and white clothing. It contains actual EXIF GPS tags for the fictional test
coordinate 0° N / 0° E, synthetic camera identifiers and a PNG iTXt GPS marker.
It is not a photograph, family image or real person's location. Created for
this repository's metadata-removal regression; repository MIT license applies.

The Godot avatar regression decodes and re-encodes this exact PNG through the
runtime importer, then checks the stored result has no EXIF/camera/GPS markers.
The fixture remains under `tests/` and must never be packaged in an Android app.
