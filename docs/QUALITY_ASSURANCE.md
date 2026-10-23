# Kinderwelt: Qualität und Prüfstand

**Zielgruppe:** Klasse 1–2, aktuelle Aufgaben für die zweite Klasse. Ein lokales Godot-Lernabenteuer mit 320 Grundaufgaben und 640 freiwilligen Boni. Kein Wirksamkeitsnachweis und keine Google-Play-Freigabe.

## Orientierung

| Bereich | Inhalt / zuständige Dateien |
|---|---|
| Lernen | Je 40 Stationen in Mathe, Sprache, Logik, Physik, Biologie, Chemie, Mensch, Geografie; Sprache jeweils DE/EN/RU. Zahlen-/Wort-/Regelrätsel, Sachfragen mit indirekten Bildhinweisen. |
| App | `core/quest/main.tscn` und `core/quest/`: Oberfläche, Weltbewegung, Aufgaben, Audio, lokaler Spielstand; keine externe Spielserver-Abhängigkeit. |
| Redaktion | `scripts/content/generate.py` kompiliert versionierte TSV-/JSON-Quellen und `advanced.py`/`experience.py` nach `games/quest/`. [Quellen und Ablauf](CONTENT_AUTHORING.md). |
| Medien | Lokale Vorbisclips: DE/RU Serena, EN LJSpeech. [Sprachverfahren und Hörgrenzen](voice.md). [Musik](music.md), [Bildherkunft](character-origins.md). |
| Varianten / Android | Getrennte neutrale und private Figurenquellen; [Build und technische Paketprüfung](android.md). Keine privaten Familien-Assets für neutrale Tests nötig. |

## Ausführen

Dieselben Befehle wie im [README](../README.md):

```sh
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/run.sh
# Mit grafischer Sitzung oder xvfb-run:
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/qa/quest-render.sh qa-results/visual
python3 scripts/qa/documentation.py --check
```

Die bestehende CI ruft die vollständige Suite und die grafische Suite auf. Laufzeitdaten landen in `qa-results/`; Android-Ausgaben in `build/`. Kein neuer APK-/AAB-Build ist für diese Dokumentationsarbeit beauftragt.

## Letzter belegter Ausgangsstand

**Commit `a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e`, 23.10.2026**; über PR #13 in `main` übernommen. Die folgenden Ergebnisse stammen aus diesem Stand, nicht aus einer vorweggenommenen KW-QA-01-Freigabe. [Vollständiger damaliger Bericht](https://github.com/sayac007/Kinderwelt/blob/a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e/docs/test-report.md).

| Dimension | Tatsächlich verifiziert / Grenze |
|---|---|
| Spiellogik / Punkte | Familien-Suite: 88 Python-Tests, 6056 Aufgaben-, 3608 Welten-, 991 Punkteprüfungen bestanden; Neustart mit 3360 Punkten. Neutraler Start separat bestanden, keine zweite volle Suite. |
| Audio | Alle 2719 Dateien decodiert; 36 Wiedergabe-, 75 Sequenz-, 38 Weltsprachprüfungen bestanden. ASR-Stichprobe ist keine Hörfreigabe. |
| Darstellung | 461 echte Renderbilder in vier Displayprofilen/drei Sprachen; kein vollständiger manueller Bild- oder Gerätetest. |
| Android | 0.9.1: kein neuer Export. Ältere 0.9.0-APK-/AAB-Nachweise im Archiv; sie belegen keine aktuelle Uploadbereitschaft. |
| Datenschutz | Quell-/Konfigurationsaudit ohne Netzwerk-/Konten-/Werbeintegration bestanden. Lokale Spielstände; keine personenbezogenen Testdaten neu erhoben. Keine umfassende Datenschutz-/Sicherheitszertifizierung. |
| Pädagogik | Vor KW-QA-01 offen: verratende Hinweise, Logik-/Bonusduplikate, 33 auffällige Grundaufgaben und Fachsprache. Tests beweisen keine Lernwirkung oder passende Schwierigkeit für jedes Kind. |

## KW-QA-01: Dokumentation konsolidiert

139 Dateien / **7.383.943 Bytes** wurden im verifizierten Git-Archiv erhalten; `docs/qa/` enthält jetzt zwei notwendige Referenzdateien / **78.669 Bytes**. Keine Historie gelöscht. Alle 139 Remote-Blobs samt Archivtag geprüft, lokale Dokumentations- und CI-Dateiverweise gültig; zwei neue Linkregressionen und der umgezogene ASR-Fixture-Test bestanden. GitHub-Einstellungs-/Actionsseiten erfordern Anmeldung; keine allgemeine öffentliche HTTP-Erreichbarkeit behauptet. [Inventar und Ablageentscheidung](qa/README.md).

## Offene Inhaltsprüfung und Freigaben

Zuerst Dokumentation konsolidieren, danach Inhaltsquellen korrigieren und offline testen. Ergebnisse, Ausnahmen, korrigierte Aufgabenanzahl, betroffene Sprachdateien und der tatsächlich getestete Commit werden **hier** nach erfolgreicher Durchführung ergänzt. Muttersprachliches Hören, Fachreview, Tests mit Kindern und reale Android-Geräte-/Updateprüfungen bleiben eigene Freigaben. Für eine Kinderstudie sind Protokoll, Einwilligung und Datenschutzentscheidung vor jeder personenbezogenen Datenerhebung erforderlich; aktuell werden keine Kinderaufnahmen oder Telemetriedaten gesammelt.

## Dokumentationsregeln

- Ein aktueller Überblick, Anleitungen und begründete langfristige Referenzen im Git; **keine neuen Einzelberichte je Testlauf**.
- Neue Logs/JSONs nach `qa-results/` oder `build/`; CI-Artefakte werden nach sieben Tagen gelöscht. Dauerhafte Freigaben brauchen eine verifizierte versionierte Ablage mit Commit, Datum, Namen und Hashes.
- Historische Dateien erst nach geprüfter Ersatzablage entfernen. [Archiv und vollständiger Index](qa/README.md): 139 Originaldateien unverändert erreichbar; keine Veröffentlichung privater Grafiken oder Zugangsdaten.
- README, CI und Anleitungen müssen dieselben Testkommandos verwenden. `documentation.py` kontrolliert lokale Markdown-Ziele, Archivindex und CI-Dateireferenzen; externe HTTP-Erreichbarkeit wird getrennt ausgewiesen.
