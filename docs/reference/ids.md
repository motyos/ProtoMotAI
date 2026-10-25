# מזהים ופירושם

> **נוצר אוטומטית. לא לערוך ידנית.** מקורות: `filename_templates.md` (סעיף מזהים ופירושם). הפקה מחדש: `python3 tools/build_docs.py`; בדיקה: `--check`. גרסת פרוטוקול: PROTOMOTAI_V1 (גרסת הפרוטוקול הנוכחית; פרויקט שמאמץ רושם אותה בהוראותיו).

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
