# status - מקור האמת למצב צעדים

> פורמט קבוע. אל תשנו סדר עמודות או צורת מפתח - פקודות grep של בדיקת תלויות נשענות עליו.

| # | מפתח | כותרת | תלויות | plan_state | exec_state | run_id | commit | tag | הערות |
|---|---|---|---|---|---|---|---|---|---|

- `plan_state`: `approved` / `draft` / `blocked` (משתנה רק בידי הבעלים)
- `exec_state`: `TODO` / `IN PROGRESS` / `BLOCKED: <ad-n | q-n | FAILED_3X | DEPCHECK | DEP <key>>` / `DONE`
- מתעדכן רק בפתיחה ובסגירה של ריצת צעד, בתוך ריצה נעולה.
