
from rest_framework.serializers import ImageField, CharField
from rest_framework.serializers import ModelSerializer

from apps.questions.models import Questions
from apps.quiz.models import Quiz
from apps.variants.models import Variant
from common.serializers.questions.serializer import QuestionCreateSerializer
from common.utils import delete_files, save_unique_file


class QuizListSerializer(ModelSerializer):

    class Meta:
        model = Quiz
        fields = [
                  "id",
                  "quiz_img",
                  "title",
                  "description",
                  "password",
                  "time_limit",
                  "is_finished",
                  "slug"
                  ]


class QuizDetailSerializer(ModelSerializer):

    questions = QuestionCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
                  "id",
                  "quiz_img",
                  "title",
                  "description",
                  "password",
                  "time_limit",
                  "questions",
                  "is_finished",
                  "slug"
                  ]



class QuizCreateSerializer(ModelSerializer):
    quiz_img = ImageField(required=False)
    password = CharField(required=False)
    questions = QuestionCreateSerializer(many=True, required=False)

    class Meta:
        model = Quiz
        fields = ["quiz_img", "title", "description", "password", "time_limit", "questions"]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")
        quiz_img = validated_data.pop("quiz_img", None)

        # Quiz yaratish
        quiz = Quiz.objects.create(**validated_data)
        if quiz_img:
            quiz.quiz_img = quiz_img
            quiz.save()

        # Har bir question va uning variantlarini yaratish
        for question_data in questions_data:
            variants_data = question_data.pop("variants")
            question = Questions.objects.create(quiz=quiz, **question_data)
            for variant_data in variants_data:
                Variant.objects.create(question=question, **variant_data)

        return quiz




class QuizUpdateSerializer(ModelSerializer):
    quiz_img = ImageField(required=False, allow_null=True)
    questions = QuestionCreateSerializer(many=True, required=False)

    class Meta:
        model = Quiz
        fields = ["quiz_img", "title", "description", "time_limit", "questions"]

    def update(self, instance, validated_data):
        # --- Image handling ---
        new_image = validated_data.pop("quiz_img", None)

        if new_image is None and "quiz_img" in self.initial_data:
            if instance.quiz_img:
                delete_files([instance.quiz_img.url])
                instance.quiz_img = None

        elif new_image:
            if instance.quiz_img:
                delete_files([instance.quiz_img.url])
            instance.quiz_img = save_unique_file(new_image, "quiz_images")

        # --- Update Quiz fields ---
        for attr, value in validated_data.items():
            if attr != "questions":
                setattr(instance, attr, value)
        instance.save()

        # --- Nested Questions & Variants ---
        questions_data = validated_data.get("questions", None)
        if questions_data is not None:
            existing_q_ids = [q.id for q in instance.questions.all()]
            incoming_q_ids = []

            for question_data in questions_data:
                variants_data = question_data.pop("variants", [])
                q_id = question_data.get("id", None)

                if q_id and q_id in existing_q_ids:
                    question = Questions.objects.get(id=q_id, quiz=instance)
                    for attr, value in question_data.items():
                        setattr(question, attr, value)
                    question.save()
                else:
                    question = Questions.objects.create(quiz=instance, **question_data)
                incoming_q_ids.append(question.id)

                # Variants update/create/delete
                existing_v_ids = [v.id for v in question.variants.all()]
                incoming_v_ids = []

                for variant_data in variants_data:
                    v_id = variant_data.get("id", None)
                    if v_id and v_id in existing_v_ids:
                        variant = Variant.objects.get(id=v_id, question=question)
                        for attr, value in variant_data.items():
                            setattr(variant, attr, value)
                        variant.save()
                    else:
                        variant = Variant.objects.create(question=question, **variant_data)
                    incoming_v_ids.append(variant.id)

                # Delete removed variants
                for variant in question.variants.all():
                    if variant.id not in incoming_v_ids:
                        variant.delete()

            # Delete removed questions
            for question in instance.questions.all():
                if question.id not in incoming_q_ids:
                    for variant in question.variants.all():
                        variant.delete()
                    question.delete()

        return instance