from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.api.serializers import EvaluationRunSerializer
from apps.evaluations.models import EvaluationRun


class EvaluationRunDetailAPIView(generics.RetrieveAPIView):
    serializer_class = EvaluationRunSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "evaluation_id"

    def get_queryset(self):
        return EvaluationRun.objects.filter(
            answer__request__workspace__owner=self.request.user
        ).select_related("answer", "answer__request")
