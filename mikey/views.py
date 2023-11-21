from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer
from django.shortcuts import get_object_or_404
from .models import Register  # Assurez-vous d'importer votre modèle
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from .models import Comment # Assurez-vous d'importer YourPostModel
import logging
from rest_framework.generics import RetrieveUpdateDestroyAPIView

logger = logging.getLogger(__name__)

# ... (other imports)

@api_view(['GET', 'POST'])
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            pseudo = request.data.get('pseudo')
            email = request.data.get('email')
            password = request.data.get('password')
            confirm_passwd = request.data.get('confirm_passwd')
            
            # Hash the password before saving it
            hashed_password = make_password(password)

            # Vérifier si les mots de passe correspondent
            if password != confirm_passwd:
                return JsonResponse({'message': 'Les mots de passe ne correspondent pas.'}, status=400)

            # Créer l'objet Register seulement si les mots de passe correspondent
            regist = Register.objects.create(pseudo=pseudo, email=email, password=hashed_password, confirm_passwd=confirm_passwd)

            return JsonResponse({'message': 'Votre inscription s\'est bien passée'}, status=201)
        except IntegrityError:
            return JsonResponse({'message': 'Erreur lors de l\'insertion des données'}, status=400)
    elif request.method == 'GET':
        regist = Register.objects.all()
        data = {
            'members': list(regist.values())
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'message': 'Méthode de requête non valide!'}, status=400)

@api_view(['POST'])
@csrf_exempt
def login_auth(request):
    if request.method == 'POST':
        pseudo = request.data.get('pseudo')
        password = request.data.get('password')
        email = request.data.get('email')

        try:
            user = Register.objects.get(pseudo=pseudo)

            # Use check_password to compare hashed password
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return JsonResponse({'message': 'Connexion réussie'})
            else:
                return JsonResponse({'message': 'Identifiants invalides'}, status=401)
        except Register.DoesNotExist:
            return JsonResponse({'message': 'L\'utilisateur n\'existe pas ou identifiants invalides'}, status=400)

@api_view(['PATCH'])
@csrf_exempt
def updatephoto(request, user_id):
    if request.method == 'PATCH':
        profile_picture = request.data.get('profile_picture')

        try:
            user = Register.objects.get(id=user_id)
        except Register.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Update the user's profile picture
        user.profile_picture = profile_picture
        user.save()

        return JsonResponse({'message': 'Profile picture updated successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


class CommentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            pseudo_id = kwargs.get('pseudo_id')
            pseudo = get_object_or_404(Register, pk=pseudo_id)
            data = request.data.copy()
            data['pseudo'] = pseudo.id  # Assuming the 'pseudo' field is an ForeignKey in Comment model
            print('Request data',data)
            serializer = CommentSerializer(data=data)

            if serializer.is_valid():
                # Explicitly set the pseudo field before saving
                serializer.validated_data['pseudo'] = pseudo
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
       
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'

    def perform_update(self, serializer):
        # Vous pouvez ajouter une logique supplémentaire avant de sauvegarder la mise à jour
        serializer.save()

    def perform_destroy(self, instance):
        # Vous pouvez ajouter une logique supplémentaire avant de supprimer l'instance
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)