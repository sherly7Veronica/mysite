from rest_framework import serializers

from music.serializers import SongsSerializers
from .models import Question, Choice


class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'question_text',
        )


class ChoiceSerializers(serializers.ModelSerializer):
    question = QuestionSerializers()
    music = SongsSerializers()

    class Meta:
        model = Choice
        fields = (
            'id',
            'question',
            'music',
            'choice_text',
            'votes'
        )
