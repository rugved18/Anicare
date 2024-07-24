from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import AnimalReportForm
from .models import UserSubmission, AnimalReport
import re

def SubmitNgoForm(request):
    if request.method == 'POST':
        form = AnimalReportForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()

            # Construct Google Maps URL
            latitude = instance.latitude
            longitude = instance.longitude
            google_maps_url = f"https://maps.google.com/maps?q={latitude},{longitude}"

            # Prepare email content
            subject = 'New Animal Report Submitted'
            message = (f'A new animal report has been submitted.\n\nDetails:\n\nName: {instance.name}\n'
                       f'Phone: {instance.phone}\nLocation: {instance.location}\nDescription: {instance.description}\n'
                       f'Animal Type: {instance.animal_type}\nPriority: {instance.priority}\n\n'
                       f'Latitude: {instance.latitude}\nLongitude: {instance.longitude}\n\n'
                       f'Please check the admin panel for more details.\n\nGoogle Maps Location: {google_maps_url}')
            from_email = 'aanicaree@gmail.com'
            recipient_list = ['rugvedkulk2003@gmail.com',]

            # Send email
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                return JsonResponse({'message': 'Form submitted successfully!'})
            except Exception as e:
                return JsonResponse({'message': f'Failed to send email: {str(e)}'}, status=500)

        else:
            errors = form.errors.as_json()
            print(errors)  # Print errors to console for debugging
            return JsonResponse({'message': 'Form submission failed.', 'errors': errors}, status=400)

    else:
        form = AnimalReportForm()  # Create a new form instance for GET requests

    return render(request, 'NGO-Form.html', {'form': form})
def user_page(request):
    send = False  # Flag to track if email was sent successfully
    if request.method == 'POST':
        form = AnimalReportForm(request.POST, request.FILES)
        if form.is_valid():
            # If the form is valid, save the submission to the database
            instance = form.save(commit=False)
            # Additional processing if needed before saving
            instance.save()

            # Example of sending email to admin (optional)
            send = True  # Set to True if email sending is successful
        else:
            # Handle form errors if needed
            pass

    else:
        form = AnimalReportForm()

    return render(request, 'user_page.html', {'form': form, 'send': send})

def admin_page(request):
    animal_reports = AnimalReport.objects.all()
    return render(request, 'admin.html', {'animal_reports': animal_reports})

def landing_page(request):
    context = {
        'offerBanner1': '/static/LandingImages/offerBanner1.jpg',
        'offerBanner2': '/static/LandingImages/offerBanner2.jpg',
        'offerBanner3': '/static/LandingImages/offerBanner3.jpg',
        'ctaBg': '/static/LandingImages/ctaBg.jpg',
        'footerBg': '/static/LandingImages/footerBg.jpg',
        'heroBanner': '/static/LandingImages/heroBanner.jpg'
    }

    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'LandingPage.html', context)


def redirectToUser(request):
    return redirect('user_page')

def redirectToAdmin(request):
    submissions = UserSubmission.objects.all()
    return render(request, 'admin.html', {'submissions': submissions})

def UserLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'LoginPage.html')

def UserRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not re.match(r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            messages.error(request, 'Invalid email format. Please enter a valid email address.')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Account already exists. Please log in.')
            return redirect('UserLogin')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('landing_page')

    return render(request, 'LoginPage.html')

def NgoLink(request):
    form = AnimalReportForm()
    return render(request, 'NGO-Form.html', {'form': form})

def LoadEcommerce(request):
    return render(request, 'EcommercePage.html', {
        'pedigreeImage': '/static/EcommerceImages/pedigree.jpg',
        'P1image': '/static/EcommerceImages/p1.jpeg',
        'P2image': '/static/EcommerceImages/p2.jpeg',
        'P3image': '/static/EcommerceImages/p3.jpeg',
        'P4image': '/static/EcommerceImages/p4.jpeg',
        'Dog1Image': '/static/EcommerceImages/dog1.png',
        'KibblesNbits': '/static/EcommerceImages/kibblesnBits.jpeg',
        'Cat1Image': '/static/EcommerceImages/cat1.jpeg',
        'Cat2Image': '/static/EcommerceImages/cat2.jpeg',
        'Cat5Image': '/static/EcommerceImages/cat3.jpeg',
        'PetOffer': '/static/EcommerceImages/petOffer.png',
        'PetOffer1': '/static/EcommerceImages/petOffer1.png'
    })

def redirectToServices(request):
    return render(request, 'Services.html')
