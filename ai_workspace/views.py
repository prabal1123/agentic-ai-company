from django.http import JsonResponse
from django.views import View
from .models import User, Farm, CropPhoto, CropHealth, HealthRecord
from django.db import transaction

class UserRegistrationView(View):
    def post(self, request):
        data = request.POST
        email = data.get('email')
        if not email:
            return JsonResponse({'error': 'Email required'}, status=400)

        # Simple validation for demo
        if not email.startswith('user.'): 
            return JsonResponse({'error': 'Email must start with user.'}, status=400)

        # Create user
        user = User.objects.create_user(email)
        return JsonResponse({'status': 'success', 'user_id': user.id}, status=201)

class FarmCreationView(View):
    def post(self, request):
        data = request.POST
        name = data.get('name')
        if not name:
            return JsonResponse({'error': 'Farm name required'}, status=400)

        farm = Farm.objects.create(name=name)
        return JsonResponse({'status': 'success', 'farm_id': farm.id}, status=201)

class CropPhotoUploadView(View):
    def post(self, request, farm_id):
        data = request.POST
        image = data.get('image')
        if not image:
            return JsonResponse({'error': 'Image required'}, status=400)

        if not image.content_type.startswith('image/'): 
            return JsonResponse({'error': 'Only image files are allowed'}, status=400)

        with transaction.atomic():
            photo = CropPhoto.objects.create(farm=farm, image=image)
            return JsonResponse({'status': 'success', 'photo_id': photo.id}, status=201)

class HealthRecordView(View):
    def post(self, request, farm_id):
        data = request.POST
        description = data.get('description')
        if not description:
            return JsonResponse({'error': 'Description required'}, status=400)

        health = CropHealth.objects.create(farm=farm, status=description)
        return JsonResponse({'status': 'success', 'health_id': health.id}, status=201)

class HealthHistoryView(View):
    def get(self, request, farm_id):
        health_records = CropHealth.objects.filter(farm=farm_id).order_by('timestamp')
        data = [{'id': record.id, 'status': record.status, 'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M')} for record in health_records]
        return JsonResponse(data, safe=False)