# Django Online Course — Assessment Feature

A standalone implementation of the assessment requirements provided in the assignment: models, admin configuration, course lessons, exam submission, and result evaluation. This is a new project, not a patch to an existing course lab checkout. If the lab uses different fields or routes, reconcile those differences before submitting.

## Run locally (PowerShell)

Use Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in with the user you created. Enroll in the sample course, select answers, and submit the exam. The admin site is at http://127.0.0.1:8000/admin/. To add ordinary learner accounts, use the admin Users section. No credentials are bundled.

## Required GitHub files

1. `onlinecourse/models.py`: Question, Choice, Submission and supporting models.
2. `onlinecourse/admin.py`: exactly seven model imports; QuestionInline, ChoiceInline, QuestionAdmin, LessonAdmin, and registrations.
3. `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`: course name, all lessons, Bootstrap layout, and exam form.
4. `onlinecourse/views.py`: submit and show_exam_result, plus course browsing/enrollment.
5. `onlinecourse/urls.py`: named routes for submission and exam results.

Create a GitHub repository and upload the contents of this folder so `manage.py` is at the repository root. Include migrations, requirements, templates, and project settings. Open each required file in GitHub and copy its file URL for the corresponding assessment task. The HTML template is inside `onlinecourse/templates/onlinecourse/`.

Screenshots are excluded as requested. The original assessment still lists screenshot tasks; this package supplies the code portion only. No GitHub repository has been created or published by this package.

## Exam behavior

- Users must sign in and enroll before submitting. Submission accepts POST only and uses CSRF protection.
- The server checks that each selected choice belongs to its question and course.
- Each question earns its full weight only for the exact set of correct answers. Unanswered questions earn zero. Questions without a correct option earn zero.
- This application's pass mark is 80%, independently of Coursera's 70% assignment passing grade.
- Results are private to the submitting user. Each retake creates a separate submission.
- Scores are stored at submission time. The answer review uses the current question/choice text: do not edit a live exam after submissions if historical review must stay unchanged.
- Bootstrap loads from a CDN; internet access is needed for its styling.
- Development settings default to DEBUG enabled. Before public deployment, configure a secret key, DEBUG=0, allowed hosts, HTTPS, static asset hosting, and a production server/database.

## Validation

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```
