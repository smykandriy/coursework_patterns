from django.http import JsonResponse


def reports_placeholder(_request):
    return JsonResponse({"detail": "Reports not implemented"}, status=501)
