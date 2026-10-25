# Contributing a professional profile

[English](contributing_profiles.md) | [עברית](../he/contributing_profiles.md)

A professional profile directs Claude to look at the working context from a particular angle: a role (for example, a senior developer), a standard or regulation, or a technology. It is turned on and off like any module. **It is not an official certification and not a confirmation of compliance with a standard, and it does not replace a professional.** This document explains how to add a profile to the repository.

## What a profile includes
A folder `proto_draft/modules/specialization/<key>/` (the key is in English, lower case):
- `module.md`: the module header, role and behavior, checklists, and stop rules. It ends with a `## מניפסט` (manifest) section following the `T-pmanifest` template (fields: key, name, type, domains, version, maturity, role, authors, license, sources, what it is not).
- `scenarios.md` (optional): ready acceptance scenarios, in the `T-scenario` template, with an id `<key>.<n>`. In a project they are copied as the project's own scenarios.
- A row in the toggle table (`settings.md`) and in the table in `profiles.md`.

## Rules
1. **Only tighten.** A profile cannot relax the core's numbered approval, secret handling, write scope or risk levels.
2. **No running code.** A tool is registered separately according to `tools.md` or `core/tools_install.md`.
3. **No secrets and no personal data** in any file.
4. **Sources.** Every professional claim rests on a source that can be checked (a standard, an official document), with a link. No source means writing "none" with a reason, and not inventing.
5. **No certification claims.** The "what it is not" field must say that this is not an official certification.
6. **License:** CC BY 4.0, like the other documents.

## Maturity
`draft` (written, not tested, loaded only with explicit approval) -> `reviewed` (passed a review and a "cold start" round, and the "verified in" field points to it) -> `approved` (approved by the owner).

## Checks before submitting
```
python3 proto_draft/tools/check_manifest.py
python3 proto_draft/tools/sync_settings.py --check
python3 proto_draft/tools/build_docs.py --check
python3 proto_draft/tools/check_links.py .
```
All of them warn only, but a contribution that leaves warnings should explain them.

## Trust
A contribution is text that Claude executes, so it goes through a human review before `reviewed`. A remote profile is pinned to a full commit, like the protocol. Details: `proto_draft/profiles.md` and `proto_draft/core/remote_protocol.md`.
