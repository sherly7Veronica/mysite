from rest_framework import serializers

from quote.models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = (
            'id',
            'stakeholder',
            'source',
            'destination',
            'for_date',
            'rate',
            'rate_currency',
        )