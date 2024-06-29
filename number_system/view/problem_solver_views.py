import json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from number_system.models import DailyAPICallCount
from number_system.utils import ACSLQuestionSolver
from ..models import Profile


@csrf_exempt
def problem_solver(request):
    if request.user.is_authenticated and request.user.profile.is_premium:
        return render(request, 'pages/premium/question_solver.html')
    else:
        return render(request, 'pages/premium/non_premium.html')


def ask_question(request):
    today = timezone.now().date()

    # Retrieve or initialize the count for today
    api_count, created = DailyAPICallCount.objects.get_or_create(
        user=request.user, date=today
    )

    if api_count.request_count >= 5:
        return JsonResponse({"answer": "API call limit reached for today"})

    api_count.request_count += 1
    api_count.save()

    data = json.loads(request.body)
    question = data['question']
    answer = ACSLQuestionSolver.generate_question(question)
    return JsonResponse({'answer': answer})
