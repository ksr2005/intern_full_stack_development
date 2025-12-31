"""
ELECTRICAL MACHINES Q&A PLATFORM - COMPLETE BACKEND
All-in-one Django application with database models, views, and API integration
PEP 8 Compliant | Well Documented | Production Ready
"""

import pymysql
pymysql.install_as_MySQLdb()

import os
import sys
import requests
import logging
from pathlib import Path

# ============================================================================
# LOAD ENVIRONMENT VARIABLES FIRST
# ============================================================================

env_path = Path(__file__).resolve().parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

def config(key, default=None, cast=None):
    """Simple config function to read environment variables"""
    value = os.environ.get(key, default)
    if cast and value is not None:
        if cast == bool:
            return value.lower() in ('true', '1', 'yes')
        return cast(value)
    return value

# ============================================================================
# DJANGO IMPORTS (Must come after environment setup)
# ============================================================================

from django.core.management import execute_from_command_line
from django.conf import settings

# ============================================================================
# SETTINGS CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent

if not settings.configured:
    settings.configure(
        DEBUG=config('DEBUG', default=True, cast=bool),
        SECRET_KEY=config('SECRET_KEY', default='dev-secret-key-change-in-production'),
        ALLOWED_HOSTS=['*'],
        ROOT_URLCONF=__name__,
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            '__main__',  # Register this script as an app
        ],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': config('DB_NAME', default='electrical_qa_db'),
                'USER': config('DB_USER', default='root'),
                'PASSWORD': config('DB_PASSWORD', default=''),
                'HOST': config('DB_HOST', default='localhost'),
                'PORT': config('DB_PORT', default='3306'),
            }
        },
        STATIC_URL='/static/',
        STATIC_ROOT=BASE_DIR / 'staticfiles',
        LOGIN_REDIRECT_URL='home',
        LOGOUT_REDIRECT_URL='home',
        LOGIN_URL='login',
        LANGUAGE_CODE='en-us',
        TIME_ZONE='Asia/Kolkata',
        USE_I18N=True,
        USE_TZ=True,
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
        HUGGINGFACE_API_KEY=config('HUGGINGFACE_API_KEY', default=''),
    )

# ============================================================================
# SETUP DJANGO - CRITICAL: Must happen before importing models
# ============================================================================

import django
django.setup()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# IMPORT DJANGO COMPONENTS (After django.setup())
# ============================================================================

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages, admin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.urls import path
from django.contrib.auth import views as auth_views


# ============================================================================
# DATABASE MODELS (5 columns each as required)
# ============================================================================

class Question(models.Model):
    """
    Question model - stores user questions about electrical machines.
    Database columns: id, user_id, question_text, category, created_at
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.TextField()
    category = models.CharField(max_length=100, default='General')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = '__main__'  # Explicitly declare app_label
        ordering = ['-created_at']
        db_table = 'questions'

    def __str__(self):
        return f"{self.question_text[:50]}..."


class Answer(models.Model):
    """
    Answer model - stores AI-generated answers.
    Database columns: id, question_id, answer_text, source, confidence_score
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer_text = models.TextField()
    source = models.CharField(max_length=50, default='HuggingFace AI')
    confidence_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = '__main__'  # Explicitly declare app_label
        ordering = ['-created_at']
        db_table = 'answers'

    def __str__(self):
        return f"Answer to: {self.question.question_text[:30]}..."


# ============================================================================
# GROQ/HUGGING FACE AI SERVICE
# ============================================================================


