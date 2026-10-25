# הגדרות

> **נוצר אוטומטית. לא לערוך ידנית.** מקורות: `settings.md`. הפקה מחדש: `python3 tools/build_docs.py`; בדיקה: `--check`. גרסת פרוטוקול: PROTOMOTAI_V1 (גרסת הפרוטוקול הנוכחית; פרויקט שמאמץ רושם אותה בהוראותיו).

## שפה ורישום

| הגדרה | ערך |
|---|---|
| dialog_language | עברית | שיחה עם המשתמש |
| file_and_folder_names | אנגלית, אותיות קטנות, ascii | קבצים, תיקיות, tags, ענפים |
| general_log_language | עברית | היומן הכללי של הפרויקט (actions_log) |
| run_log_language | אנגלית | פלט שוטף של קבצי הרצה (`.log`) |
| git_messages_language | אנגלית | הודעות commit |
| templates_language | he | תבנית בעברית מייצרת תוצר בעברית; תבניות נוספות בתיקיית השפה המקבילה; הגדרת התבניות ב-`templates/templates_registry.md` |
| source_code_and_comments | אנגלית |  |

## אישורים

| הגדרה | ערך |
|---|---|
| approval_style | רשימה ממוספרת לפני כל פעולה; "אשר 1,3 / דחה 2 / שנה 4: ..."; מספר שלא הוזכר = לא מאושר |
| default_mode | מחנים ושואלים (ללא החלטות אוטומטיות) |
| read_scope_approval | אישור אחד לשלב קריאה (לא לכל קובץ) |
| write_scope | רק תיקיות כתיבה שהוכרזו בפרויקט |

## ערכי סף

| הגדרה | ערך |
|---|---|
| protocol_path | נתיב מלא לתיקיית הפרוטוקול בשרת (למשל `/home/<user>/projects/protomotai/proto_draft`; אחרי אישור `.../proto_approved`). נכתב פעם אחת בהוראות הפרויקט המאמץ |
| restore_point_validity_days | 7 (נקודת חזרה ישנה מזה נבדקת מחדש לפני שמסתמכים עליה) |
| blanket_approval | אישור גורף תקף רק עד השלב או הזמן שנאמרו, ורק לאותה ריצה |
| repeated_failure_stop | 3 כישלונות חוזרים באותה פעולה = עוצרים ושואלים |
| repeated_failure_warn | 2 כישלונות חוזרים = אזהרה ובדיקת גישה אחרת; 3 = עצירה (`repeated_failure_stop`) |
| security_test_ttl_days | לפי קטלוג הבדיקות של הפרויקט (עמודת TTL) |

## ערכי סף של מודול הסוכנים (נקראים רק כשהמודול דלוק)

| הגדרה | ערך |
|---|---|
| stale_lock_hours | 3 (נעילה ישנה מזה = שואלים לפני takeover) |
| heartbeat_minutes | 15 (שורת יומן בפעולה ארוכה) |
| disk_stop_percent | 80 (דיסק מעל זה = עצירה) |
| session_usage_cap_percent | 80 (לפי דיווח הבעלים; מעל זה מקטינים מקביליות, מתחת מותר להגדיל עד התקרה) |
| agents_concurrency_cap | לפי משאבים באותו רגע; ברירת מחדל 5 |
| cold_start_checks_per_run | 3 (תקציב בדיקות קרות לריצה) |
| consultations_per_run | 2 (רק כש-consultation_panel דלוק) |
| profiles_active_warn | 3 (יותר מזה פרופילים מקצועיים פעילים = אזהרה; כל פרופיל מוסיף קריאה להקשר) |
| critical_cost_threshold | יותר מ-5 קבצים או יותר מ-2 שעות תיקון = קריטי |
| calibration_min_runs | 3 (כיול הערכות רק מ-3 ריצות עם הערכה ויחס; פחות = "אין מספיק נתונים") |
| idle_gap_minutes | 30 (פער בין שתי שורות יומן מעל זה נחשב המתנה ולא זמן פעיל) |
| overview_stale_days | 3 (עמוד סקירה ישן מהריצה האחרונה ביותר מזה = אזהרה; project_lifecycle בלבד) |
| periodic_review_every | כל 10 החלטות אוטומטיות או בסוף ריצה, המוקדם מביניהם (auto_decisions בלבד) |
| panel_decision_rule | 2 מתוך 3 יועצים; בתיקו שואלים את הבעלים (consultation_panel בלבד) |
| exposure_levels | E0 אין חשיפה / E1 מתוכננת ומאושרת / E2 אחר = עוצרים (auto_decisions בלבד) |

