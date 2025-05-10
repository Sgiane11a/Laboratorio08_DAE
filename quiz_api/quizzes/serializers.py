from rest_framework import serializers
from .models import Quiz, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Choice (opción)"""
    class Meta:
        model = Choice
        fields = ['id', 'question', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Question (pregunta)"""
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text']


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Question con las opciones anidadas"""
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'choices']


class QuizSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Quiz (cuestionario)"""
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at']


class QuizDetailSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Quiz con preguntas y opciones anidadas"""
    questions = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'questions']
    
    def get_questions(self, obj):
        questions = obj.questions.all()
        return QuestionDetailSerializer(questions, many=True).data


class AnswerSerializer(serializers.Serializer):
    """Serializador para la validación de respuestas"""
    question_id = serializers.IntegerField()
    choice_id = serializers.IntegerField()
