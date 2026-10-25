# templates_registry - הגדרת כל התבניות במקום אחד

מודול: templates | פרויקט: protomotai | גרסה: 0.1 | סטטוס: טיוטה | מצב: דלוק | תלוי ב: settings | רמת סיכון: נמוכה | עודכן: 2026-10-23 | עודכן על ידי: claude

> **קובץ ההגדרה היחיד לתבניות.** כדי להוסיף, לשנות או לבטל תבנית - משנים שורה כאן. כל תבנית יושבת לפי: `templates/<סוג מודול>/<מודול>/<שפה>/<קובץ>`. סוג מודול: `core` / `general` / `specialization`. תבנית של מודול כבוי לא בשימוש (גם אם הקובץ קיים).
> שפת התוצר = שפת התבנית (`templates_language` ב-`settings.md`). תבנית בשפה אחרת נכנסת לתיקיית שפה מקבילה (`en/`) ונרשמת כאן באותו מזהה.

## עמודות
- **מזהה** - קבוע, לא ממוחזר. **מודול** - איזה מודול אחראי. **נתיב תוצר** - איפה נוצר הקובץ בפרויקט המאמץ (לפי `filename_templates.md`). **שדות חובה** - מה חייב להיות מלא (ריק אסור; "אין" מותר). **גרסה מינימלית** - התבנית הקלה לאותה מטרה.

## core
| מזהה | קובץ (בתיקיית he) | מטרה | נתיב תוצר | שדות חובה | גרסה מינימלית |
|---|---|---|---|---|---|
| T-run | core/he/run_progress.md | קובץ התקדמות ריצה מלא | runs/run_<yyyymmdd>_<subject>.md | מטרה, אישור (ציטוט UTC), נקודת חזרה, טבלת שלבים, סיכום סיום | T-run-short |
| T-run-short | core/he/run_progress_short.md | ריצה קצרה / תיעוד בלבד | runs/run_<yyyymmdd>_<subject>.md | מטרה, אישור, נקודת חזרה, סיכום סיום | - |
| T-close | core/he/closing_summary.md | סיכום סיום (9 שדות, 0-8) | בתוך קובץ הריצה | כל השדות; "מה לא נקרא" חובה | - |
| T-decision | core/he/decision_record.md | החלטת בעלים (`d-<n>`) | decisions.md | סטטוס, נדחו, אושר על ידי (ציטוט + תאריך ושעת UTC), מחליף | - |
| T-question | core/he/open_question_row.md | שאלה פתוחה (`q-<n>`) | open_questions.md | מזהה, שאלה, סטטוס מרשימה סגורה | - |
| T-finding | core/he/finding_record.md | ממצא (`f-<n>`) | בתוך קובץ הריצה / findings.md | מיקום מדויק, חומרה, בדיקת חזרה | - |
| T-tools | core/he/tools_page.md | רישום כלים בפרויקט | tools.md | מזהה, נתיב, מה עושה, מתי מפעילים, סיכון | שם + מה עושה + מתי |
| T-metrics | core/he/metrics_page.md | סטטיסטיקות ריצות (הערכה מול ביצוע) | runs/metrics.md | ריצה, זמן פעיל, הערכה, ניצול סשן, כיול | - |
| T-pset | core/he/project_settings.md | דריסות הגדרות הפרויקט (מתגים וערכים) | project_settings.md | מתגי מודולים, דריסות ערכים, storage_mode | - |
| T-ptools | core/he/project_tools.md | כלים מותקנים ומקובעים בפרויקט | project_tools.md | מזהה, pin, verify_command, אושר על ידי, מצב | - |
| T-toolspec | core/he/tool_spec.md | תיאור כלי גנרי (לייצור עצמי או להתקנה) | tools_build/ts-<n>_<subject>.md או tools_install/ti-<n>_<subject>.md | סוג, למה נדרש, מה עושה, מה נדרש, סיכון, כללי כשל-סגור, בדיקות קבלה, pin, verify_command, פרוטוקול אבטחה | - |
| T-secproto | core/he/security_protocol.md | פרוטוקול אבטחה לנושא אחד | security/<subject>.md | מטרה, מתי חל, צעדים, סיכונים, רשימת בדיקה, מה נרשם | - |
| T-pmanifest | core/he/profile_manifest.md | מניפסט פרופיל מקצועי | modules/specialization/<key>/module.md (סעיף מניפסט) | key, שם, סוג, תחומים, גרסה, בשלות, תפקיד, מחברים, רישיון, מקורות, מה זה לא | - |
| T-sessions | core/he/sessions_page.md | יומן צ'אטים לפי נושא | runs/sessions.md | תאריך UTC, סוג נושא, תיאור קצר, קבצים, ריצה | - |
| T-next | core/he/next_in_queue.md | "הבא בתור" - נקודת כניסה לצ'אט חדש | בראש todo.md | ריצה אחרונה, צעד הבא | - |
| T-scope | core/he/scope_file.md | קובץ היקף: כתיבה / קריאה בלבד / אסור | scope.md | נתיבי כתיבה, קריאה בלבד, אסורים | - |
| T-deliverables | core/he/deliverables_index.md | רשימת תוצרים | deliverables/index.md | קובץ, פורמט, תאריך, מצב | - |
| T-instr | core/he/project_instructions.md | הוראות פרויקט מאמץ (שורת הפניה אחת) | instructions/project_instructions.md | שם, תיקיית כתיבה, מודולים דלוקים | - |

