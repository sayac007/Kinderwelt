# APK-Größe 0.4: Analyse vor Optimierung

Alle Angaben sind **dezimal MB (1 MB = 1000000 Bytes)** oder exakte Bytes.
Messdaten und größte ZIP-Einträge: [apk-size-v04.json](apk-size-v04.json).
Es wurden weder ABIs noch Spielinhalte entfernt oder Engine-Funktionen blind gestrichen.

| Schritt | Universal-Debug-APK | AAB | Aussage |
|---|---:|---:|---|
| Tatsächliche 0.3-Lieferung | 164121430 Bytes | 53755876 Bytes | Ausgangsmessung |
| Nur native Bibliotheken komprimieren, noch 0.3-Inhalte | 64093414 Bytes | 53755877 Bytes | Isolierte Optimierungsprobe |
| Fertige 0.4 mit neuen Figuren, Grafiken, zehn Titeln und Sprache | **65764990 Bytes** | **55406003 Bytes** | Endartefakte |

Die fertige APK ist gegenüber 0.3 **59,93 % kleiner** und erfüllt das vorläufige
120-MB-Ziel. Die neuen Inhalte erhöhen die komprimierte Probe um rund 1,67 MB.
Ein-Byte- bzw. kleinere Metadatenabweichungen zwischen Builds sind keine Inhaltsoptimierung;
Zeitstempel und neue Entwicklungssignaturen verhindern eine Zusage byteidentischer APKs.

## Nachgewiesene Ursache und Maßnahme

Die alte APK enthielt rund **160,08 MB unkomprimierte native Bibliotheken** für zwei ABIs.
Allein `libgodot_android.so` belegte etwa 76,18 MB (arm64) bzw. 81,19 MB (x86_64).
Audio war damals nur rund 1,31 MB komprimierter ZIP-Inhalt. Neue Bilder oder Musik zu
entfernen hätte die Hauptursache nicht behoben.

Beide Exportpresets setzen jetzt `gradle_build/compress_native_libraries=true`.
Godots offizielle Gradle-Vorlage verwendet damit komprimierte native Libraries und
`extractNativeLibs=true`. Die Android-Verifikation prüft das tatsächlich in APK/AAB,
zusätzlich zu ELF-/ZIP-Ausrichtung und den übrigen bisherigen Prüfungen.

**Alle vier nativen Bibliotheken der APK haben vor und nachher identische SHA-256-Werte
für ihren entpackten Inhalt.** Die Maßnahme ist verlustfrei. Beide ABIs bleiben vorhanden.
Android extrahiert diese Bibliotheken bei Installation: Die kleinere Download-/Archivgröße
ist **kein Nachweis einer entsprechend kleineren installierten App**. Installationszeit,
Speicherplatz und Performance sind auf einem echten Gerät noch zu messen.

## Endgültige Universal-APK nach Gruppen

| Gruppe | Unkomprimiert | Im ZIP gespeichert |
|---|---:|---:|
| Native arm64-v8a, 2 Dateien | 77555944 | 28340126 |
| Native x86_64, 2 Dateien | 82524296 | 31735164 |
| Audio, 33 importierte Dateien | 3176867 | 2892702 |
| Grafiken/Texturen einschließlich Android-Icons, 55 Dateien | 151318 | 150943 |
| Anwendungsdaten, Importmetadaten und Code, 161 Dateien | 229479 | 182423 |
| Android-Metadaten/DEX/Klassen, 70 Dateien | 6188161 | 2407333 |
| Separat gepackte Fonts | 0 | 0 |

ZIP-Zentralverzeichnis, Signatur und Ausrichtungs-Overhead werden im JSON gesondert
bilanziert. Godots eingebaute Fallback-Schrift steckt in der Engine; sie wurde nicht als
„kostenlos“ oder separat entfernt dargestellt. Der Analyzer erkennt auch Godots
`.oggvorbisstr`-Importformat als Audio und zählt nicht nur Quelldateiendungen.

Die grafische Darstellung verwendet kleine Original-SVGs und gezeichnete gemeinsame
Körperteile statt großer Spritebilder oder 3D-Modelle. Die Musikbox lädt nur aktuelle und
überblendende Titel; keine zehn vollständig vorab geladenen Stücke. Neue Musik ist Vorbis
q5, Sprache q4, jeweils mono 22050 Hz. Das spart Platz, ersetzt aber keine menschliche
Hörprüfung. [Codecprüfung und offene Qualitätsziele](audio-v04.md).

## Gerätepakete und Play-Ziel

Das AAB enthält beide ABIs und ist mit rund 55,41 MB bereits kleiner als die universelle
Debug-APK. Bei gerätespezifischer Zustellung kann die jeweils andere ABI entfallen:
x86_64 trägt im Debug-ZIP etwa 31,74 MB, arm64 etwa 28,34 MB bei. Diese Zahlen sind echte
Archivanteile, **keine gemessenen oder separat erzeugten gerätespezifischen Downloads**.

Das 80-MB-Ziel für einen späteren Play-Gerätedownload bleibt deshalb **nicht gemessen**.
Eine verbindliche Zahl benötigt Bundle-/Play-Zustellung auf eine definierte Gerätekonfiguration
und die noch fehlende sichere dauerhafte Signatur und Freigabe. Es wird keine Uploadbereitschaft
behauptet. Weitere mögliche Schritte wären ein explizites ABI-Testpaket oder ein separat
validierter kleinerer Godot-Exporttemplate-Build. Da das 120-MB-Ziel ohne Inhaltsverlust
erreicht wurde, wurden diese risikoreicheren Änderungen hier nicht durchgeführt.

## Reproduzieren

```bash
python3 scripts/android/analyze_size.py \
  build/android-0.3-first-mission/kinderwelt-debug.apk \
  build/android-0.4-compression-experiment/kinderwelt-debug.apk \
  build/android-0.4-final/kinderwelt-debug.apk \
  --output /tmp/kinderwelt-size-comparison.json
```

Die alten Artefakte müssen dafür vorhanden sein; die gemessenen Befunde sind im Repository
archiviert. Jeder neue Android-Build schreibt automatisch `size-analysis.json` für seine
APK und sein AAB neben die Signatur-/Manifest-/Provenienzberichte.
