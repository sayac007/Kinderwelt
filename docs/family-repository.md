# Getrenntes privates Repository für Familienfiguren

Gewünschte Trennung:

- `sayac007/Kinderwelt`: Godot-Code, neutrale Fantasiefiguren, gemeinsames Eichhörnchen und Build-/Prüfskripte.
- **`sayac007/Kinderwelt-Privat` muss privat sein**: sechs erzeugte Familienfiguren, sechs Kostümatlanten und `looks.json`/`names.json`, insgesamt 14 Dateien unter `characters/`. Keine Originalfotos oder Android-Signaturschlüssel.

Der zweite Bestand wurde lokal als eigenständiges Git-Repository unter `/workspace/Kinderwelt-family-assets` vorbereitet und committed. Dieser lokale Verzeichnisname bleibt unverändert; sein `origin` zeigt jetzt auf `https://github.com/sayac007/Kinderwelt-Privat.git`. Commit und Manifest-SHA sind in `scripts/ci/family-assets.json` festgelegt.

Am 22. Oktober 2026 hat der Benutzer das bereits angelegte Repository `sayac007/Kinderwelt-Privat` als Ziel benannt. Die öffentliche GitHub-API bestätigte HTTP 200, `private: false` und Größe 0; die Branch-Abfrage meldete HTTP 409 für das leere Repository. Es wurden **keine Familiengrafiken hochgeladen**. Der angemeldete API-Aufruf scheitert aktuell mit **HTTP 401 Bad credentials**. Ein öffentlicher Lesezugriff bestätigt keine funktionierende Schreibberechtigung.

## Noch erforderliche Einrichtung bei funktionierendem GitHub-Zugang

Zuerst das vorhandene [Repository auf privat umstellen](https://github.com/sayac007/Kinderwelt-Privat/settings) und den GitHub-Zugriff in der Cloud-Umgebung wiederherstellen. Ein nachträglicher Sichtbarkeitswechsel kann eine vorherige öffentliche Veröffentlichung nicht zurücknehmen. Deshalb prüft auch der Workflow weiterhin ausdrücklich `private: true`.

```sh
set -eu
# Kein Token gehört in den Chat. Bestehenden GitHub-Zugang sicher einrichten.
# Ausschließlich fortfahren, wenn der authentifizierte Abruf true bestätigt:
test "$(gh api repos/sayac007/Kinderwelt-Privat --jq .private)" = true
# Erst danach die vorbereiteten Bilder ins bestehende Repository übertragen:
git -C /workspace/Kinderwelt-family-assets push -u origin main
# Hauptcode und Workflow ebenfalls pushen:
git push origin feat/experience-polish
```

Bei inzwischen vorhandenen entfernten Commits zuerst abrufen und prüfen; kein Force-Push. Das bisherige Ziel `Kinderwelt-family-assets` wird nicht neu erstellt.

Für Actions einen **Fine-grained Personal Access Token** erzeugen, der ausschließlich das ausgewählte private Figurenrepository lesen darf: **Contents: Read**, Metadatenzugriff wie von GitHub vorgesehen. Diesen Wert im Hauptrepository unter **Settings → Secrets and variables → Actions → New repository secret** als `KINDERWELT_FAMILY_ASSETS_TOKEN` speichern. Ein bestehender Standard-`GITHUB_TOKEN` des Hauptrepositorys reicht für das zweite private Repository nicht aus. Keine Zugangsdaten im Repository oder als Build-Artefakt speichern.

[Actions-Secrets für Kinderwelt](https://github.com/sayac007/Kinderwelt/settings/secrets/actions). Es wurde kein PAT erfunden, keine Release-Signierung geändert und kein Schlüssel in Git geschrieben.

Danach baut ein vertrauenswürdiger Push oder manueller Workflowlauf beide Varianten. Actions liest den festgelegten Commit, prüft zusätzlich, dass das Figurenrepository wirklich privat ist, und importiert ausschließlich die 14 hashgeprüften erlaubten Dateien. Zugangsdaten werden von Checkout nicht dauerhaft gespeichert. **Pull Requests erhalten keinen Zugriff auf das Figurenrepository oder seinen Token** und prüfen ausschließlich die neutrale Variante; `pull_request_target` wird nicht verwendet.

## Lokale Reproduktion ohne GitHub-Secret

```sh
# In einem frischen Hauptcode-Checkout ohne .private/characters:
git clone /workspace/Kinderwelt-family-assets .private/family-assets
python3 scripts/ci/family_assets.py restore
python3 scripts/android/build_variants.py --tools /workspace/tools \
  --output build/android-delivery-neu
```

Die beiden fertigen APKs heißen exakt `kinderwelt-debug-family.apk` und `kinderwelt-debug-neutral.apk`. Zusätzlich entstehen `kinderwelt-unsigned-family.aab`, `kinderwelt-unsigned-neutral.aab`, Nachweise je Variante sowie `delivery.json`. Die APKs haben getrennte vorläufige Paketkennungen und können gleichzeitig installiert werden; lokale Spielstände sind getrennt. Es wird niemals eine neutrale APK als fehlende Familienversion ausgegeben. Fehlender Zugang oder ein falscher Manifest-Hash bricht den Familienbuild verständlich ab.

Alle großen APK-/AAB-Dateien stehen nur einmal im Ausgabeverzeichnis. Private Quellbilder, Repository-Metadaten und Zugangsdaten sind nicht Teil des hochgeladenen Actions-Artefakts. Die Familien-APK enthält naturgemäß die daraus sichtbaren Figuren; Zugriff und Aufbewahrung der Build-Artefakte müssen zur gewünschten privaten Nutzung passen.
