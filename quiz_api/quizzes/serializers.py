from rest_framework import serializers
from .models import Quiz, Question, Choice
from categories.models import Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

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
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False
    )
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'category', 'tags']


class QuizDetailSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Quiz con preguntas y opciones anidadas"""
    questions = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'questions', 'category', 'tags']
    
    def get_questions(self, obj):
        questions = obj.questions.all()
        return QuestionDetailSerializer(questions, many=True).data


class AnswerSerializer(serializers.Serializer):
    """Serializador para la validación de respuestas"""
    question_id = serializers.IntegerField()
    choice_id = serializers.IntegerField()
