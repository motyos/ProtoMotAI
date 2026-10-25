# filename_templates - כל תבניות שמות הקבצים והתיקיות

מודול: filename_templates | פרויקט: protomotai | גרסה: 0.1 | סטטוס: טיוטה | מצב: דלוק | תלוי ב: settings | רמת סיכון: נמוכה | עודכן: 2026-10-23 | עודכן על ידי: claude

> כללים: אנגלית, אותיות קטנות, ascii (אותיות, ספרות, `_`, `-`, `.`). שינוי תבנית כאן משנה את כל הפרויקט; תבנית בעברית (אם נבחרה) מייצרת תוצר בעברית.
> סימונים: `<yyyymmdd>` תאריך, `<subject>` נושא באנגלית, `<key>` מפתח צעד, `<n>` מספר.

| סוג | תבנית | דוגמה |
|---|---|---|
| קובץ התקדמות של ריצה | `runs/run_<yyyymmdd>_<subject>.md` | `runs/run_20261023_setup.md` |
| יומן ריצה (אנגלית) | `runs/run_<yyyymmdd>_<subject>.log` | `runs/run_20261023_setup.log` |
| יומן כללי של הפרויקט (עברית) | `actions_log.md` | |
| רשומת החלטה | `decisions.md` (רשומות `d-<n>`) | `d-12` |
| שאלות פתוחות | `open_questions.md` (שורות `q-<n>`) | `q-3` |
| ממצא | בקובץ הריצה או `findings.md` (רשומות `f-<n>`) | `f-7` |
| רשימת משימות ו"הבא בתור" | `todo.md` | - |
| טיוטות לפי נושא (טבלת ניתוב ב-`topics.md`) | `draft/brainstorm/<subject>.md`, `draft/scenarios/<subject>.md` | - |
| סטטיסטיקות ריצות | `runs/metrics.md` (שורה לריצה) | - |
| יומן צ'אטים לפי נושא | `runs/sessions.md` (שורה לנושא) | - |
| כלי ברישום הכלים | `tools.md` (שורות `tool-<n>`) | `tool-3` |
| עמוד סקירה (מודול project_lifecycle) | `project/overview.md` | - |
| תרחיש קבלה (מודול project_lifecycle) | `project/scenarios.md` (רשומות `sc-<n>`) | `sc-4` |
| החלטה אוטומטית (מודול auto_decisions) | `auto_decisions.md` (רשומות `ad-<n>`) | `ad-3` |
| ראיות ריצה | `runs/evidence/<subject>/<file>.log` | |
| תדריך סוכן (מודול agents) | `wip/<stage>-logs/briefs/brief-<letter>.md` | |
| יומן סוכן גולמי | `wip/<stage>-logs/<worker-id>.log` | |
| קובץ צעד בתוכנית | `plan/<key>_plan_<subject>.md` | |
| tag לנקודת חזרה | `pre-<subject>-s<step>-<yyyymmdd>` | `pre-setup-s1-20261023` |
| ענף | `<type>/<subject>` | `feature/login` |
| תיקיית עבודה זמנית | `wip/<stage>-<worker>` | |
| קובץ הגדרות פרויקט | `project_settings.md` (תבנית T-pset) | - |
| תיאור כלי לייצור עצמי (בפרוטוקול) | `tools_build/ts-<n>_<subject>.md` (מזהה `ts-<n>`) | `ts-1_test_catalog.md` |
| תיאור כלי להתקנה (בפרוטוקול) | `tools_install/ti-<n>_<subject>.md` (מזהה `ti-<n>`) | `ti-1_php_container.md` |
| פרוטוקול אבטחה | `security/<subject>.md` | `security/downloads_installs.md` |
| כלים בפרויקט | `project_tools.md` (תבנית T-ptools) | - |
| מטמון פרוטוקול מרוחק | `runs/protocol_cache/<commit>/` (ב-`.gitignore`) | |
| נתיבים רגישים | `sensitive_paths.md` | |

## מזהים ופירושם
> מקור יחיד. נוצר ממנו `docs/reference/ids.md` (`tools/build_docs.py`). מזהה קבוע ולא ממוחזר; מזהה שבוטל נשאר ריק.
<!-- ids:begin -->
| מזהה | פירוש | איפה מוגדר | דוגמה |
|---|---|---|---|
| `d-<n>` | decision: החלטת בעלים | `decisions.md`, תבנית T-decision | `d-12` |
| `q-<n>` | question: שאלה פתוחה | `open_questions.md`, T-question | `q-3` |
| `f-<n>` | finding: ממצא | קובץ הריצה או `findings.md`, T-finding | `f-7` |
| `sc-<n>` | scenario: תרחיש קבלה | `project/scenarios.md`, T-scenario | `sc-4` |
| `sx-<yyyymmdd>-<name>` | security campaign: קמפיין בדיקות אבטחה (עבר מ-`sc-`) | `security/campaigns/`, T-campaign | `sx-20261023-auth` |
| `ad-<n>` | auto decision: החלטה אוטומטית | `auto_decisions.md`, T-ad (מודול auto_decisions) | `ad-3` |
| `R-<n>` | review finding: ממצא סקירה בלתי תלויה | דוח סקירה (T-brief-review) | `R-2` |
| `tool-<n>` | tool: כלי רשום ב-`tools.md` | `tools.md`, `project_tools.md` | `tool-3` |
| `ts-<n>` | tool spec (build): תיאור כלי לייצור עצמי | `tools_build/`, T-toolspec | `ts-2` |
| `ti-<n>` | tool install: תיאור כלי להתקנה | `tools_install/`, T-toolspec | `ti-1` |
| `<פרופיל>.<n>` | תרחיש מוכן מספריית פרופיל מקצועי | `modules/specialization/<פרופיל>/scenarios.md` | `secure_dev.1` |
| `T-<שם>` | template: תבנית | `templates/templates_registry.md` | `T-run` |
| `R0` / `R1` / `R2` | רמות סיכון: קריאה בהיקף / כתיבה בתיקיית הכתיבה / פעולה מסוכנת (אישור נפרד) | ליבה §2.4 | - |
| `E0` / `E1` / `E2` | exposure: רמות חשיפה לרשת (מודול auto_decisions) | `settings.md` | - |
| `M0`-`M6` | שלבי מיגרציה | `modules/general/migration/module.md` | `M2` |
| `G1`-`G15` | פריטי רשימת פערים במיגרציה | `modules/general/migration/gap_checklist.md` | `G9` |
| `PROTOMOTAI_V1` | גרסת הפרוטוקול (`protocol_version`) | `settings.md` | - |
<!-- ids:end -->

## שמות מזהים
- מזהה ריצה: `<yyyymmddhhmm>-<6 hex>`.
- מזהה סוכן: `worker-<letter>-<stage>`; מנהל: `manager-<stage>`.

## מיגרציה (רק כשהמודול דלוק)
- תיקיית סריקה (שכפול GitHub בלבד): `runs/scan_<yyyymmdd>_<subject>/src/` (ב-`.gitignore`)
- מסמכי מיגרציה: `runs/migration/{inventory,gaps,plan}.md`
- תג נקודת חזרה: `pre-migration-s<step>-<yyyymmdd>`