class HuggingFaceAI:
    """Service to interact with Groq API for generating answers."""

    def __init__(self):
        self.groq_key = config('GROQ_API_KEY', default='')
        self.hf_key = settings.HUGGINGFACE_API_KEY

    def get_answer(self, question_text):
        """Generate answer for electrical machines question using Groq API."""

        # Use Groq API (fast and reliable)
        if self.groq_key:
            try:
                groq_url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.groq_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert in electrical machines, motors, transformers, and power systems. Provide clear, accurate, technical answers with examples when helpful."
                        },
                        {
                            "role": "user",
                            "content": question_text
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500,
                    "top_p": 0.9
                }

                logger.info(f"Sending request to Groq API for question: {question_text[:50]}...")

                response = requests.post(
                    groq_url, 
                    headers=headers, 
                    json=payload, 
                    timeout=30
                )

                logger.info(f"Groq API Response Status: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    answer = result['choices'][0]['message']['content'].strip()

                    logger.info(f"Successfully got answer from Groq AI")

                    return {
                        'success': True,
                        'answer': answer,
                        'source': 'Llama 3.1 AI (Groq)',
                        'confidence': 0.95
                    }

                elif response.status_code == 401:
                    logger.error("Groq API: Invalid API key")
                    return {
                        'success': False,
                        'answer': 'API authentication failed. Please check your Groq API key in .env file.',
                        'error': 'Invalid API key'
                    }

                elif response.status_code == 429:
                    logger.error("Groq API: Rate limit exceeded")
                    return {
                        'success': False,
                        'answer': 'Too many requests. Please wait a moment and try again.',
                        'error': 'Rate limit'
                    }

                else:
                    logger.error(f"Groq API Error: {response.status_code} - {response.text}")
                    return {
                        'success': False,
                        'answer': f'API Error (Status {response.status_code}). Please try again.',
                        'error': response.text
                    }

            except requests.exceptions.Timeout:
                logger.error("Groq API: Request timeout")
                return {
                    'success': False,
                    'answer': 'Request timed out. Please try again.',
                    'error': 'Timeout'
                }

            except Exception as e:
                logger.error(f"Groq API Exception: {str(e)}")
                return {
                    'success': False,
                    'answer': f'Error: {str(e)}. Please check your API key and internet connection.',
                    'error': str(e)
                }
        else:
            logger.error("No Groq API key found in environment")
            return {
                'success': False,
                'answer': 'Groq API key is missing. Please add GROQ_API_KEY to your .env file.',
                'error': 'No API key'
            }



# ============================================================================
# FORMS
# ============================================================================

class RegisterForm(UserCreationForm):
    """User registration form with email and name fields."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control'}
        )


class QuestionForm(forms.ModelForm):
    """Form for asking questions about electrical machines."""
    CATEGORIES = [
        ('General', 'General'),
        ('DC Machines', 'DC Machines'),
        ('AC Machines', 'AC Machines'),
        ('Transformers', 'Transformers'),
        ('Induction Motors', 'Induction Motors'),
        ('Synchronous Machines', 'Synchronous Machines'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Question
        fields = ['question_text', 'category']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ask your question about electrical machines here...'
            }),
        }


# ============================================================================
# VIEWS
# ============================================================================

def home(request):
    """Homepage with recent questions and statistics."""
    recent_questions = Question.objects.all()[:10]
    stats = {
        'total_questions': Question.objects.count(),
        'total_users': User.objects.count(),
        'total_answers': Answer.objects.count(),
    }
    return render(request, 'home.html', {
        'recent_questions': recent_questions,
        'stats': stats
    })


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'Welcome {user.username}! Your account has been created.'
            )
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def ask_question(request):
    """Ask a new question and get AI answer."""
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()

            # Get AI answer
            ai_service = HuggingFaceAI()
            result = ai_service.get_answer(question.question_text)

            # Save answer
            Answer.objects.create(
                question=question,
                answer_text=result['answer'],
                source=result.get('source', 'AI'),
                confidence_score=result.get('confidence')
            )

            if result['success']:
                messages.success(
                    request,
                    'Question posted and answered successfully!'
                )
            else:
                messages.warning(
                    request,
                    'Question posted but AI response had issues.'
                )

            return redirect('answer_detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {'form': form})


def question_list(request):
    """List all questions."""
    questions = Question.objects.all()
    return render(request, 'questions.html', {'questions': questions})


def answer_detail(request, pk):
    """View question with answer."""
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    return render(request, 'answer.html', {
        'question': question,
        'answers': answers
    })


# ============================================================================
# ADMIN CONFIGURATION
# ============================================================================

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question model."""
    list_display = ['question_text', 'user', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['question_text']
    date_hierarchy = 'created_at'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin interface for Answer model."""
    list_display = ['question', 'source', 'confidence_score', 'created_at']
    list_filter = ['source', 'created_at']
    date_hierarchy = 'created_at'


# ============================================================================
# URL CONFIGURATION
# ============================================================================

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ask/', ask_question, name='ask_question'),
    path('questions/', question_list, name='question_list'),
    path('answer/<int:pk>/', answer_detail, name='answer_detail'),
]


# ============================================================================
# WSGI APPLICATION
# ============================================================================

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


# ============================================================================
# MANAGEMENT COMMANDS
# ============================================================================

if __name__ == '__main__':
    execute_from_command_line(sys.argv)