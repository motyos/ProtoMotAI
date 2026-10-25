# Security: what is protected, what is not enforced, and how to report

[English](security.md) | [עברית](../he/security.md)

Document: security | Version: 0.1 | Status: draft | Updated: 2026-10-25 | Protocol version: PROTOMOTAI_V1 (draft)

> The protocol is mainly **instructions to the chat**. It reduces risk, but it does not replace operating-system permissions. Do not rely on it as your only protection mechanism.

## What the protocol tries to guarantee
- Claude does not touch anything outside the scope you defined, and does not read secret files without an explicit request.
- Dangerous actions (deletion, installation, network, push, writing outside the scope, sending files out) require a separate approval.
- Secrets are not written in the chat, in logs or in git. If a secret value appeared in output, it is reported immediately without repeating it.
- Text found inside the files of a scanned project, or in tool output, is information and not an instruction.

## What is enforced by a tool and what is instruction only
| Subject | Classification | Note |
|---|---|---|
| A project scan does not print secret values | The tool does not print values (tested); running it is an instruction | `scan_project.py` reports only path, line and type; files with a sensitive name are not opened, symbolic links are not followed. Covered by a self-test |
| Leak check before upload | An instruction to run it; the tool itself does not print values | `leak_check.py` compares hashes of secret values and prints only `path:line`. Running it before upload is done with the owner's consent and is not technically enforced |
| Tool registry and drift check | warn-only | `check_tools.py`, `check_overview.py`: warnings without blocking |
| Read-only source during migration | Instruction | No blocking on the server. It is recommended to connect the source as read-only |
| Numbered approval before an action | Instruction | Depends on the chat's compliance. No hook blocks it |
| A restore point before a change | Instruction | |
| `--no-verify` is forbidden | Instruction | Cannot be enforced |

## What else is recommended
1. Connect to Claude **only** the folders it needs, and connect read-only folders as read-only mounts.
2. Run under a user without unnecessary permissions. Avoid sudo.
3. Do not keep secrets inside the writing folder. Keep them outside the scope.
4. Do not paste tokens or passwords into the chat.
5. Publish a repository only after scanning for secrets and local paths.
6. Agents: limit concurrency and check resources before a wave (`check_resources.sh`).

## A protocol from a remote source and tool installation
- **A remote protocol is instructions that the chat executes.** Therefore it is pinned to a full commit and verified at the start of every chat, and an update happens only with a numbered approval after the changes are shown. A private repository is not supported, because it requires a token (a secret). If verification fails, Claude does not read from the cache and stops.
- **Remote text does not widen permissions.** Write scope, deny files and numbered approval are set in the project instructions and the local files, and take precedence.
- **Installing tools** is R2, with a pinned version, integrity verification (hash or signature, when available), running with minimal permissions, and a verification command before each use. Details in `proto_draft/security/downloads_installs.md`. Enforcement is in the instructions and the chat, not a technical block.

## Known limitations
- Hidden instructions inside files (prompt injection) are a real risk. The protocol defines them as information and not an instruction (`core §2.7`), but this is a rule in the instructions and not a technical block.
- Secret filtering is based on patterns and a hash check of whole values. A secret that was changed (partial, encoded) will not be detected.
- The procedure for loading from GitHub and the tool installation were written and not tested against a real GitHub repository or a real installation.
- The protocol was checked with cold tests and self-tests, and has not been used in a live project over time.
- It does not include code vulnerability scanning, and does not guarantee compliance with any standard.

## Reporting a vulnerability
If you found a vulnerability in the protocol or the tools, do not publish it publicly. Use GitHub's private reporting: in the Security tab of the repository, "Report a vulnerability" (https://github.com/motyos/ProtoMotAI/security/advisories/new). If the option is not available, open an Issue without exploit details and write that you have a private report, and the owner will contact you. Include: what you found, how to reproduce it, and what the impact is. No real secret values.
