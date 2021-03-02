from django.shortcuts import render
from django.db.models import Q

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from django_filters.rest_framework import DjangoFilterBackend

from assessments.models import (
    AssignedAssessor, 
    AssessmentData, 
    QlassicAssessmentApplication,
)

from assessments.serializers import (
    AssignedAssessorSerializer,
    AssessmentDataSerializer,
    QlassicAssessmentApplicationSerializer,
)

class AssignedAssessorViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssignedAssessor.objects.all()
    serializer_class = AssignedAssessorSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated] #AllowAny IsAuthenticated
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssignedAssessor.objects.all().filter()
        return queryset    
 
class AssessmentDataViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = AssessmentData.objects.all()
    serializer_class = AssessmentDataSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated] #AllowAny IsAuthenticated
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = AssessmentData.objects.all().filter()
        return queryset

class QlassicAssessmentApplicationViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = QlassicAssessmentApplication.objects.all()
    serializer_class = QlassicAssessmentApplicationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated] #AllowAny IsAuthenticated
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]    

    
    def get_queryset(self):
        queryset = QlassicAssessmentApplication.objects.all().filter()
        return queryset

class GetProjectDataView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = request.data
        response = {
            'success': serializer['haha'],
        }

        return Response(response)