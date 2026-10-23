# Kinderwelt 0.9.0: Punkte, Bonusaufgaben und native Lerninhalte

Stand: 23.10.2026 (Europe/Berlin). Technische Prüfungen und offene Hör-/Geräteprüfungen sind getrennt zu lesen. Keine Aussage über nachgewiesene Lernwirkung oder Google-Play-Freigabe.

## Verhalten

- Die 320 Stationen behalten ihre Plätze, aber alle Fragen wurden für eine neue, anspruchsvollere Runde ersetzt. Die drei Sprachfassungen werden gegen die tatsächlich zuvor ausgelieferten Fragen geprüft; keine der 960 Grundfragen-Sprachfassungen bleibt unverändert. Mathe reicht mit mehreren Schritten über den Zehner hinaus, Sprachaufgaben verwenden neue native Wörter mit zwei Buchstabenlücken, Logik kombiniert Regeln. 200 neu geschriebene Sachfragen fordern Kontext, Ursache, Abgrenzung oder Reihenfolge. Die beabsichtigte höhere Schwierigkeit ist noch nicht mit Kindern empirisch geprüft. Jede hat zwei freiwillige Bonusaufgaben mit 50 und 100 Punkten; die Grundaufgabe gibt 10 Punkte. Beide Boni sind unabhängig wählbar und ohne Abzug überspringbar. Fehler kosten keine Punkte. Bereits gelöste Aufgaben geben beim Wiederholen keine zusätzlichen Punkte.
- In der neuen Runde maximal 960 belohnte Aufgaben / 51.200 Punkte. Bis zu 3200 bereits verdiente Punkte der früheren Runde bleiben separat erhalten: insgesamt maximal 54.400. Der Spielstand enthält stabile Aufgaben-IDs und den daraus geprüften Gesamtwert. Unbekannte IDs, falsche Typen und erfundene Summen werden verworfen. Frühere lokale Grundaufgaben werden mit zehn Punkten ins Archiv übernommen. Ihre Stationen sind in der neuen Runde wieder ungelöst und erneut belohnbar. Das Archiv wird beim nächsten Start nicht nochmals gutgeschrieben. Nach jeder richtigen Lösung wird gespeichert; ein neuer App-Prozess zeigt den Gesamtwert direkt im Kopfbereich.
- Bei Wechsel vom alten Android-Testpaket kann eine begleitende erwachsene Person im Elternbereich bestätigen, dass die erste Runde vollständig gelöst war, und die früher verdienten 3200 Punkte einmalig übernehmen. Das ist eine ausdrückliche manuelle Übernahme, kein automatisch nachgewiesener Zugriff auf den Spielstand der anderen App; vorhandene Archivpunkte werden nicht doppelt gezählt.
- Lokale Daten bleiben im jeweiligen App-Paket; Zurücksetzen löscht auch Punkte. Neue Paketinstallationen oder Deinstallation können keine Daten einer anderen App übernehmen. Besonderheiten des Wechsels von 0.8.1 und des Entwicklungsschlüssels: [Android](android.md).
- Deutsch vermittelt deutsche, English englische und Русский russische Lernwörter und Buchstaben. Russische Menüs, Figuren-/Musiknamen und Aufgaben verwenden kyrillische Wörter. Die internen Fach- und Speicher-IDs bleiben stabil. Keine deutsche Folgeaufnahme in englischen/russischen Sprachaufgaben.
- Zwei Rechenschritte und fehlende Zahlen, wechselnde Zahlenregeln, zwei gleichzeitig geltende Bild-/Zahlenregeln und zusammengesetzte Reihenfolgehinweise sowie zwei fehlende Buchstaben (Boni drei oder vier) bilden zusätzliche Herausforderungen. Die neue Sprachrunde übt die Rekonstruktion geschriebener Wörter; sie bewertet keine uneindeutigen englischen Silbenvarianten.
- 200 Sachaufgaben zeigen indirekte, prozedural gezeichnete Kontexte statt einer Kopie des Lösungsbilds. Beispiel: Musikanlage und „Hören. Die Augen sind zu, trotzdem erkennst du ein Lied. Was empfängt seinen Schall?“ Die Station zeigt ein Fragezeichen. Die Auswahlbilder bleiben als Antwortmöglichkeiten bestehen.
- Sach-Boni nutzen andere Antworten als die zugehörige Grundaufgabe und der jeweils andere Bonus. Die Texte fragen nach Beziehungen, Ursachen oder Übertragung auf eine andere Situation. Redaktionelle Konzeptfragen werden an mehreren Stationen wiederverwendet; 640 Bonusplätze sind nicht 640 vollständig unterschiedliche redaktionelle Fragen. Die tatsächliche Schwierigkeit muss mit Kindern geprüft werden.

