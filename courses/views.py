from django.shortcuts import render, get_object_or_404
from .models import Course, Submission, Choice

def submit(request, course_id):
    if request.method == 'POST':
        submission = Submission.objects.create(user=request.user)
        for key, value in request.POST.items():
            if key.startswith('choice'):
                choice = Choice.objects.get(id=value)
                submission.choices.add(choice)
        return show_exam_result(request, submission.id)

def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    total = 0
    score = 0
    for choice in submission.choices.all():
        total += choice.question.grade
        if choice.is_correct:
            score += choice.question.grade

    context = {
        'score': score,
        'total': total,
        'submission': submission
    }
    return render(request, 'courses/exam_result.html', context)
