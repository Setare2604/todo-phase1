import time
import schedule
from app.db.session import SessionLocal
from app.commands.autoclose_overdue import autoclose_overdue_tasks

def job():
    db = SessionLocal()
    try:
        closed_count = autoclose_overdue_tasks(db)
        print(f"[autoclose] closed {closed_count} overdue tasks")
    finally:
        db.close()

def main():
    # هر 10 دقیقه یک بار
    schedule.every(10).minutes.do(job)

    print("Autoclose scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()