## Stimme: ehrlich offener Teilauftrag

Die unveränderte synthetische englische LJSpeech-Stimme bleibt weiblich. Deutsch (Thorsten) und Russisch (Denis) bleiben vorerst die klareren nativen Stimmen. Die gewünschte identische weibliche Stimmfarbe für alle drei Sprachen ist **nicht erreicht**.

Die getestete OpenVoice-V2-Umwandlung der nativen Sprachaufnahmen zur synthetischen englischen Referenz verschlechterte bei einem festen Vergleich aus sieben bestehenden 0.8.1-Clips je Sprache die unabhängige ASR-Zeichenfehlerrate: Deutsch 3,463 % → 16,450 %, Russisch 3,756 % → 15,493 %. Akustische Anpassungen von Tonhöhe und Spektrum brachten keine verlässliche deutsche Verbesserung. Diese Versuche wurden nicht ausgeliefert. Die [Messdaten](qa/voice-v090-experiments.json) dokumentieren Referenztexte, Erkennung und Datei-Hashes. Schauspieleraufnahmen wurden nicht zur Stimmenkopie verwendet. Vor einer weiteren Umstellung sind ein verständlicher multilingualer Kandidat und Hörprüfungen nötig.

Die neuen Inhalte haben pro Sprache 1947 Clip-Zuordnungen einschließlich Hinweisen und Bonusfragen. Gleiche Texte teilen Audiodateien. Die Pipeline behält alle erzeugten Sätze, Ruhe am Anfang/Ende und gemessene phonetische Dauern. Fehlende Audioinhalte, beschädigte Dateien, falsche Hashes, Übersteuerung und unerwartete Schnitte werden technisch geprüft. Das beweist keine vollständige Verständlichkeit.

## Reproduzieren

```sh
python3 scripts/content/generate.py
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 bash tests/run.sh
GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 xvfb-run -a bash tests/qa/quest-render.sh qa-results/visual-neu
python3 scripts/android/build_variants.py --tools /workspace/tools --output build/android-neu
python3 scripts/qa/listening_pack.py --output qa-results/listening.html
```

Die Tests starten für den Neustartnachweis tatsächlich zwei getrennte Godot-Prozesse. Der grafische Test verwendet echtes OpenGL-Rendering und prüft unter anderem identische Rätselpixel beim Austausch des alten Lösungsobjekts. Die 461 Bildschirmaufnahmen decken vier Displayprofile, drei Sprachen, kombinierte Bild-Zahlen-Muster, Reihenfolgen, die manuelle Punkteübernahme, Bonusauswahl, beide Bonusstufen und den Maximalpunktestand einschließlich erster Runde ab. Eine strukturell vollständige Bildsammlung ersetzt keine manuelle Betrachtung aller Zustände.

Tatsächliche Endergebnisse und Artefakte: [Testbericht](test-report.md).

## Offene Freigaben

- Hörprüfung DE/EN/RU ohne Text, dann mit Musik im Spiel; Wortanfänge/-enden, Buchstaben, Silben und Bonusfragen. Gemeinsame weibliche Stimmidentität bleibt offen.
- Muttersprachliche und fachliche Prüfung aller neuen Inhalte, Eindeutigkeit der Antwortbilder und Verständnis der Kontextzeichnungen. Die bisherige Ablenkerheuristik markiert weiterhin 33 Grundaufgaben; das ist keine automatische fachliche Widerlegung oder Freigabe.
- Geräteprüfung: Neustart und Android-Prozessbeendigung, Rotation, kleine Bildschirme, Touchflächen, Bluetooth/Unterbrechungen und Aktualisierung mit demselben Entwicklungsschlüssel. Keine echte Android-Geräteprüfung in dieser Cloud behauptet.
- Praktische Evaluation mit Kindern und freiwillig begleitenden Erwachsenen nach bestehenden Protokollen; keine personenbezogenen Daten neu erfasst.
- Endgültige Paketkennung, Release-Signierung und Google-Play-Anforderungen bleiben offen.