## יומני ריצה

| הגדרה | ערך |
|---|---|
| run_files | `runs/run_<yyyymmdd>_<subject>.md` + `.log` לכל ריצה, גם קצרה (תבנית `T-run-short`) |
| run_log_immediacy | רישום מיידי של פעולות, ממצאי סוכנים, החלטות ולקחים; `backfill:` לשורה בדיעבד |
| run_log_language | אנגלית (ראה למעלה) |

## גיט

| הגדרה | ערך |
|---|---|
| git_scope | רק הריפו של הפרויקט שלנו; לעולם לא ריפו של פרויקט אחר |
| remote_and_push | אסור בלי אישור מפורש |
| identity | מקומית בלבד (`git config` בריפו) |
| commit_trailers | `Co-Authored-By` לפי הוראת המערכת. שורת `Claude-Session` נשמרת רק בריפו פרטי; בקומיט שמתפרסם ציבורית היא לא נכללת |
| locks_without_delete_permission | ראה modules/general/git_ops.md |

## claude.ai Project

| הגדרה | ערך |
|---|---|
| project_write | לבקש אישור בכל פעם |
| project_write_policy | רק מסמכים יציבים, במרוכז. שינוי תוכן מסמך מרוקן cache לכל הצ'אטים בפרויקט (לפי תיעוד כלי ה-Project ולפי ניסיון בניסיון קודם; לא נמדד בניסוי) |
| server_is_source_of_truth | כן; ה-Project מחזיק רק index קצר והוראות |

## בחירות כלליות

| הגדרה | ערך |
|---|---|
| delivery_mode | `server` (אפשרויות: server / upload / hybrid; ראה `core/delivery_modes.md`) |
| deliverables_dir | `deliverables/` (בתיקיית הכתיבה של הפרויקט המאמץ) |
| deliverable_format_mode | `default` (או `ask` - הצ'אט מציע רשימה ממוספרת) |
| default_deliverable_format | `md` |
| migration_source_type | - (`path` או `github`; מאגר פרטי לא נתמך) |
| migration_source | - (הנתיב המדויק בשרת או כתובת GitHub ציבורית; נקודת הפתיחה) |
| migration_output | `dir` (או `branch` באישור R2 נפרד / `report_only`) |
| migration_output_dir | - (נתיב בשרת כש-`dir`; או תיקיית פלט בענף) |
| protocol_version | PROTOMOTAI_V1 (גרסת הפרוטוקול הנוכחית; פרויקט שמאמץ רושם אותה בהוראותיו) |
| session_start_question | `דלוק` (או `כבוי`; שאלת נושא בתחילת כל צ'אט וניתוב תיעוד לפי `topics.md`) |
| protocol_source | `path` (או `github:<owner>/<repo>`; נקבע **רק בהוראות הפרויקט**; ראה `core/remote_protocol.md`) |
| protocol_ref | - (commit מלא של 40 תווים כש-source הוא github; **רק בהוראות הפרויקט**) |
| storage_mode | `local` (או `claude_project` - מתוכנן, לא ממומש; ראה `core/remote_protocol.md` סעיף 7) |
| lifecycle_stage | - (1-8 כשהמודול דלוק) |
| lifecycle_wizard | - (quick_start / general / developers / network_admins / it_managers) |
