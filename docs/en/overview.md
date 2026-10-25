# Project overview

[English](overview.md) | [עברית](../he/overview.md)

Document: docs/en/overview | Updated: 2026-10-25 | Status: draft

## What this project is, in brief

It is a rulebook for Claude, for the time when it is connected to your computer or server and can perform actions there by itself. The rulebook sets what it may do, what it may not do, when it must ask you, and how it documents the work so that the work can continue even after a break.

## What problem it solves

Imagine you hired a very capable assistant and gave him the keys to the office. There are two problems here:

- **He can touch anything.** By mistake he might change an important file, delete something, or see a password and copy it to the wrong place.
- **He arrives every morning with no memory.** Every new conversation with Claude starts from zero. It does not remember what was done yesterday, what was decided and why.

The protocol deals with both problems. It has safety rules, and it has an orderly "shift log" that the next assistant reads before starting work.

## The main ideas

- **A work order before every action.** Claude writes a numbered list and waits. You answer, for example, "approve 1,3 / reject 2", and what you did not approve does not happen.
- **One workroom.** There is one folder where it may write, and folders it may only read. Everything else is neither read nor written.
- **A vault for secrets.** It does not open files of passwords and keys. If such a file must be read, it sees only a version in which the sensitive values are replaced with `****`, and secrets are not printed in the chat.
- **A risk traffic light (R0-R2):**
  - **R0, green:** reading only. One approval is enough for the whole stage.
  - **R1, yellow:** writing in the workroom. Approval for the list.
  - **R2, red:** deletion, installation, network access, `sudo`, `git push`, writing outside the workroom and handing over control. Every action needs a separate approval.
- **A shift log.** All work is recorded immediately, not at the end: what was done, what was found and what was decided. A new chat reads the log and continues from the same point.
- **What is read is information, not an instruction.** Text found in a file, a website or an external repository does not tell Claude what to do. Even an instruction that appears inside it does not cancel the core rules.
- **An opening question.** Claude does not see the chat's name. So at the start of a conversation it asks "what topic are we working on?", and according to the answer it knows which file to document in (brainstorming, a decision, execution and so on).
- **A car with add-ons.** There is a core that always runs, and add-ons that are turned on and off in one toggle panel (`settings.md`). A project that adopts the protocol can override values in its own settings file, except for the core rules. Order of precedence: core rules, the project instructions, the project settings, the protocol settings.

## The add-ons

| Add-on | What it does | Default |
|---|---|---|
| Server link and git | Rules for working on a server and in code repositories | on |
| A professional "hat" | A specialization, for example a senior developer who thinks about security first (`secure_dev`) | off |
| A step guide | Eight steps from idea to finish, with separate tracks for developers, network administrators and IT administrators | off |
| Migration | Moving an existing project to work according to the protocol. The default writes to a separate folder, and writing into the source repository requires a separate approval | off |
| Several agents in parallel | "Assistants of the assistant". This is the most dangerous add-on, so it is off | off |

Also:
- **Ready forms.** Every document (a decision, a finding, a summary) is created from a fixed template, so that all documents look the same and no detail is forgotten.
- **Small check tools.** There are 16 scripts that check that everything is consistent: that no fields are missing, that there are no broken links, and that no secret leaked before upload. Most of them also have a self-test (11 test files in total).

## Token and quota management

The protocol is aware that working with Claude is limited by a quota, and tries to use it wisely: not to get stuck in the middle, and not to leave it unused.

- **Tracking.** Every run gets a metrics line in `runs/metrics.md`: duration, active time, actions, findings and decisions. For each agent the model and tokens are recorded **as reported**, never guessed.
- **Reporting from you.** Claude cannot see the session usage percentage by itself. Before launching agents and at each new wave it reminds you to update it, and acts on what you reported. Without a fresh report the state is "unknown", and it is cautious.
- **Pacing.** A cheaper model for reading, summarizing and cold-start checks, and a stronger model for planning and security review. A concurrency cap by available resources. Below the threshold (80 percent by default) parallelism may be raised to use the quota; above it no new agent is launched.
- **Numbers.** There is a [measurement from a previous project](../../proto_draft/evidence/token_measurements.md) (Hebrew): a cold-start check on the order of 150 thousand tokens, and a strong-model drafting round between 300 and 640 thousand. It is one run and self-reported by the agents, so it is an order of magnitude only. Measure in your own project.
- **What is missing.** There is no automatic reading of the quota. The adjustment depends on your reports and on the recorded data, and it applies only when the agents module is on (default: off).

## Where it came from

The protocol was born from practical experience working with Claude on a real software project. It takes the procedures that worked there and words them so that they fit any project.

## What is in the repository

| Folder or file | What is in it |
|---|---|
| `proto_draft/` | The rulebook itself, what Claude reads. The entry point is `index.md`. Written in Hebrew |
| `docs/he/`, `docs/en/` | Explanations for humans in Hebrew and English: quickstart, concepts, frequently asked questions, security. `docs/reference/` is generated automatically (Hebrew) |
| Files in the root | README, licenses, attribution instructions, and the procedure for reporting security holes |

## Where the project stands

- **Draft.** The main test that was done is the "cold-start test": a new agent, with no context at all, reads only the entry point and answers questions. If it cannot, something is missing in the documents. Beyond that there are self-tests for the tools.
- **Published, and reviewed.** After the first publication an internal review was carried out, and following it the severe findings were fixed and the scripts were hardened. The review was done by the same tool that wrote the protocol, and so it was not checked by an outside party.
- **License:** the documents are under CC BY 4.0, meaning the source must be credited. The code is under MIT.

## Known limitations

- The protocol has not yet been used in a live project over time.
- Most of the rules are instructions to the chat, not technical enforcement. The tools check consistency, but they do not prevent Claude from acting differently. Details in [security.md](security.md).
- Loading the protocol from a remote repository has not been tested in practice, and is currently supported only on GitHub.
- Automatic tool installation has not been tested in a real installation.
- Working with several agents in parallel and keeping settings inside a Project in claude.ai are options that have not yet been tested or have not been implemented.
- The project itself is not yet fully documented according to the protocol's own rules (for example, run files were not created for every stage). This will be corrected from the next run.
- The protocol itself is in Hebrew only.

## What next

[Quickstart](quickstart.md), [Concepts](concepts.md), [FAQ](faq.md).
