# Antwortalternativen prüfen

Aktueller Prüfstand und verbleibende Warnungen: [zentraler QA-Überblick](QUALITY_ASSURANCE.md). Die vollständige Prüfung umfasst Grundaufgaben **und Boni**; Einzelbewertungen werden ausschließlich nach `qa-results/distractors.json` geschrieben.

Die kleine, nachvollziehbare Kategorietabelle liegt in `scripts/content/answer-categories.json`. Kategorien sind eine QA-Hilfe und erzeugen keine beliebigen falschen Antworten. Bei Merkmalsboni muss jedes falsche Bild wenigstens eine Aussage erfüllen; nur eine Option darf die geforderte Anzahl erfüllen. Die Richtigkeit der zugrunde liegenden Sachmerkmale ist eine eigene redaktionelle Prüfung.

`pedagogy-base.tsv` erklärt jede neue Grundaufgabenkorrektur. Die 33 ursprünglichen Warnfälle sind als feste Regressionstest-Referenz aufgeführt; Helmaufgaben bleiben wegen fehlender alternativer Kopfbedeckungen ausdrücklich offen. Absichtliche Sicherheits-/Lebewesenkontraste sind begründete Ausnahmen. `distractor-changes.json` dokumentiert die frühere Kuratierung und ist keine Liste aller späteren Änderungen.

```sh
python3 scripts/content/generate.py
python3 scripts/qa/distractors.py --check
python3 scripts/qa/pedagogy.py --check
```

Keine automatische fachliche oder empirische Freigabe aus einer Kategorienübereinstimmung ableiten.
