# گزارش پروژه ToDoList (فازهای ۱ تا ۴)

## 1) معرفی پروژه و هدف
پروژه‌ی ToDoList یک سیستم مدیریت پروژه و وظیفه (Task) است که کاربر می‌تواند پروژه‌ها را ایجاد کند و برای هر پروژه چندین تسک با وضعیت‌های مختلف تعریف نماید. هر تسک دارای عنوان، توضیح، وضعیت (todo / doing / done) و یک deadline اختیاری است. هدف این پروژه پیاده‌سازی مرحله‌ای سیستم با حفظ اصول OOP، معماری لایه‌ای، ذخیره‌سازی پایدار و ارائه‌ی API برای دسترسی از طریق HTTP است.

فازهای پروژه به شکل زیر طراحی و پیاده‌سازی شده‌اند:
- **فاز ۱:** CLI با ذخیره‌سازی در حافظه (In-Memory) و قوانین دامنه
- **فاز ۲:** ذخیره‌سازی پایدار با PostgreSQL + Alembic Migration
- **فاز ۲ تکمیلی:** Scheduled Task برای بستن خودکار تسک‌های overdue
- **فاز ۳:** FastAPI Web API مطابق RESTful design
- **فاز ۴:** تست End-to-End با Postman

---

## 2) معماری و ساختار کلی پروژه
ساختار پروژه بر اساس معماری لایه‌ای طراحی شده است تا وابستگی‌ها جدا و مسئولیت هر بخش مشخص باشد. این معماری در فازهای بعدی حفظ شده و فقط لایه Persistence گسترش یافته است.

### لایه‌ها
1) **Domain/Core (todo_cli/core)**
   - مدل‌های اصلی دامنه: `Project`, `Task`, `TaskStatus`
   - مستقل از نوع ذخیره‌سازی و رابط کاربری

2) **Service Layer (todo_cli/core/services + app/services)**
   - پیاده‌سازی قوانین کسب‌وکار: validationها، unique بودن، محدودیت تعداد، تغییر وضعیت و …
   - هیچ کد مستقیم دیتابیس در این لایه وجود ندارد.

3) **Persistence / Storage / Repository**
   - **InMemoryStorage** برای فاز ۱  
   - **DBStorage + Repositories + ORM Models** برای فاز ۲ و ۳  
   - وظیفه این لایه فقط خواندن/نوشتن داده است.

4) **Controller / Router (app/controllers)**
   - مرز ارتباط HTTP و تبدیل خطاهای دامنه به status code مناسب

5) **Schema Layer (app/schemas)**
   - تعریف قرارداد ورودی/خروجی API با Pydantic

---

## 3) فاز ۱ — CLI + In-Memory (OOP)
در این فاز یک CLI تعاملی پیاده‌سازی شده که تمام داده‌ها را در حافظه نگهداری می‌کند. مهم‌ترین نکته در این فاز رعایت اصول OOP و پیاده‌سازی قوانین دامنه بود.

### مهم‌ترین قوانین دامنه در فاز ۱:
- **Unique بودن نام پروژه:** دو پروژه با نام یکسان مجاز نیست.
- **محدودیت تعداد پروژه و تسک (از env):**
  - `MAX_NUMBER_OF_PROJECTS`
  - `MAX_NUMBER_OF_TASKS_PER_PROJECT`
- **اعتبار deadline:** اگر وارد شود باید تاریخ معتبر باشد.
- **وضعیت تسک فقط یکی از todo / doing / done است.**
- **Cascade delete در حافظه:** با حذف پروژه، تمام تسک‌های آن نیز حذف می‌شوند.

### فایل‌های اصلی فاز ۱:
- `todo_cli/core/models.py` → تعریف مدل‌های دامنه و Enum وضعیت
- `todo_cli/core/services.py` → قوانین دامنه و منطق پروژه/تسک
- `todo_cli/storage/in_memory_storage.py` → ذخیره‌سازی در RAM
- `todo_cli/cli/main.py` → رابط CLI و منوها
- `todo_cli/tests/*` → تست منطق سرویس و storage

### سناریوی تست فاز ۱:
1) ساخت پروژه جدید
2) افزودن چند تسک به پروژه
3) تغییر وضعیت تسک‌ها
4) حذف پروژه و مشاهده حذف شدن تسک‌ها

---

## 4) فاز ۲ — CLI + RDB (PostgreSQL) + Migration
در این فاز ذخیره‌سازی پروژه از حافظه به دیتابیس PostgreSQL منتقل شد تا داده‌ها پایدار باشند و در اجرای مجدد برنامه از بین نروند.

### علت استفاده از دیتابیس
- **ماندگاری داده** بین اجراهای مختلف
- **آمادگی برای API و توسعه‌های آینده**
- ایجاد امکان گزارش‌گیری و queryهای ساختاریافته

### ORM Models
در پوشه `app/models` دو مدل ORM ایجاد شده است:
- `Project` → جدول `projects`
- `Task` → جدول `tasks`
  
ویژگی‌های مهم:
- رابطه **One-to-Many**: هر پروژه چند تسک دارد.
- FK در Task با `ondelete="CASCADE"`
- cascade در relationship نیز فعال است تا حذف پروژه باعث حذف تسک‌ها شود.
- ذخیره‌ی وضعیت در DB با Enum و ثبت `closed_at` هنگام بسته شدن.

