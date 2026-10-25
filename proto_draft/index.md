# ProtoMotAI - נקודת כניסה לפרוטוקול

פרוטוקול גנרי לעבודה עם claude.ai כשהוא מחובר למחשב או שרת, עם מודולי התמחות (למשל פיתוח תוכנה מאובטח).

מודול: index | פרויקט: protomotai | גרסה: 0.2 | סטטוס: טיוטה | מצב: דלוק | תלוי ב: - | רמת סיכון: נמוכה | עודכן: 2026-10-23 | עודכן על ידי: claude

## איך משתמשים
בפרויקט חדש מוסיפים להוראות שורה אחת: "לקרוא את <נתיב>/index.md ולעבוד לפיו", או "לקרוא את github:<owner>/<repo>@<commit> ולעבוד לפיו" (פרוטוקול מרוחק לקריאה בלבד; הגדרות וקבצי הפרויקט נשארים מקומיים).

## סדר קריאה (בצ'אט חדש)
0. אם שורת ההפניה בהוראות הפרויקט היא `github:<owner>/<repo>@<commit>`: קודם טוענים ומאמתים את הפרוטוקול לפי `core/remote_protocol.md` סעיף 4 (רשימה ממוספרת, אימות ה-commit), ואז קוראים מתיקיית המטמון.
1. `settings.md` – כל ההגדרות ומצב המודולים.
2. `sensitive_paths.md` – מה אסור לקרוא ומה נקרא רק אחרי מיסוך.
3. `core/protocol_core.md` – הליבה (חובה).
   אחריה `topics.md` – שאלת הפתיחה "על איזה נושא נעבוד?" וניתוב התיעוד (כש-`session_start_question` דלוק).
4. רק מודולים שמצבם **דלוק** בהגדרות (`modules/general/*`, `modules/specialization/*`). מודול הסוכנים הוא תיקייה: מתחילים ב-`agents/module.md`, ומשם לתת-קבצים הדלוקים.
5. `filename_templates.md` ו-`templates/templates_registry.md` – בעת יצירת קובץ.
6. לפי צורך: `profiles.md` (פרופילים מקצועיים והתמחות), `core/remote_protocol.md` (הגדרות פרויקט `project_settings.md`, מקור מרוחק), `core/tools_install.md` (התקנת כלים עם `pin`), `tools_build/` ו-`tools_install/` (קטלוגי כלים), `security/` (פרוטוקולי אבטחה) (הרישום מצביע לתבנית בתיקיית המודול).

## בתחילת כל צ'אט
אחרי הקריאה לפי הסדר, הצ'אט שואל: **"על איזה נושא נעבוד?"** (brainstorm / decision / question / scenario / work / review / resume / chat) ומתעד לפי `topics.md`. כל תיעוד באישור ממוספר.

## שלוש הנחיות שאסור לפספס
- לפני כל פעולה: רשימה **ממוספרת** וממתינים לאישור ("אשר 1,3 / דחה 2 / שנה 4"). מספר שלא הוזכר = לא מאושר.
- לא נוגעים בשום דבר שמחוץ לתיקיית הכתיבה; מה שלא ברשימה אסור גם לקריאה.
- לא מדפיסים סודות; אם לא יודעים – שואלים ולא ממציאים.

## פרויקט חדש מאמץ - ארבעה צעדים
`<נתיב>` בשורת ההפניה הוא ערך `protocol_path` ב-`settings.md` (נתיב מלא בשרת). תיקיית `instructions/` וכל קבצי הפרויקט המאמץ ממוקמים יחסית לתיקיית הכתיבה שלו, לא לתיקיית הפרוטוקול.
ראה `core/protocol_core.md` סעיף 12.8. חזרה אחרי קטיעה: 12.9. תנאי עצירה מרוכזים: 12.10.

## כלים
`tools/sync_settings.py` (עדכון כותרות מודולים לפי מתגי `settings.md`; עם `--project-settings` מציג מצב אפקטיבי בלי לכתוב לפרוטוקול; בדיקה עצמית `tools/test_sync_settings.py`), `tools/runlog.sh` (שורת יומן עם `date -u`), `tools/check_template.py` (בדיקת שדות חובה לפי `templates/required_fields.json`), `tools/scan_project.py` (סריקה בקריאה בלבד למיגרציה; בדיקה עצמית: `tools/test_scan_project.py`), `tools/run_lock.sh` (נעילת ריצה), `tools/check_resources.sh` (בדיקת דיסק ומשאבים לפני גל סוכנים), `tools/build_docs.py` (הפקת `docs/reference/` מהמקורות) ו-`tools/check_links.py` (קישורים שבורים; בדיקה עצמית `tools/test_build_docs.py`), `tools/run_metrics.py` (סטטיסטיקת ריצה; בדיקה עצמית `tools/test_run_metrics.py`), `tools/check_tools.py` (רישום כלים מול התיקייה; בדיקה עצמית `tools/test_check_tools.py`), `tools/check_overview.py` (סטיית עמוד סקירה), `tools/leak_check.py` (בדיקת דליפת סודות לפי hash לפני העלאה, מדפיס נתיב:שורה בלבד), `tools/check_traceability.py` (עקיבות דרישה -> תרחיש -> הוכחה; בדיקה עצמית `tools/test_check_traceability.py`), `tools/check_manifest.py` (מניפסט פרופילים מקצועיים; בדיקה עצמית `tools/test_check_manifest.py`).

## מבנה
```
index.md  settings.md  topics.md  filename_templates.md  sensitive_paths.md  tools.md
core/{protocol_core,deliverables,delivery_modes,remote_protocol,tools_install}.md
tools_build/{index,ts-<n>_*}.md   tools_install/{index,ti-<n>_*}.md   security/{index,downloads_installs}.md
modules/general/{server_link,git_ops}.md
modules/general/project_lifecycle/{module,stages}.md  +  wizards/{quick_start,general,developers,network_admins,it_managers}.md
modules/general/migration/{module,wizard,gap_checklist}.md
modules/general/agents/{module,start_and_resume,run_lock,tokens_and_engine,agents_procedure,
                        auto_decisions,consultation_panel,auto_plan_activation}.md
modules/specialization/<פרופיל>/{module,scenarios}.md   profiles.md  (למשל secure_dev)
templates/templates_registry.md   (הגדרת כל התבניות)
templates/<core|general|specialization>/<מודול>/<שפה>/*.md
```

## כותרת מודול
בראש כל קובץ שורת מפתח:ערך שמתעדכנת ומתרחבת: `מודול | פרויקט | גרסה | סטטוס: טיוטה/מאושר | מצב: כבוי/דלוק | תלוי ב | רמת סיכון | עודכן | עודכן על ידי | ...`.
מעבר מטיוטה ל"מאושר" והדלקה/כיבוי = שינוי בשורה זו ובטבלה ב-`settings.md`.
