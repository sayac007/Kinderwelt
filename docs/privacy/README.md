# Privacy text sources

The operator-supplied root `Datenschutzerklärung für die App.htm` is the German
master, dated 26 October 2026. The file remains byte-identical to the upload.
`datenschutz.de.md` is its readable text copy. EN/RU are translations of the same
facts and contact information prepared for operator review; no separate legal
approval or verification of the external email/Google practices is claimed.

`approved_privacy.py` generates the static site and `assets/privacy/policy.json`.
The latter is bundled and shown offline in the parents area, with plain text
references and no browser/network or photo access. Full paragraphs are checked;
no personal test photos are used. The static pages contain no scripts, external
fonts or images. This directory is prepared source content, not a published site.
The operator still chooses/enables hosting and supplies the public URL to Play.

```sh
python3 scripts/store/approved_privacy.py --check --output docs/privacy/site
# When the master/translation changes, intentionally regenerate and review:
python3 scripts/store/approved_privacy.py --write-app --output build/privacy-new
```

Copy the reviewed generated HTML pages into `docs/privacy/site/` after an intended
policy change. The check rejects stale site/app copies and unresolved fields.
The older generic privacy renderer remains a preview tool; the approved-source
export is the current publication handoff. [Release steps](../play/PUBLICATION.md).