### Alembic Migration
برای ساخت و نسخه‌بندی دیتابیس از Alembic استفاده شد:
- تنظیمات در `alembic.ini`
- فایل اتصال Alembic به ORM در `alembic/env.py`
- migrationها در `alembic/versions/` نگهداری می‌شوند.
  
مهاجرت‌ها شامل `upgrade()` و `downgrade()` هستند تا تغییرات DB قابل اعمال/بازگشت باشد.

### فایل‌های اصلی فاز ۲
- `app/db/base.py` → Base مشترک ORM
- `app/db/session.py` → ساخت engine و SessionLocal
- `app/models/project.py`, `app/models/task.py` → مدل‌های ORM
- `app/repositories/*` → CRUD دیتابیس
- `todo_cli/storage/db_storage.py` → اتصال CLI به DB و مپ بین Domain و ORM

### نشانه موفقیت فاز ۲
بعد از ساخت پروژه و تسک در CLI، خروج از برنامه و اجرای مجدد، داده‌ها باید باقی بمانند.

---

## 5) فاز ۲ تکمیلی — Scheduled Task (Autoclose Overdue)
در این بخش یک تسک زمان‌بندی‌شده اضافه شد تا وظایف overdue به صورت خودکار بسته شوند.

### نیاز پروژه
اگر:
- `deadline < now`
- و `status != done`
  
سیستم باید:
- status تسک را `done` کند
- مقدار `closed_at` را زمان فعلی ثبت نماید.

### محل پیاده‌سازی در معماری
- **Repository:**  
  `TaskRepository.list_overdue_open_tasks()`  
  برای پیدا کردن تسک‌های overdue و باز

- **Command:**  
  `app/commands/autoclose_overdue.py`  
  شامل منطق بستن خودکار و commit تغییرات

- **Runner / Scheduler:**  
  `app/cli/console.py`  
  اجرای دوره‌ای job با کتابخانه `schedule`

### سناریوی تست Scheduled Task
1) ساخت تسک با deadline گذشته (مثلاً 2020)
2) اجرای scheduler:
poetry run python -m app.cli.console

3) مشاهده لاگ:


[autoclose] closed 1 overdue tasks

4) گرفتن خروجی API و دیدن:
- `status = done`
- `closed_at` مقدار دارد.

---

## 6) فاز ۳ — FastAPI Web API
در این فاز قابلیت‌های پروژه به صورت REST API روی FastAPI ارائه شدند.

### طراحی RESTful
- همه endpointها در کنترلرها تعریف شدند:
- `app/controllers/project_controller.py`
- `app/controllers/task_controller.py`
- تسک‌ها **nested** زیر پروژه‌ها هستند:
`/projects/{project_id}/tasks/...`

### Schemaهای Pydantic
در `app/schemas` قرارداد ورودی/خروجی تعریف شد:
- `ProjectCreate`, `ProjectUpdate`, `ProjectOut`
- `TaskCreate`, `TaskUpdate`, `TaskOut`
- با `from_attributes=True` ORMها مستقیم serialize می‌شوند.

### Error Handling
- خطاهای دامنه (ValidationError/NotFound) در سرویس رخ می‌دهند
- کنترلرها آن‌ها را به HTTP وضعیت مناسب تبدیل می‌کنند:
- 400 برای validation
- 404 برای not found
- خطاهای Pydantic → 422

### نشانه موفقیت فاز ۳
- Swagger در `/docs` بالا می‌آید
- endpointهای CRUD و PATCH قابل تست هستند.

---

## 7) فاز ۴ — تست با Postman
در این فاز تمام endpointها به صورت End-to-End با Postman تست شدند.

### موارد انجام‌شده
- ساخت environment با `base_url`
- ساخت collection شامل:
- CRUD پروژه‌ها
- CRUD تسک‌ها
- PATCH تغییر status
- تست success و error:
- deadline نامعتبر → 422
- status نامعتبر → 400
- پروژه/تسک ناموجود → 404

---

## 8) نحوه اجرای هر فاز (Runbook)

### فاز ۱
poetry run python -m todo_cli.cli.main


storage پیش‌فرض in-memory است.

### فاز ۲
docker compose up -d
poetry run alembic upgrade head
STORAGE=db
poetry run python -m todo_cli.cli.main

### فاز ۲ تکمیلی (Autoclose)
poetry run python -m app.cli.console

### فاز ۳
poetry run uvicorn app.main:app --reload


Swagger:
http://127.0.0.1:8000/docs

### فاز ۴

اجرای API

تست همه endpointها در Postman

9) جمع‌بندی و پیشنهاد توسعه

پروژه تمام نیازهای فازهای ۱ تا ۴ را پیاده‌سازی کرده است. استفاده از معماری لایه‌ای باعث شد توسعه در فازهای بعد بدون تغییر در دامنه اصلی انجام شود.

پیشنهاد برای نسخه‌های بعدی:

اضافه‌کردن pagination و filter برای لیست‌ها

اضافه‌کردن PATCH عمومی برای تسک

تبدیل Scheduled Task به cron job در محیط production

اضافه‌کردن authentication ساده برای API