## general/agents (נטען רק כשמודול agents דלוק)
| מזהה | קובץ | מטרה | נתיב תוצר | שדות חובה | גרסה מינימלית |
|---|---|---|---|---|---|
| T-step | general/agents/he/step_plan.md | תכנית צעד (6 סעיפים) | plan/<key>_plan.md | התחל כאן, תלויות כפקודת OK, פעולות עם אימות, טבלת "נקטע אחרי פעולה N" | - (זו כבר המינימלית) |
| T-status | general/agents/he/status_table.md | מקור אמת למצב צעדים | plan/status.md | plan_state, exec_state, run_id, commit | - |
| T-contracts | general/agents/he/contracts.md | שמות חוצי-צעדים | plan/contracts.md | producer, consumers | - |
| T-ad | general/agents/he/auto_decision_record.md | החלטה אוטומטית (`ad-<n>`) | auto_decisions.md | ספק, סיווג קריטיות, חלופות, קלות תיקון, סטטוס אישור | - |
| T-brief-common | general/agents/he/agent_brief_common.md | כללים משותפים לסוכנים | runs/evidence/<run>/briefs/common.md | כללים קשיחים, דפוסי כשל, יומן גולמי | - |
| T-brief-worker | general/agents/he/agent_brief_worker.md | תדריך סוכן עובד | runs/evidence/<run>/briefs/brief_<id>.md | מטרה, קבצים בבעלותך, אסור, הגדרת סיום | - |
| T-brief-mut | general/agents/he/agent_brief_mutation.md | תדריך מוטציות | runs/evidence/<run>/briefs/brief_mut_<id>.md | מטרה, בסיס, שיטה, מוטציות, דוח | - |
| T-brief-review | general/agents/he/agent_brief_review.md | תדריך סקירה בלתי תלויה | runs/evidence/<run>/briefs/brief_review.md | דרישות, התמקדות, אסור, פורמט דוח | - |
| T-cold | general/agents/he/cold_start_questionnaire.md | שאלון פתיחה קרה (7 שאלות) | runs/evidence/<run>/cold_start_r<n>.md | שאלות, VERDICT, MISSING | - |
| T-approval | general/agents/he/master_approval.md | אישור אחד לתוכנית | plan/master_approval.md | hash, מה מאושר, מה לא מאושר, עצירות קבועות | - |
| T-resume | general/agents/he/resume_prompt.md | הודעת המשך אחת | plan/resume_prompt.md | plan_state, run_lock, קודי יציאה | - |
| T-restart | general/agents/he/post_restart_checklist.md | בדיקות אחרי אתחול | plan/post_restart_checklist.md | פקודה, תוצאה, עוצר | - |
| T-lock | general/agents/he/run_lock_file.md | קובץ נעילת ריצה | run_lock.md | status, run_id, started_utc, last_update_utc | - |
| T-planstate | general/agents/he/plan_state.md | מצב תוכנית בשורה אחת | plan/plan_state.txt | STATE, NOT_ACTIVATED | - |

