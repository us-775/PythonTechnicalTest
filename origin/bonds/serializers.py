from rest_framework import serializers

from .models import Bond


class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        exclude = ('user', )

    def create(self, validated_data):
        # Fetch bond's name from GLEIF's API
        if not validated_data.get('legal_name'):
            legal_name = Bond.get_legal_name_from_gleif(validated_data['lei'])
            validated_data['legal_name'] = legal_name
        return super().create(validated_data)
