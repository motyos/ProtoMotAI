# ProtoMotAI

[English](README.en.md) | [עברית](README.md)

A generic protocol for working with Claude (claude.ai) when it is connected to your computer or server. It defines how Claude asks for approval before acting, how it handles secrets, how runs and decisions are documented, and how work resumes in an orderly way after a break, so that whoever opens a new chat does not start from a blank page.

Document: README | Version: 0.1 | Status: draft | Updated: 2026-10-25 | Protocol version: PROTOMOTAI_V1 (draft)

> **The protocol itself is written in Hebrew** (`proto_draft/`). This English documentation explains what it is and how to adopt it; the files Claude reads are in Hebrew. Claude works with them regardless of the language you talk to it in.

> **Status: draft.** The protocol was checked with "cold start" tests (a fresh agent reads only the entry point and answers questions) and with self-tests for the tools. It has not yet been used in a live project over time. What is enforced by tools and what is instruction only is detailed in [security](docs/en/security.md).

## Who it is for
- People who connect Claude to a server or computer and want clear boundaries: what it may read, what it may write, when it must ask.
- People working on a long project across several chats who want the state kept in files and not in the memory of one conversation.
- People who want to work in an orderly way without inventing procedures: developers, network administrators and IT administrators.

## How it works, in brief
1. Before every action Claude presents a **numbered list** and waits: "approve 1,3 / reject 2 / change 4". What is not approved is not done.
2. It writes **only** in the folder you define. Secret files are not opened and not printed.
3. Every run is documented in a progress file and a log, so a new chat can continue from there.
4. **Token and quota awareness:** the protocol tracks token usage per run, reminds you to report session usage, and adjusts parallelism and model choice so as not to exceed the quota, nor leave it unused.

## Five-minute start
See the [quickstart](docs/en/quickstart.md). In short: add one line to the project instructions, "read `<path>/index.md` and work according to it".

## Repository layout and who reads what
- `proto_draft/` (later `proto_approved/`): **the protocol itself**. Claude reads it, starting from `index.md`. Written in Hebrew.
- Inside the protocol: `profiles.md` (professional profiles), `core/remote_protocol.md` (protocol from a remote source and local project settings), `tools_build/` and `tools_install/` (tool catalogs), `security/` (security protocols).
- `docs/he/` and `docs/en/`: documentation for humans, in Hebrew and English. Claude does not need to read it. `docs/reference/` is generated from the protocol (Hebrew).
- `SECURITY.md`: how to report vulnerabilities. `.gitignore`: files that must not enter the repository.
- `LICENSE.md`, `LICENSE-CODE.md`, `NOTICE.md`, `CITATION.cff`: license and attribution in the root.

## Documentation
| Document | Contents |
|---|---|
| [docs/en/overview.md](docs/en/overview.md) | Short overview: what it is, what problem it solves, where the project stands |
| [docs/en/quickstart.md](docs/en/quickstart.md) | New project or moving an existing one, step by step |
| [docs/en/concepts.md](docs/en/concepts.md) | The concepts: approval, modules and toggles, runs, decisions, secrets |
| [docs/en/faq.md](docs/en/faq.md) | Frequently asked questions and problems |
| [docs/en/security.md](docs/en/security.md) | What is protected, what is not enforced, and how to report vulnerabilities |
| [docs/reference/](docs/reference/modules.md) | Modules, settings, templates, tools and identifiers (generated, Hebrew) |
| [docs/en/contributing_profiles.md](docs/en/contributing_profiles.md) | How to contribute a professional profile |

The entry point of the protocol itself, which Claude reads, is [proto_draft/index.md](proto_draft/index.md). **Claude does not need to read `docs/`.**

## License and attribution
- Documents and templates: Creative Commons Attribution 4.0 (CC BY 4.0). See [LICENSE.md](LICENSE.md). The official English license text: https://creativecommons.org/licenses/by/4.0/legalcode
- Scripts: MIT, see [LICENSE-CODE.md](LICENSE-CODE.md).
- Required attribution: "ProtoMotAI by osmoty, https://github.com/motyos/ProtoMotAI". See [NOTICE.en.md](NOTICE.en.md) and [CITATION.cff](CITATION.cff).

## Contributing and reporting
Suggestions and comments: [project Issues](https://github.com/motyos/ProtoMotAI/issues). To report a security vulnerability: [docs/en/security.md](docs/en/security.md).
