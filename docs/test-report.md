# Tatsächliche Prüfungen Kinderwelt 0.7.1

Stand: 21. Oktober 2026. **6.083 Godot-Spiel-/Layoutprüfungen, 30 echte Audiomischer-Prüfungen, 36 Python-Tests und 343 Desktop-Renderings bestanden.** Alle 1.621 Sprachdateien und 20 Musikstücke wurden tatsächlich dekodiert.

Die neue deutsche Stimme und die Begrenzung langer Figuren-Schaltflächen sind in [speech-clarity-v071.md](speech-clarity-v071.md) beschrieben. Rohprotokolle liegen in [qa-evidence/v071/](qa-evidence/v071/); bisherige 0.7-Nachweise bleiben in `qa-evidence/v07/`.

Die unabhängige Rückerkennung umfasst 31 feste Stichproben je Sprache ohne Referenztext-Prompt. Bei 18 unveränderten deutschen Referenztexten sinkt die normalisierte Zeichenfehlerquote von 13,09 % auf 5,82 %. Das ist keine menschliche Hörabnahme. Insbesondere „Chemie“, einzelne zusammengesetzte Wörter und einige englische/russische Fachnamen bleiben bei der Rückerkennung auffällig. Rohtexte und Modellhashes bleiben sichtbar.

Android 0.7.1 / 8 wird als nächster Schritt aus einem sauberen Quellcommit gebaut. Artefakte und Prüfergebnisse werden nach tatsächlichem Export ergänzt.

Offen: echte Android-Geräteinstallation, Safe-Areas und Audiofokus, Verständlichkeit durch Muttersprachler und Kinder, fachliche/empirische Evaluation und Google-Play-Freigaben. Keine Lernwirkungs- oder Uploadbereitschaftsbehauptung.
