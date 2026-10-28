# Feedback fixes — partial revision

Do not treat this package as fully aligned with the lab yet. The exact model field specifications and required Submission.__str__ output still need verification against the enrolled lab instructions.

## Confirmed corrections

The result view now calculates total_score and possible_score using Question.is_get_score(), and passes grade and possible in its template context. The template displays those values. Tests cover the weighted score and denominator, including unanswered questions.

## Repository name

The supplied evaluation requires `tfjzl-final-cloud-app-with-database`. On GitHub open your existing repository, select Settings, change Repository name to exactly that name, and click Rename. Then upload the revised files at the same paths. Do not upload an outer folder or ZIP. Keep existing migration files when updating an existing database.

After renaming, use the new URLs in the submission. Renaming alone does not address the model feedback.

## Screenshots

Your evaluation awarded full points to both screenshots. Reuse them; no replacement screenshots are included here.

## Remaining information needed

Open Coursera Module 5, Final Project: Add a New Assessment Feature to an Online Course App, and launch the lab. Copy the section specifying the Question, Choice, and Submission models, their fields/defaults, is_get_score(), and Submission.__str__(). The public course overview and IBM starter do not include those exact specifications.

The existing README describes the earlier standalone implementation. This revision note takes precedence about outstanding grading compatibility.
