from rest_framework import serializers

from hubs.models import Hubs


class HubsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hubs
        fields = (
            'id',
            'name',
            'stakeholder'
        )