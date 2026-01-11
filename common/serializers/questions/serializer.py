from rest_framework.serializers import ModelSerializer

from apps.questions.models import Questions
from common.serializers.variants.serializer import VariantCreateSerializer


class QuestionCreateSerializer(ModelSerializer):
    variants = VariantCreateSerializer(many=True, required=True)

    class Meta:
        model = Questions
        fields = ["text", "points", "variants"]


