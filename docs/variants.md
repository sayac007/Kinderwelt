# Familien- und neutrale Variante

`family` enthält die sechs erzeugten Familienfiguren und das gemeinsame Eichhörnchen. `public` ist die interne Kennung für die **neutrale** Ausgabe mit Nova, Lumi, Karo, Tavi, Zora, Flocke und Eichhörnchen. Beide Varianten besitzen je sieben Figuren und dieselben fünf Looks, Aufgaben, Animationen und Welten. Alle stabilen Speicherkennungen bleiben erhalten.

Die Familienquellen werden jetzt aus dem getrennten privaten Repository `sayac007/Kinderwelt-Privat` bezogen. Nur die 14 erlaubten abgeleiteten Dateien werden in `.private/characters/` importiert. Originalfotos werden weder dort benötigt noch in das neue Figurenrepository aufgenommen. Hauptcode und öffentliche Quellschnappschüsse enthalten keine privaten Quellbilder. [Einrichtung, bestätigter privater Upload und noch erforderlicher Actions-Lesetoken](family-repository.md).

```sh
# Beide benannten Android-Ausgaben, nach geprüftem Familienimport:
python3 scripts/android/build_variants.py --output build/android-delivery-neu
# Rein neutrale Ausgabe ohne private Quellen:
python3 scripts/android/build_variants.py --variants neutral --output build/android-neutral-neu
# Godot-Arbeitsplatz materialisieren:
python3 scripts/variants.py prepare --variant auto --output .
```

Die Artefakte heißen exakt `kinderwelt-debug-family.apk` und `kinderwelt-debug-neutral.apk`. Sie verwenden getrennte vorläufige Paketkennungen und lokale Spielstände. Jede APK enthält nur den gewählten Figurenbestand. Quelle, Version, Paket, Signaturstatus und SHA256 stehen in `delivery.json` und den Berichten je Variante. APKs werden nur temporär für Tests signiert; AABs bleiben unsigniert.

Ohne Familienquellen bricht ein angeforderter Familienbuild verständlich ab; eine zweite neutrale APK wird niemals als Ersatz ausgegeben. Tests wählen mit `KINDERWELT_VARIANT=public` neutral oder mit `auto` einen verfügbaren Bestand. Erzeugte Arbeitsdateien (`core/quest/cast.gd`, `assets/quest/cast.json`, `looks.json`, `characters/`) bleiben ignoriert.

Aktuelle Figurenherkunft und Grenzen: [Herkunftsprüfung](character-origins.md). Alle aktiven Bildquellen sind auf hier erzeugte KI-Ausgaben zurückgeführt; deren heutige Hashes werden vor Android-Export geprüft. Die vier früheren Bilder bleiben aus aktiven Paketen ausgeschlossen.

`python3 scripts/variants.py public-source --output build/public-source-neu` erzeugt einen neutralen Quellschnappschuss ohne Git-Historie, private Bilder oder interne Notizen. Lokale frühere Sicherungen unter `build/private-family-art*.zip` bleiben privat. **Das getrennte Repository und `.gitignore` entfernen keine älteren Familiengrafiken oder anderen Dateien aus der bisherigen Git-Historie.** Eine History-Umschreibung oder entfernte Löschung wurde nicht vorgenommen.
