# Kinderwelt — Codex work package

Five YAML specifications for a reusable, offline-first, age-7 educational game platform built with Godot 4.x. The five learning domains are logic, mathematics, language, autonomy and social cooperation.

## Suggested execution

Give Codex the entire folder and ask it to execute `01_foundation.yaml` through `05_android_release.yaml` in dependency order, maintaining a working repository, committing after each accepted stage, running tests and reporting failures. Parallelize only independent work; integration and QA must follow the dependent stages. The 1–2 day duration is an ambition, not a promise.

**Suggested Codex instruction:**

> Treat the five YAML files as the implementation contract. Build a working Godot project, not a mockup. Execute in dependency order. Make reasonable decisions autonomously and document them. Use existing test tooling when applicable. Run and record actual test results. Do not invent benchmarks, signing credentials, audio assets, device tests, or publication status. If Android export/signing is unavailable, deliver the reproducible build scripts, all available artifacts, and a precise blocker report. Prioritize a genuinely playable, readable-free child experience over breadth of placeholder features. Keep all work in version control and provide a final acceptance matrix.

## Important

Google Play publication requires a developer account, valid app ID, signing, policy declarations and assets. No credentials are included. A signed `.aab` is not guaranteed without the necessary environment and signing material.
