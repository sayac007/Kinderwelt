# Kinderwelt asset licensing and source notices

The root [MIT LICENSE](LICENSE) covers the Kinderwelt software and its associated
documentation. It is **not a blanket licence for images, recordings, fonts,
models, datasets or other third-party material**. Their specific notices remain
applicable; the software licence does not replace them.

## Operator decision still required

Licence for project-created illustrations and generated speech recordings:

**`{{ASSET_LIZENZ_DES_BETREIBERS}}`**

No licence for those assets is selected by this change. The operator must check
the relevant provider, model, reference-image and distribution terms and supply
the applicable statement before distribution. The release builder already
rejects an unset corresponding asset-licence field in
`scripts/android/release-metadata.json` (or its documented
`KINDERWELT_ASSET_LICENSE` override). Supplying that field is an operator decision,
not an automated legal approval; this template must also be completed for release.
It must not override the existing third-party notices below.

| Material | Existing notice / evidence | Scope and remaining limits |
|---|---|---|
| Bundled generated artwork | [Character origins](docs/character-origins.md), [visual audit and C2PA limits](docs/qa/VISUAL_IP_AUDIT.md), `art/character-origins.json` | Generation lineage is evidence, not a copyright/trademark clearance or a licence grant. Family-derived illustrations stay private; neutral builds use the fictional cast. |
| German and Russian speech | [German model card](assets/voice/quest/de/MODEL_CARD.txt), [Russian model card](assets/voice/quest/ru/MODEL_CARD.txt), their adjacent Apache-2.0 `LICENSE.txt` files | Qwen model notices describe the model; no automatic Apache licence for generated recordings or separately unspecified datasets is inferred. The operator's recording licence remains pending above. |
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
