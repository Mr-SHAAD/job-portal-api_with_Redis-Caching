from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.cache import cache
from .models import Company, Job, Application
from .serializers import (
    RegisterSerializer, CompanySerializer,
    JobSerializer, ApplicationSerializer
)

# Register
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Account created'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=400)

# Jobs List — Redis Cache ke saath
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def job_list(request):
    if request.method == 'GET':
        # Cache check karo
        cached_jobs = cache.get('all_jobs')
        if cached_jobs:
            return Response({
                'source': 'cache',  # Dikhata hai cache se aaya
                'data': cached_jobs
            })

        # Cache nahi mila — database se lo
        jobs = Job.objects.filter(is_active=True).select_related('company')
        serializer = JobSerializer(jobs, many=True)

        # Cache mein save karo — 5 min ke liye
        cache.set('all_jobs', serializer.data, timeout=300)

        return Response({
            'source': 'database',
            'data': serializer.data
        })

    # POST — Naya job create karo
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'Login karo'}, status=401)

        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(posted_by=request.user)

            # Cache clear karo — naya job aaya
            cache.delete('all_jobs')

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Job Detail
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def job_detail(request, pk):
    try:
        job = Job.objects.get(id=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job nahi mili'}, status=404)

    if request.method == 'GET':
        # Individual job bhi cache karo
        cache_key = f'job_{pk}'
        cached = cache.get(cache_key)
        if cached:
            return Response({'source': 'cache', 'data': cached})

        serializer = JobSerializer(job)
        cache.set(cache_key, serializer.data, timeout=600)
        return Response({'source': 'database', 'data': serializer.data})

    if request.method == 'PUT':
        if job.posted_by != request.user:
            return Response({'error': 'Permission nahi'}, status=403)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('all_jobs')
            cache.delete(f'job_{pk}')
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        if job.posted_by != request.user:
            return Response({'error': 'Permission nahi'}, status=403)
        job.delete()
        cache.delete('all_jobs')
        cache.delete(f'job_{pk}')
        return Response({'message': 'Job delete ho gayi'}, status=204)

# Company Views
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def company_list(request):
    if request.method == 'GET':
        cached = cache.get('all_companies')
        if cached:
            return Response({'source': 'cache', 'data': cached})

        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        cache.set('all_companies', serializer.data, timeout=600)
        return Response({'source': 'database', 'data': serializer.data})

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'Login karo'}, status=401)
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            cache.delete('all_companies')
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Apply for Job
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_job(request, pk):
    try:
        job = Job.objects.get(id=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job nahi mili'}, status=404)

    # Pehle se apply kiya?
    if Application.objects.filter(job=job, applicant=request.user).exists():
        return Response({'error': 'Pehle se apply kiya hai'}, status=400)

    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(job=job, applicant=request.user)
        return Response({'message': 'Apply ho gaya'}, status=201)
    return Response(serializer.errors, status=400)

# My Applications
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user)
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)

# Search Jobs
@api_view(['GET'])
@permission_classes([AllowAny])
def search_jobs(request):
    query = request.query_params.get('q', '')
    location = request.query_params.get('location', '')
    job_type = request.query_params.get('type', '')

    # Search cache key
    cache_key = f'search_{query}_{location}_{job_type}'
    cached = cache.get(cache_key)
    if cached:
        return Response({'source': 'cache', 'data': cached})

    jobs = Job.objects.filter(is_active=True)

    if query:
        jobs = jobs.filter(title__icontains=query) | \
               jobs.filter(skills_required__icontains=query)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    serializer = JobSerializer(jobs, many=True)
    cache.set(cache_key, serializer.data, timeout=120)
    return Response({'source': 'database', 'data': serializer.data})
# Create your views here.
