from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question, Choice
from .serializers import QuestionSerializers, ChoiceSerializers


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializers
    queryset = Question.objects.all()


class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializers
    queryset = Question.objects.all()


class QuestionListRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializers
    queryset = Question.objects.all()


class QuestionView(APIView):
    serializer_class = QuestionSerializers
    queryset = Question.objects.all()

    def post(self, request):
        post_data = self.request.data
        question_text = post_data['question_text']

        instance = Question.objects.create(
            question_text=question_text
        )
        result = QuestionSerializers(instance=instance).data
        return Response(result)


class ChoiceListView(generics.ListAPIView):
    serializer_class = ChoiceSerializers
    queryset = Choice.objects.all()


class ChoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializers
    queryset = Choice.objects.all()


class ChoiceListRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChoiceSerializers
    queryset = Choice.objects.all()


class ChoiceView(APIView):
    serializer_class = ChoiceSerializers

    def post(self, request):
        post_data = self.request.data
        # question_text = post_data['question_text']
        choice_text = post_data['choice_text']
        votes = post_data['votes']

        instance = Choice.objects.create(
            # question_text=question_text,
            choice_text=choice_text,
            votes=votes
        )
        result = ChoiceSerializers(instance=instance).data
        return Response(result)
