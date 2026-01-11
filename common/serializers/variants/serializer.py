from rest_framework.serializers import ModelSerializer

from apps.variants.models import Variant


class VariantCreateSerializer(ModelSerializer):
    class Meta:
        model = Variant
        fields = ["text", "is_true"]