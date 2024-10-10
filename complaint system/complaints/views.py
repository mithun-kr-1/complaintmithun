
import torch
from transformers import pipeline
from PIL import Image
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Complaint

# Hugging Face pipelines
sentiment_classifier = pipeline("sentiment-analysis")
image_classifier = pipeline("zero-shot-image-classification")

def submit_complaint(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        complaint_text = request.POST['complaint']
       # Sentiment analysis on the complaint text
        sentiment_result = sentiment_classifier(complaint_text)
        sentiment = sentiment_result[0]['label']
        
        # Image analysis if an image is provided
        image_classification = "No image"
        if 'complaintImage' in request.FILES:
            image = Image.open(request.FILES['complaintImage'])
            candidate_labels = ["cleanliness", "security", "emergency", "business", "errors"]
            image_result = image_classifier(image, candidate_labels=candidate_labels)
            image_classification = image_result[0]['label']
        
        # Save complaint to database
        complaint = Complaint(
            name=name,
            email=email,
            complaint_text=complaint_text,
            sentiment=sentiment,
            image_classification=image_classification,
        )
        complaint.save()
        return redirect('home')  # Redirect to the admin dashboard after submission

    return render(request, 'submit_complaint.html')

def view_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    return render(request, 'view_complaint.html', {'complaint': complaint})

def admin_dashboard(request):
    complaints = Complaint.objects.all()
    return render(request, 'admin_dashboard.html', {'complaints': complaints})


def home(request):
    return render(request, 'home.html')

def officerlogin(request):
    if request.method == 'POST':
        # handle the login logic here (authentication, etc.)
        # if login successful:
        return redirect('admin_dashboard')  # Redirect to admin_dashboard after successful login
    return render(request, 'officerlogin.html')  # Render the officer login page for GET requests





def resolve_complaint(request, complaint_id):
    if request.method == 'POST':
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.resolved = True
        complaint.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})








from django.shortcuts import render, redirect
from .models import Feedback

def feedback_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        location = request.POST['location']
        rating = request.POST['rating']
        feedback_quality = request.POST['feedback']

        # Save feedback to the database
        feedback = Feedback(
            name=name,
            email=email,
            location=location,
            rating=rating,
            feedback_quality=feedback_quality,
        )
        feedback.save()
        
        return redirect('home')  

    return render(request, 'feedback_form.html')



