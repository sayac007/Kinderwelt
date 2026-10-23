# Quellen, Vorschauen und Grafikgrößen

App-Ressourcen liegen einmal unter `assets/`; öffentliche Figurenquellen unter `art/public/`. Private Grafiken gehören ausschließlich in den ignorierten lokalen Pack. Die Materialisierung wählt genau einen Figurenbestand für den App-Export. Details: [Varianten](variants.md).

Doppelte Figuren-PNGs, ZIP-Pakete sowie Musik-/Sprach-MP3-Vorschauen sind aus `docs/` entfernt. `scripts/qa/previews.py` erzeugt aktuelle Vorschauen unter `build/`. Alte Beschreibungen und Sitzungsnotizen liegen lokal unter `docs/internal/`, das ignoriert und beim öffentlichen Quellexport ausgeschlossen ist. Auch private Backups dürfen nicht ins öffentliche Repository geladen werden.

Das Entfernen aktueller Dateien verkleinert einen frischen Quellstand, **bereinigt aber keine ältere Git-Historie oder bereits hochgeladene Artefakte**. Dafür wäre eine gesonderte Entscheidung zu Historie, vorhandenen Klonen und externen Dateien nötig. Der Export `public-source` enthält keine Git-Historie und keinen privaten Pack.

## Grafikoptimierung

Pillow-Lanczos-Skalierung in RGBA, keine Farbpaletten-Quantisierung: private klassische Figuren 512×768, Kostümatlanten 768×1152, gemeinsames Eichhörnchen 640×768 und Kostümatlas 768×1152, Kulissen 1296×864, Android-Icon 512×512. Öffentlicher Figurenatlas bleibt 1024×1536 und wird nur verlustfrei als PNG neu komprimiert. Objektatlanten behalten ihre Koordinaten und Auflösung.

Die ursprünglichen privaten Quellen sind vor der Optimierung separat lokal gesichert. `scripts/graphics/optimize.py` erzeugt die verkleinerten Ressourcen; anschließend `scripts/graphics/compile_wardrobe.py family` ausführen, damit Grenzen, Hashes und Masken zu den tatsächlichen Pixeln passen. Für öffentliche Figuren `scripts/graphics/compile_public.py` ausführen: enge Alpha-Grenzen und Kostümmasken verhindern benachbarte Bildfragmente; das PNG wird dabei nicht verändert. Erneutes Resampling bereits passender Größen findet nicht statt. Der Optimierungsbericht [graphics-optimization.json](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/qa/graphics-optimization.json) dokumentiert die ausgeführte Änderung; private Dateien werden öffentlich nur zusammengefasst.

Die 19 bearbeiteten PNGs schrumpften als Quelldateien von **46.194.894 auf 20.729.183 Bytes**. Das ist **keine APK-Größenmessung**. Godot importiert eigene Texturformate; tatsächliche Android-Archivgrößen werden separat mit `scripts/android/analyze_size.py` ermittelt und im [Testbericht](test-report.md) verglichen. Die Ausgangs-APK 0.7.1 und der neue Stand unterscheiden sich auch in Sprachinhalten und Variantenmetadaten; die gesamte Größendifferenz darf daher nicht allein PNG-Kompression zugeschrieben werden.

## Musiknachweise

`python3 scripts/music/notices.py` reproduziert die Hinweise ohne Audio-Neuerzeugung. Wiener Blut dokumentiert den vierstimmigen Auszug und Vierteltempo 180; Puccini die MIDI-Zeitskalierung mit Faktor 1.65. Andere Stücke nennen ihre konkrete Notenvorlage und tatsächliche LilyPond-Aufbereitung. Die 20 ursprünglichen Lizenzzeilen samt Links bleiben bytegleich gesichert; Quelldateien und Lizenzen sind unverändert.
