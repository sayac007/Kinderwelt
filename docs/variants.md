# Private und öffentliche Variante

`family` bleibt der Standard für private Android-Builds. Der dafür nötige private Grafikpack liegt ausschließlich in `.private/characters/` und ist über `.gitignore` ausgeschlossen. `public` verwendet sechs neu erfundene Figuren aus `art/public/characters/` und das gemeinsam genutzte Eichhörnchen. Animationen, Auswahl, Kleidung, Aufgaben und Spielmechanik sind gleich. Die internen Speicherkennungen bleiben stabil; lokale Lösungen und Kleiderwahl müssen nicht umgeschrieben werden. Angezeigte Namen kommen aus dem jeweiligen Pack.

```sh
# Privater Arbeitsplatz mit wiederhergestelltem Pack:
python3 scripts/variants.py prepare --variant family --output .
python3 scripts/android/build.py --variant family --output build/family-neu
# Öffentliche, vom privaten Pack unabhängige Ausgabe:
python3 scripts/variants.py prepare --variant public --output .
python3 scripts/android/build.py --variant public --output build/public-neu
```

Ohne privaten Pack bricht ein ausdrücklich gewählter Familienbuild verständlich ab. Tests wählen mit `KINDERWELT_VARIANT=public` die öffentliche Variante; `auto` verwendet privat, wenn der Pack vorhanden ist, sonst öffentlich. GitHub Actions wählt ausdrücklich `public`. Vor direktem Öffnen im Godot-Editor einmal `prepare` ausführen. Die erzeugten `core/quest/cast.gd`, `assets/quest/cast.json`, `looks.json` und `characters/` sind ignorierte Arbeitsdateien. Die Materialisierung verändert den lokalen Quellpack nicht. Die gesonderte Größenoptimierung und ihre Sicherung sind in `repository.md` beschrieben.

Der private Pack enthält sechs normale PNGs, sechs Kostüm-PNGs, `looks.json` und `names.json`. Der ursprüngliche Pack ist lokal unter `build/private-family-art.zip` gesichert, die optimierte Build-Fassung unter `build/private-family-art-optimized.zip`. Zum Wiederherstellen den gewünschten Pack privat unter `.private/` entpacken, sodass `.private/characters/looks.json` existiert. Dieses Archiv privat sichern, nicht zu GitHub oder in einen öffentlichen Download hochladen. Ein frischer Checkout besitzt den Pack absichtlich nicht. Alte Review-Bilder liegen lokal in `.private/review/`.

Einen sauberen Quellschnappschuss mit `python3 scripts/variants.py public-source --output build/public-source-neu` erstellen. Er enthält keine Git-Historie; interne Notizen, private Packs und Vorschauarchive werden nicht kopiert.

Ein öffentlicher Quellschnappschuss darf nur App, öffentliche Grafikquellen, Skripte, Tests und bereinigte Dokumentation enthalten, niemals `.private`, `.git`, `docs/internal` oder private Build-Ausgaben. Ein variantenspezifischer App-Snapshot enthält nur die gewählten Figurenressourcen. Der Android-Verifier kontrolliert das deklarierte Ressourcenprofil und weist private Figurenressourcen in öffentlichen Paketen zurück.

**Grenze:** `.gitignore` und das Entfernen aus dem aktuellen Stand löschen keine bereits veröffentlichte Git-Historie. Frühere Commits und Artefakte können noch ältere Grafiken enthalten. Es wurde keine History-Umschreibung oder Löschung entfernter Releases durchgeführt. Für eine vollständig getrennte öffentliche Veröffentlichung einen bereinigten Quellschnappschuss ohne `.git` in ein neues Repository übernehmen.
