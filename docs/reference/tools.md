# כלים

> **נוצר אוטומטית. לא לערוך ידנית.** מקורות: `tools.md`. הפקה מחדש: `python3 tools/build_docs.py`; בדיקה: `--check`. גרסת פרוטוקול: PROTOMOTAI_V1 (גרסת הפרוטוקול הנוכחית; פרויקט שמאמץ רושם אותה בהוראותיו).

| מזהה | סוג | נתיב / קישור | מה עושה | מתי מפעילים | קלט → פלט | סיכון | אכיפה | נייד? | סטטוס ואימות |
|---|---|---|---|---|---|---|---|---|---|
| tool-1 | protocol | `tools/runlog.sh` | שורת יומן ריצה עם חותמת UTC | מיד אחרי כל פעולה, ממצא, החלטה, לקח | טקסט → שורה בקובץ `.log` | R1 | instruction | כן | פעיל; בשימוש בריצות |
| tool-2 | protocol | `tools/check_template.py` | בדיקת שדות חובה בקובץ שנוצר מתבנית | אחרי יצירת קובץ מתבנית | מזהה תבנית + קובץ → OK/FAIL | R0 | warn | כן | פעיל |
| tool-3 | protocol | `tools/sync_settings.py` | סנכרון כותרות מודולים עם טבלת המתגים; `--summary`; `--project-settings` (מצב אפקטיבי עם דריסות הפרויקט, בלי כתיבה לפרוטוקול); אזהרת ספים בטקסט | אחרי שינוי מתג; בסוף ריצה | `settings.md` → כותרות מודולים (`--apply`) | R0 / R1 (`--apply`) | warn | כן | פעיל |
| tool-4 | protocol | `tools/scan_project.py` | מלאי פרויקט בקריאה בלבד, חשד לסודות כנתיב:שורה:סוג | מיגרציה M2 | תיקייה → דוח markdown | R0 | instruction | כן | נבדק בדמה (test_scan_project.py) |
| tool-5 | protocol | `tools/test_scan_project.py` | בדיקה עצמית ל-scan_project | אחרי שינוי ב-scan_project | → PASS/FAIL | R0 | instruction | כן | פעיל |
| tool-6 | protocol | `tools/leak_check.py` | בדיקת דליפת סודות לפי hash לפני העלאה | לפני העלאה ל-Project / החוצה | קבצי סודות + קבצי יעד → MATCH נתיב:שורה | R0 | instruction | כן | נבדק (test_leak_check.py). נכשל סגור: קוד 2 כשלא נטענו סודות, קוד 3 כשדולגו קבצים. חריג מוסכם: הסקריפט (לא הצ'אט) קורא את קובצי הסודות, באישור ממוספר מפורש |
| tool-7 | protocol | `tools/run_lock.sh` | נעילת ריצה (acquire/check/heartbeat/log/release/takeover) | תחילת וסוף כל ריצה (agents דלוק) | פקודות → `run_lock.md` | R1 | instruction | Linux בלבד (GNU date, flock) | נבדק (test_shell_tools.py); heartbeat/log/release דורשים `RUN_ID` של הבעלים; טרם בריצה אמיתית |
| tool-8 | protocol | `tools/check_resources.sh` | דיסק, עומס וזיכרון לפני גל סוכנים | לפני גל סוכנים | תיקייה → מספרים וקוד יציאה | R0 | instruction | כן | נבדק (test_shell_tools.py); ערך לא מספרי = קוד 2 |
| tool-9 | protocol | `tools/check_overview.py` | סטיית עמוד סקירה (סדר פרקים ותאריך) | בסוף ריצה / שער (lifecycle דלוק) | `overview.md` → אזהרות | R0 | warn | כן | לא נבדק אוטומטית |
| tool-10 | protocol | `tools/check_tools.py` | השוואת רישום הכלים לתיקיית `tools/` | בסוף ריצה שנגעה ב-`tools/` | `tools.md` → אזהרות | R0 | warn | כן | נבדק בדמה (test_check_tools.py) |
| tool-11 | protocol | `tools/test_check_tools.py` | בדיקה עצמית ל-check_tools | אחרי שינוי ב-check_tools | → PASS/FAIL | R0 | instruction | כן | פעיל |
| tool-12 | protocol | `tools/run_metrics.py` | סטטיסטיקת ריצה מהיומן ומ-git, שורה ל-`runs/metrics.md`, בדיקת שורה חסרה וכיול | בסגירת כל ריצה (core §12.7) | `.log` (+ התקדמות) → שורה ב-metrics.md | R1 | warn | כן | נבדק בדמה (test_run_metrics.py) |
| tool-13 | protocol | `tools/test_run_metrics.py` | בדיקה עצמית ל-run_metrics | אחרי שינוי ב-run_metrics | → PASS/FAIL | R0 | instruction | כן | פעיל |
| tool-14 | protocol | `tools/build_docs.py` | הפקת `docs/reference/` (מודולים, הגדרות, תבניות, כלים) מהמקורות; `--check` מזהיר על סטייה | אחרי שינוי בהגדרות, ברישום תבניות או ב-`tools.md`; בסגירת ריצה שנגעה בפרוטוקול (§12.4) | מקורות הפרוטוקול → `docs/reference/*.md` | R1 (כותב); `--check` R0 | warn | כן | נבדק בדמה (test_build_docs.py) |
| tool-15 | protocol | `tools/check_links.py` | בדיקת קישורי markdown יחסיים שבורים | אחרי שינוי במסמכים; בסגירת ריצה שנגעה בפרוטוקול (§12.4) | תיקיות/קבצי md → אזהרות | R0 | warn | כן | נבדק בדמה (test_build_docs.py) |
| tool-16 | protocol | `tools/test_build_docs.py` | בדיקה עצמית ל-build_docs ול-check_links | אחרי שינוי באחד מהם | → PASS/FAIL | R0 | instruction | כן | פעיל |
| tool-17 | protocol | `tools/test_sync_settings.py` | בדיקה עצמית ל-`sync_settings.py --project-settings` | אחרי שינוי ב-sync_settings | → PASS/FAIL | R0 | instruction | כן | פעיל |
| tool-18 | protocol | `tools/check_traceability.py` | בדיקת עקיבות דרישה -> תרחיש -> הוכחה (חייב בלי תרחיש, תרחיש בוצע בלי הוכחה או commit, הוכחה ישנה מול HEAD) | לפני שער המוכנות; בריצת קבלה (lifecycle דלוק) | `scenarios.md` + `traceability.md` (+ `--head`) → אזהרות | R0 | warn | כן | נבדק בדמה (test_check_traceability.py) |
| tool-19 | protocol | `tools/test_check_traceability.py` | בדיקה עצמית ל-check_traceability | אחרי שינוי ב-check_traceability | → PASS/FAIL | R0 | instruction | כן | פעיל |
| tool-20 | protocol | `tools/check_manifest.py` | בדיקת מניפסט פרופילים מקצועיים (שדות, גרסה, בשלות, הצהרת "לא הסמכה", עקביות עם `profiles.md` ועם טבלת המתגים) | אחרי הוספה או שינוי של פרופיל | `modules/specialization/*` + `profiles.md` → אזהרות | R0 | warn | כן | נבדק בדמה (test_check_manifest.py) |
| tool-21 | protocol | `tools/test_check_manifest.py` | בדיקה עצמית ל-check_manifest | אחרי שינוי ב-check_manifest | → PASS/FAIL | R0 | instruction | כן | פעיל |
| tool-22 | protocol | `tools/check_registry.py` | עקביות `templates_registry.md` מול `required_fields.json` (מזהים, עמודת שדות חובה, מילות מפתח בקבצי התבנית) | אחרי שינוי בתבנית או ברישום | → OK/FAIL | R0 | instruction | כן | פעיל |
| tool-23 | protocol | `tools/test_check_registry.py` | בדיקה עצמית ל-check_registry | אחרי שינוי ב-check_registry | → PASS/FAIL | R0 | instruction | כן | פעיל |
| tool-24 | protocol | `tools/test_leak_check.py` | בדיקה עצמית ל-leak_check (נכשל סגור, דילוגים, התאמה) | אחרי שינוי ב-leak_check | → PASS/FAIL | R0 | instruction | כן | פעיל |
| tool-25 | protocol | `tools/test_shell_tools.py` | בדיקה עצמית ל-run_lock.sh, runlog.sh ו-check_resources.sh | אחרי שינוי באחד מהם | → PASS/FAIL | R0 | instruction | Linux בלבד | פעיל |