## general/project_lifecycle (נטען רק כשהמודול דלוק)
| מזהה | קובץ | מטרה | נתיב תוצר | שדות חובה | גרסה מינימלית |
|---|---|---|---|---|---|
| T-profile | general/project_lifecycle/he/user_profile.md | פרופיל משתמש | project/profile.md | תפקיד, סגנון עבודה | - |
| T-goal | general/project_lifecycle/he/goal_smart.md | מטרת הפרויקט SMART | project/goal.md | מדד, תאריך יעד, מחוץ להיקף | quick_start brief |
| T-stakeholders | general/project_lifecycle/he/stakeholders.md | בעלי עניין ו-RACI | project/stakeholders.md | RACI, השפעה | - |
| T-budget | general/project_lifecycle/he/budget_timeline.md | תקציב ולוח זמנים | project/budget_timeline.md | תקציב, לוח זמנים, אבן דרך | - |
| T-brainstorm | general/project_lifecycle/he/brainstorm_topic.md | נושא סיעור | project/brainstorm.md (או `draft/brainstorm/<subject>.md` כשהמודול כבוי, ראה topics.md) | סטטוס, חלופות, ביקורת אבטחה, תרחישים מועמדים, החלטת הבעלים | - |
| T-wbs | general/project_lifecycle/he/wbs_todo.md | פירוק משימות ועדיפויות MoSCoW | todo.md | עדיפות, בעלים, אומדן | - |
| T-scenario | general/project_lifecycle/he/scenario.md | תרחיש קבלה | project/scenarios.md (או `draft/scenarios/<subject>.md` כשהמודול כבוי, ראה topics.md) | מצב, מפעיל, צעדים, נגזר מ, אופן בדיקה, תוצאה צפויה, commit שנבדק | - |
| T-overview | general/project_lifecycle/he/overview_page.md | עמוד סקירה / כניסה לצ'אט חדש | project/overview.md | מצב והצעד הבא, מפת מסמכים, כללי עבודה קריטיים, מגבלות ידועות, עודכן | - |
| T-risks | general/project_lifecycle/he/risk_register.md | רישום סיכונים | project/risks.md | סבירות, השפעה, תגובה | - |
| T-canvas | general/project_lifecycle/he/business_canvas.md | מודל עסקי (Canvas) | project/canvas.md | פלחי לקוחות, הצעת ערך, ערוצים, קשרי לקוחות, מקורות הכנסה, משאבי מפתח, פעילויות מפתח, שותפים מרכזיים, מבנה עלויות | - |
| T-trace | general/project_lifecycle/he/traceability.md | עקיבות דרישה, תרחיש, בדיקה | project/traceability.md (או `draft/traceability.md` כשהמודול כבוי) | דרישה, עדיפות, תרחישים | - |
| T-gate | general/project_lifecycle/he/stage_gate.md | שער שלב | project/gates/gate_<n>.md | קריטריוני יציאה, החלטה, בעלים מאשר | - |

## general/migration (נטען רק כשהמודול דלוק)
| מזהה | קובץ | מטרה | נתיב תוצר | שדות חובה | גרסה מינימלית |
|---|---|---|---|---|---|
| T-inventory | general/migration/he/inventory_report.md | מלאי פרויקט מהסריקה | runs/migration/inventory.md | מקור, תאריך סריקה, מה לא נסרק, חשד לסודות | - |
| T-gaps | general/migration/he/gap_report.md | דוח פערים מול הפרוטוקול | runs/migration/gaps.md | בדיקה, מצב, חומרה, המלצה | - |
| T-migplan | general/migration/he/migration_plan.md | תוכנית מיגרציה ממוספרת | runs/migration/plan.md | פלט, נקודת חזרה, בעלים מאשר, סיכון, אימות | - |

## general/server_link
| מזהה | קובץ | מטרה | נתיב תוצר | שדות חובה | גרסה מינימלית |
|---|---|---|---|---|---|
| T-snapshot | general/server_link/he/snapshot_info.md | הצהרת צילום להעלאה החוצה | בתוך החבילה שמועלית | נוצר, commit, זה צילום, דליפת סודות | - |

## specialization/secure_dev
| מזהה | קובץ | מטרה | נתיב תוצר | שדות חובה | גרסה מינימלית |
|---|---|---|---|---|---|
| T-campaign | specialization/secure_dev/he/security_campaign.md | קמפיין בדיקות אבטחה | security/campaigns/sx-<yyyymmdd>-<name>.md | אושר על ידי הבעלים, commit בסיס, ראיות, ניקוי | - |
| T-sectest | specialization/secure_dev/he/security_test_catalog_row.md | שורת קטלוג בדיקות | security/security_tests.md | סוג, היקף, TTL | - |

## כללי שימוש
1. יוצרים קובץ רק מתבנית רשומה כאן. אין תבנית מתאימה - מוסיפים שורה כאן קודם.
2. בלוק משותף שחוזר בכמה קבצים (למשל כללים קבועים) יושב בקובץ אחד ומפנים אליו. **לא מעתיקים** - בניסיון קודם הבלוק שהועתק ל-56 קבצים התפצל ל-50 גרסאות.
3. עמודה ריקה בתבנית היא ריקה בכוונה רק אם כתוב "אין". תבנית שחלק מהשדות בה ריקים תמיד - מבטלים את השדה (בניסיון קודם שדות כאלה היו תקורה בלבד).
4. אחרי ריצה ראשונה בפרויקט חדש: לרשום אילו שדות חסרו או ריקים, ולעדכן כאן.
5. מזהה תבנית לא ממוחזר.
