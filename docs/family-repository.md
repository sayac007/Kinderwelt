# Getrenntes privates Repository für Familienfiguren

Gewünschte Trennung:

- `sayac007/Kinderwelt`: Godot-Code, neutrale Fantasiefiguren, gemeinsames Eichhörnchen und Build-/Prüfskripte.
- **`sayac007/Kinderwelt-family-assets` muss privat sein**: sechs erzeugte Familienfiguren, sechs Kostümatlanten und `looks.json`/`names.json`, insgesamt 14 Dateien unter `characters/`. Keine Originalfotos oder Android-Signaturschlüssel.

Der zweite Bestand wurde lokal als eigenständiges Git-Repository unter `/workspace/Kinderwelt-family-assets` vorbereitet und committed. Commit und Manifest-SHA sind in `scripts/ci/family-assets.json` festgelegt. Die GitHub-Erstellung wurde mit `gh repo create --private` versucht, aber die API antwortete **Forbidden**. Das entfernte Repository ist deshalb **noch nicht als erstellt bestätigt**. Git-Fetch mit vorhandener Anmeldung scheiterte zudem mit **Invalid username or token**.

## Noch erforderliche Einrichtung bei funktionierendem GitHub-Zugang

```sh
# Zuerst die GitHub-Verbindung/Anmeldung erneuern, keinen Token in den Chat kopieren.
gh repo create sayac007/Kinderwelt-family-assets --private \
  --source /workspace/Kinderwelt-family-assets --remote origin --push
# Sichtbarkeit ausdrücklich prüfen:
gh api repos/sayac007/Kinderwelt-family-assets --jq .private
# Muss true ergeben.
```

Für Actions einen **Fine-grained Personal Access Token** erzeugen, der ausschließlich das ausgewählte private Figurenrepository lesen darf: **Contents: Read**, Metadatenzugriff wie von GitHub vorgesehen. Diesen Wert im Hauptrepository unter **Settings → Secrets and variables → Actions → New repository secret** als `KINDERWELT_FAMILY_ASSETS_TOKEN` speichern. Ein bestehender Standard-`GITHUB_TOKEN` des Hauptrepositorys reicht für das zweite private Repository nicht aus. Keine Zugangsdaten im Repository oder als Build-Artefakt speichern.

[Private Repositorys erstellen](https://github.com/new), [Actions-Secrets für Kinderwelt](https://github.com/sayac007/Kinderwelt/settings/secrets/actions). Es wurde kein PAT erfunden, keine Release-Signierung geändert und kein Schlüssel in Git geschrieben.

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
