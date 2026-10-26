# Getrenntes privates Repository für Familienfiguren

Gewünschte Trennung:

- `sayac007/Kinderwelt`: Godot-Code, neutrale Fantasiefiguren, gemeinsames Eichhörnchen und Build-/Prüfskripte.
- **`sayac007/Kinderwelt-Privat` muss privat sein**: sechs erzeugte Familienfiguren, sechs Kostümatlanten und `looks.json`/`names.json`, insgesamt 14 Dateien unter `characters/`. Keine Originalfotos oder Android-Signaturschlüssel.

Der zweite Bestand wurde lokal als eigenständiges Git-Repository unter `/workspace/Kinderwelt-family-assets` vorbereitet und committed. Dieser lokale Verzeichnisname bleibt unverändert; sein `origin` zeigt jetzt auf `https://github.com/sayac007/Kinderwelt-Privat.git`. Commit und Manifest-SHA sind in `scripts/ci/family-assets.json` festgelegt.

Am 22. Oktober 2026 hat der Benutzer das bereits angelegte Repository `sayac007/Kinderwelt-Privat` als Ziel benannt. Die öffentliche GitHub-API bestätigte HTTP 200, `private: false` und Größe 0; die Branch-Abfrage meldete HTTP 409 für das leere Repository. Es wurden **keine Familiengrafiken hochgeladen**. Der angemeldete API-Aufruf scheitert aktuell mit **HTTP 401 Bad credentials**. Ein öffentlicher Lesezugriff bestätigt keine funktionierende Schreibberechtigung.

## Bestätigter Upload und noch erforderliches Actions-Secret

Der Benutzer hat die Dateien manuell hochgeladen. Der authentifizierte GitHub-Abruf bestätigt jetzt **private: true** und Schreibzugriff der Cloud-Sitzung. Der tatsächlich entfernte Commit `5a35f7675eb1a0881447005fbe51dc089ef8471f` wurde abgerufen; alle 14 Familiengrafik-/Katalogdateien stimmen exakt mit dem unveränderten Manifest überein und bestehen den Importer. `scripts/ci/family-assets.json` verweist jetzt auf diesen neuen Commit statt den nur lokal existierenden ursprünglichen Commit. Das Fehlen der zwei versteckten Git-Regeldateien beim Browser-Upload verändert die zugelassenen App-Bilder nicht.

Das Lesen der Actions-Secret-Liste über die aktuelle Integration scheitert mit **HTTP 403 Resource not accessible by integration**. Deshalb ist nicht bestätigt, ob `KINDERWELT_FAMILY_ASSETS_TOKEN` bereits existiert. Diese Einschränkung betrifft Secrets; Repository-Lese-/Schreibzugriff ist bestätigt. Der Token muss sicher über GitHub eingerichtet werden, nicht im Chat oder Code.

Für Actions einen **Fine-grained Personal Access Token** erzeugen, der ausschließlich das ausgewählte private Figurenrepository lesen darf: **Contents: Read**, Metadatenzugriff wie von GitHub vorgesehen. Diesen Wert im Hauptrepository unter **Settings → Secrets and variables → Actions → New repository secret** als `KINDERWELT_FAMILY_ASSETS_TOKEN` speichern. Ein bestehender Standard-`GITHUB_TOKEN` des Hauptrepositorys reicht für das zweite private Repository nicht aus. Keine Zugangsdaten im Repository oder als Build-Artefakt speichern.

[Actions-Secrets für Kinderwelt](https://github.com/sayac007/Kinderwelt/settings/secrets/actions). Es wurde kein PAT erfunden, keine Release-Signierung geändert und kein Schlüssel in Git geschrieben.

Danach baut ein ausdrücklich manueller Workflowlauf mit `variant=family` oder `variant=both` die gewünschten Familienvarianten. Pushes auf `main` und Pull Requests bauen nur neutral und laden keine Artefakte hoch. Actions liest den festgelegten Commit, prüft zusätzlich, dass das Figurenrepository wirklich privat ist, und importiert ausschließlich die 14 hashgeprüften erlaubten Dateien. Zugangsdaten werden von Checkout nicht dauerhaft gespeichert. **Pull Requests erhalten keinen Zugriff auf das Figurenrepository oder seinen Token** und prüfen ausschließlich die neutrale Variante; `pull_request_target` wird nicht verwendet.

## Lokale Reproduktion ohne GitHub-Secret

```sh
# In einem frischen Hauptcode-Checkout ohne .private/characters:
git clone /workspace/Kinderwelt-family-assets .private/family-assets
python3 scripts/ci/family_assets.py restore
python3 scripts/android/build_variants.py --tools /workspace/tools \
  --output build/android-delivery-neu
```

Die beiden fertigen APKs heißen exakt `kinderwelt-debug-family.apk` und `kinderwelt-debug-neutral.apk`. Zusätzlich entstehen lokal unsignierte AABs, Nachweise je Variante sowie `delivery.json`. AAB-Uploads sind separat über `include_unsigned_bundles=true` anzufordern; neue Downloads laufen nach drei Tagen ab. Siehe [Speicherregeln](ci-artifacts.md). Die APKs haben getrennte vorläufige Paketkennungen und können gleichzeitig installiert werden; lokale Spielstände sind getrennt. Es wird niemals eine neutrale APK als fehlende Familienversion ausgegeben. Fehlender Zugang oder ein falscher Manifest-Hash bricht den Familienbuild verständlich ab.

Alle großen APK-/AAB-Dateien stehen nur einmal im Ausgabeverzeichnis. Private Quellbilder, Repository-Metadaten und Zugangsdaten sind nicht Teil des hochgeladenen Actions-Artefakts. Die Familien-APK enthält naturgemäß die daraus sichtbaren Figuren; Zugriff und Aufbewahrung der Build-Artefakte müssen zur gewünschten privaten Nutzung passen.
