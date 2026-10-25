# Quickstart

[English](quickstart.md) | [עברית](../he/quickstart.md)

Document: quickstart | Version: 0.1 | Status: draft | Updated: 2026-10-25 | Protocol version: PROTOMOTAI_V1 (draft)

> The protocol files that Claude reads are written in Hebrew. Where this document quotes Hebrew keywords (such as the toggle values `דלוק` = on and `כבוי` = off), the meaning is given next to them.

## What you need
- Claude connected to your computer or server, with access only to the folders you chose. It is best to connect only the folders that are required, and to connect read-only folders as read-only.
- The protocol folder on the same computer, that is, this repository. The full path to it is called `protocol_path`.
- (Recommended) git in the project folder. Without git there is an alternative procedure of copying before a change: see the [FAQ](faq.md).

## Terms that appear below
- **Cold-start test:** a fresh agent with no context reads only the entry point and answers questions. If it fails, the documents are missing something or contradict each other.
- **R0 / R1 / R2:** risk levels. R0 is reading, R1 is writing within the approved scope, R2 is a dangerous action (deletion, installation, network, publishing) that needs a separate approval for each action.
- **takeover:** taking over a stuck run lock from another chat; only with explicit approval.
- **deny / mask:** a file in deny is not opened without an explicit request; a file in mask is read only through a masking command that replaces sensitive values with `****` before the output reaches the chat.

## What `protocol_path` is and how to find it
It is the full path, on the computer or server, to the protocol folder. If you cloned the repository, for example to `/home/me/protomotai`, then while the protocol is a draft the path is `/home/me/protomotai/proto_draft`. Inside that folder the command `pwd` prints it. Once the protocol is approved the path will be `.../proto_approved`.

## Two things called "project instructions"
- **The project instructions in the chat** (a setting in a claude.ai Project or in your own project): this is where the reference line to the protocol goes. This is what you write.
- **`instructions/project_instructions.md`**: a file that Claude creates in the writing folder in the first step, from a template. It contains the same reference line and the project details, so that the state is kept in a file.

## Remote protocol (GitHub) and local settings
Instead of a local copy you can read the protocol directly from a public repository on GitHub, **read-only and pinned to a full commit** (40 characters, not a tag and not a branch). In the project instructions you write: `read github:<owner>/<repo>@<commit> and work according to it.` Claude asks for a numbered approval, pulls the commit into a cache folder inside the writing folder (`runs/protocol_cache/`), and verifies that the loaded commit equals the recorded one. If not, it stops. The project's settings and files (`project_settings.md`, `project_tools.md`, runs) stay local. This procedure has not yet been tested against a real GitHub repository. Details: `proto_draft/core/remote_protocol.md`.

## How to turn a module on
The file `settings.md` in the protocol folder contains a table of default toggles. If the protocol is remote or you do not want to edit it, record your overrides in `project_settings.md` in the project's writing folder (one row per module: `| key | state |`), and `sync_settings.py --summary --project-settings project_settings.md` shows the effective state without changing the protocol. Otherwise, in the `settings.md` table of your local copy, change the module's row from `כבוי` (off) to `דלוק` (on), and tell Claude "update according to the settings". It runs a tool that updates the header line in each module file (after a numbered approval). A child module is active only if its parent is on.

## Option A: a new project
Open a new chat with the connected Claude, and write **one line** in the project instructions:

```
Read <protocol_path>/index.md and work according to it.
```

(While the protocol is a draft, `<protocol_path>` points to the `proto_draft` folder. You can write the line in any language.)

From here Claude opens with four steps, and in each step presents a numbered list and waits for your approval:
1. **Project instructions** (`instructions/project_instructions.md`): the project name, the writing folder, read-only folders, the protocol version.
2. **Scope file**: where it may write, what it may only read, what is forbidden.
3. **Sensitive paths list** (`sensitive_paths.md`): secret files and what to do with each one.
4. **First run**: a progress file and a log, and work continues from there.

What is not in the scope list is forbidden even to read. If Claude does not know something, it asks and does not invent.

## Option B: moving from an existing project (migration)
Turn on the `migration` module (off by default) and say in the chat, for example: "Move to working according to PROTOMOTAI_V1", with a path on the server or a public GitHub link (a private repository is not supported yet).
Claude scans the project **read-only** and runs no code in it, produces a gap report against the protocol and a numbered plan, and only after your approval creates files. By default the output goes to a separate folder, and writing into the source repository requires a separate approval.

## What an approval looks like
Claude writes:

```
1. Create instructions/project_instructions.md
2. Create scope.md
3. Run tools/check_template.py on both
```

And you answer, for example: `approve 1,2 / reject 3` or `change 3: ...`. (The protocol's own keywords are the Hebrew `אשר` = approve, `דחה` = reject, `שנה` = change; Claude understands the English words too.) A number that was not mentioned counts as not approved. An approval applies only to what was presented.

## Resuming after a break
In a new chat Claude reads the latest progress file and the end of its log, compares them with git (without git: against the `manifest.txt` of the restore point), and continues from the first step that was not completed. It continues an interrupted run only on your explicit instruction.

## What next
- [concepts](concepts.md): the full explanation of the concepts.
- [faq](faq.md): common questions and problems.
- [security](security.md): what the protocol protects and what it does not.
- [reference](../reference/modules.md): all modules, settings, templates and tools (Hebrew, generated).
