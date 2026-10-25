# שורת קטלוג בדיקות אבטחה

| מזהה | שם | סוג | שיטה וכלי | היקף (נתיבים לחישוב fingerprint) | TTL (ימים) | סטטוס קטלוג | הפניה |
|---|---|---|---|---|---|---|---|
| st-<n> | | passive / active / destructive | | | | planned / manual / automated | OWASP/MITRE |

- passive: בלי אישור. active/destructive: ברשימה ממוספרת באישור.
- בדיקה "ישנה" כשהיקף הקבצים השתנה או ה-TTL פג. **סטטוס "נכשל" על ממצא שכבר תוקן הוא מטעה - מריצים מחדש לפני סגירה.**
- הרצות ב-JSONL append-only: `ts, test, result, note, commit, dirty, fp, campaign`.
