# Frequently asked questions and problems

[English](faq.md) | [עברית](../he/faq.md)

Document: faq | Version: 0.1 | Status: draft | Updated: 2026-10-25 | Protocol version: PROTOMOTAI_V1 (draft)

## Questions
**Why approve by numbers?** So that an approval is precise and documented: a number that was not mentioned is not approved, and there is no "do whatever seems right to you". You can approve some items, reject some and change one.

**Can I approve everything at once?** A blanket approval is possible, but it is valid only up to the stage or time stated, and only for that run. R2 actions require a separate approval in any case.

**What if I do not have git?** git is recommended, but it is possible without it (details in [core §12.14](../../proto_draft/core/protocol_core.md)). Before every change the chat copies the files that are about to change to `runs/restore/<date_time>_<subject>/` and records a `manifest.txt` of `sha256sum`. After a break it compares the step table and the log against the files and checks for drift against the manifest, and restoring is done by copying back with a numbered approval. If even a copy-based restore point is not possible (no space or permission) it stops and asks. See `core §12.14`.

**Can I work without a server, just sending files to the chat?** Yes, in `upload` mode: you upload stable pages to the AI's memory. A chat that is not linked does not know the project state and notes that the information is a snapshot and not a source of truth.

**How much does it cost in tokens?** It depends. The protocol records a metrics line for each run, and agent tokens only as reported. There is currently no documented measurement of a typical cost; measure in your own project and record it in `runs/`.

**Who decides when in doubt?** The owner. When knowledge is missing, Claude asks and does not invent.

**Why does Claude ask at the start of every chat what topic we are working on?** Because it does not see the chat's name and does not remember previous chats. The answer determines which file to document in (brainstorming, decisions, open questions, runs), and a line in `runs/sessions.md` helps continue in a new chat. For a free conversation you say "chat" and nothing is documented. To turn it off: `session_start_question` in `settings.md`.

**Can I turn on only some of the modules?** Yes. You turn them on in the toggle table in `settings.md`. A child module is active only if its parent is on.

**Can the protocol live on GitHub while my settings stay with me?** Yes, that is the plan. In the project instructions you write `github:<owner>/<repo>@<commit>` (a public repository, a full commit). The protocol is read into a cache folder and stays read-only, and the settings (`project_settings.md`) and files stay in your writing folder. Updating to a new version is always with approval, after the changes are shown. The procedure was written but has not yet been tested against a real GitHub repository.

**How does Claude install a tool, and what stops it from installing something that changed?** Every installation is a dangerous action (R2) approved for the exact action, with a pinned version (digest or hash) and a verification command. Before each use it runs the verification command, and if the version does not match it does not use the tool. The responsibility to check that the source is trustworthy remains yours.

**What is the difference between `tools_build` and `tools_install`?** `tools_build` is a description of a tool that you will build yourself (why it is needed, what it does, what is required), without code. `tools_install` is an existing tool that you install, with a pinned version and a security protocol.

**How does a new idea turn into tests at the end of development?** In brainstorming, candidate scenarios are recorded. When a topic is decided, every must-have requirement gets a scenario `sc-<n>` with an expected result and a way to test it, and a row in a traceability table. Before the gate, the blocking scenarios are run and the proof and the commit that was tested are recorded.

**What is a professional profile, and is Claude really certified?** No. A profile is a module that directs Claude to the approach and checks of a field (for example, secure development), and it carries no official certification or compliance confirmation. It is off by default for projects that do not need it, and can be turned on for only one project.

**Where are the identifier abbreviations decoded (d-, q-, sc-...)?** In [reference/ids.md](../reference/ids.md) (Hebrew).

**What are the git rules in a project?** One repository per project, a local identity, commit messages in English, and no remote, push, `--no-verify` or `reset --hard` without approval. In a connected folder without delete permission, `.lock` files remain, and they are moved to `.git/stale_locks` instead of being deleted. See [git_ops](../../proto_draft/modules/general/git_ops.md).

## Problems
**git prints "unable to unlink ... tmp_obj ... Operation not permitted".** When the chat has no delete permission in the connected folder, git cannot delete temporary files. This does not harm the data. If a `.lock` file remains, do not delete a file that an active git process holds. You can move an old lock file to another name under `.git`.

**Can the chat delete files?** Deletion is an R2 action: a separate approval for each deletion, and also a technical permission in the connected folder. How to grant the permission depends on the application that connects Claude to the computer and is not documented here. Without permission, the chat moves files to a `_to_delete/` folder and the deletion stays in your hands.

**The chat says there is an active run from another chat.** There is a lock file. A lock older than the threshold in the settings (`stale_lock_hours`) is considered stuck, but it is taken over only with your explicit approval.

**The "cold start" test failed.** It checks that an agent that reads only the entry point can answer questions. The failure indicates what is missing or contradictory; fix the file and run again.

**The chat refuses to read a file.** The file is probably not in the scope list or is in the deny policy. To read a deny file, write in one message: the exact path, the purpose, and "approve reading".

**A tool showed WARN.** The check tools are warn-only. The warning states what does not match (for example an unregistered tool, a broken link or a stale overview page), and how to fix it.

**An agent did not report tokens.** "Not reported" is recorded. Do not guess. An agent that was restarted may show a cumulative number.
