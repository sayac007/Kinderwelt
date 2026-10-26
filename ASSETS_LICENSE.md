# Kinderwelt asset licensing and source notices

The root [MIT LICENSE](LICENSE) covers the Kinderwelt software and its associated
documentation. It is **not a blanket licence for images, recordings, fonts,
models, datasets or other third-party material**. Their specific notices remain
applicable; the software licence does not replace them.

## Operator decision recorded on 2026-10-26

For project-created illustrations and generated speech recordings the operator
selected:

**Alle Rechte vorbehalten, soweit Schutzrechte bestehen.**

This reserves only rights that actually exist in the operator's own assets. It
is not a claim that every generated output is protected, nor a grant or override
of provider/model/reference-image or other third-party rights. The existing
software, music, font, model and dataset notices below remain applicable.
The same statement is recorded in `scripts/android/release-metadata.json`;
`KINDERWELT_ASSET_LICENSE` remains an explicit operator override. Recording the
statement is not automated legal clearance or Google Play approval.

| Material | Existing notice / evidence | Scope and remaining limits |
|---|---|---|
| Bundled generated artwork | [Character origins](docs/character-origins.md), [visual audit and C2PA limits](docs/qa/VISUAL_IP_AUDIT.md), `art/character-origins.json` | Generation lineage is evidence, not a copyright/trademark clearance or a licence grant. Family-derived illustrations stay private; neutral builds use the fictional cast. |
| German and Russian speech | [German model card](assets/voice/quest/de/MODEL_CARD.txt), [Russian model card](assets/voice/quest/ru/MODEL_CARD.txt), their adjacent Apache-2.0 `LICENSE.txt` files | Qwen model notices describe the model; no automatic Apache licence for generated recordings or separately unspecified datasets is inferred. The operator's own-recording policy is recorded above; upstream terms remain separate. |
| English speech | [English model card](assets/voice/quest/en/MODEL_CARD.txt), [upstream provenance notice](assets/voice/quest/en/LICENSE.txt) | The supplied LJSpeech card declares the **dataset** public domain. It does not supply a separate model-weight/output grant; those distribution terms still require operator review. |
| Music | [Per-track credits](assets/music/NOTICES.txt), `assets/music/manifest.json`, [music sources](docs/music.md) | Composition, score/arrangement and recorded rendering are distinct. Each CC-BY-SA-derived app recording is explicitly offered under the **same listed CC-BY-SA version** and URL. Other original source notices and SoundFont terms remain intact. |
| Nunito font | [SIL Open Font License](assets/quest/OFL.txt) | The font keeps its OFL notice; the software MIT licence does not relicense it. |

The unchanged [software MIT notice](assets/licenses/Kinderwelt-MIT.txt) is also
bundled; its bytes are checked against the root `LICENSE`.
All voice model cards/licence notices, the font notice and the music/source
licence texts are explicitly checked against both export filters and the bytes
actually packaged in APK/AAB, including Godot's install-time asset pack.

Device-local imported figures are user-supplied inputs, not bundled artwork or
assets licensed by this project. Their ownership is not inferred from import.
No licence is granted to other people's photographs or private family references.
This file records scope and unresolved decisions; it is not a legal opinion or
a declaration of Play upload readiness.
