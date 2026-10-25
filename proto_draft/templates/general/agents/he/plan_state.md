# plan_state - שורה אחת בקובץ מצב לתוכנית שלמה

`<STATE> <utc> <by> <reason>`
STATE: `NOT_ACTIVATED` / `RUNNING` / `STOPPED <סיבה>` / `PAUSED` / `DONE`
עצירות ברמת צעד לא משנות את הקובץ. הצ'אט קורא את הקובץ ומפרש את הקוד (ראה resume_prompt); אין כלי נפרד לכך.
