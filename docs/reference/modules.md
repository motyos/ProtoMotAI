# מודולים

> **נוצר אוטומטית. לא לערוך ידנית.** מקורות: `settings.md` (טבלת המתגים), כותרת כל קובץ מודול. הפקה מחדש: `python3 tools/build_docs.py`; בדיקה: `--check`. גרסת פרוטוקול: PROTOMOTAI_V1 (גרסת הפרוטוקול הנוכחית; פרויקט שמאמץ רושם אותה בהוראותיו).

הליבה תמיד פעילה. מודול בן פעיל רק אם האב דלוק. המצב כאן הוא ברירת המחדל לפרויקט חדש.

| מפתח | קובץ | אב | מצב בהגדרות | מצב אפקטיבי | גרסה | סטטוס | סיכון | תלוי ב |
|---|---|---|---|---|---|---|---|---|
| `server_link` | `modules/general/server_link.md` |  | דלוק | דלוק | 0.1 | טיוטה | בינונית | core |
| `git_ops` | `modules/general/git_ops.md` |  | דלוק | דלוק | 0.2 | טיוטה | בינונית | core |
| `secure_dev` | `modules/specialization/secure_dev/module.md` |  | כבוי | כבוי | 0.2 | טיוטה | גבוהה | core, server_link |
| `agents` | `modules/general/agents/module.md` |  | כבוי | כבוי | 0.2 | טיוטה | גבוהה | core, server_link |
| `agents.start_and_resume` | `modules/general/agents/start_and_resume.md` | agents | דלוק | כבוי | 0.2 | טיוטה | בינונית | agents |
| `agents.run_lock` | `modules/general/agents/run_lock.md` | agents | דלוק | כבוי | 0.2 | טיוטה | בינונית | agents |
| `agents.tokens_and_engine` | `modules/general/agents/tokens_and_engine.md` | agents | דלוק | כבוי | 0.2 | טיוטה | נמוכה | agents |
| `agents.agents_procedure` | `modules/general/agents/agents_procedure.md` | agents | דלוק | כבוי | 0.2 | טיוטה | גבוהה | agents |
| `agents.auto_decisions` | `modules/general/agents/auto_decisions.md` | agents | כבוי | כבוי | 0.2 | טיוטה | גבוהה | core, agents |
| `agents.consultation_panel` | `modules/general/agents/consultation_panel.md` | agents.auto_decisions | כבוי | כבוי | 0.2 | טיוטה | גבוהה | agents, auto_decisions |
| `agents.auto_plan_activation` | `modules/general/agents/auto_plan_activation.md` | agents.auto_decisions | כבוי | כבוי | 0.2 | טיוטה | גבוהה | core, agents, auto_decisions |
| `migration` | `modules/general/migration/module.md` |  | כבוי | כבוי | 0.1 | טיוטה | בינונית | core, server_link, git_ops |
| `project_lifecycle` | `modules/general/project_lifecycle/module.md` |  | כבוי | כבוי | 0.1 | טיוטה | נמוכה | core |
| `wizard.quick_start` | `modules/general/project_lifecycle/wizards/quick_start.md` | project_lifecycle | כבוי | כבוי | 0.1 | טיוטה | נמוכה | project_lifecycle |
| `wizard.general` | `modules/general/project_lifecycle/wizards/general.md` | project_lifecycle | כבוי | כבוי | 0.1 | טיוטה | נמוכה | project_lifecycle |
| `wizard.developers` | `modules/general/project_lifecycle/wizards/developers.md` | project_lifecycle | כבוי | כבוי | 0.1 | טיוטה | בינונית | project_lifecycle, secure_dev |
| `wizard.network_admins` | `modules/general/project_lifecycle/wizards/network_admins.md` | project_lifecycle | כבוי | כבוי | 0.1 | טיוטה | גבוהה | project_lifecycle |
| `wizard.it_managers` | `modules/general/project_lifecycle/wizards/it_managers.md` | project_lifecycle | כבוי | כבוי | 0.1 | טיוטה | בינונית | project_lifecycle |
