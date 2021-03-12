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

from assessments.models import (
    Component,
    SubComponent,
    Element,
    DefectGroup,
)

# class GetProjectDataView(APIView):
#     permission_classes = (AllowAny, )

#     def post(self, request):
#         data = request.data
#         id = data['projectID']
#         ad = AssessmentData.objects.get(qaa__id=id)
#         qaa = ad.qaa
#         response = []
        
#         components = Component.objects.all()
#         sub_components = SubComponent.objects.all()
#         elements = Element.objects.all()
#         defect_groups = DefectGroup.objects.all()
#         for component in components:
#             c_json = {
#                 'category': component.name,
#                 'type': component.type,
#                 'items': []
#             }
#             for sub_component in sub_components:
#                 if sub_component.component == component:
#                     sc_json = {}
#                     if component.type == 1:
#                         if sub_component.type == 3:
#                             sc_json = {
#                                 'topic': sub_component.name,
#                                 'type': sub_component.type,
#                                 'ptotal': ad.get_ptotal(),
#                                 'ctotal': ad.get_ctotal(),
#                                 'stotal': ad.get_stotal(),
#                                 'subtopics': []
#                             }
#                             for element in elements:
#                                 if element.sub_component == sub_component:
#                                     el_json = {
#                                         'subtopic':element.name,
#                                         'id':element.id,
#                                         'sample':element.no_of_check,
#                                         'checkbox':[]
#                                     }
#                                     for defect_group in defect_groups:
#                                         if defect_group.element == element:
#                                             el_json['checkbox'].append(defect_group.name)
#                                     sc_json['subtopics'].append(el_json)

#                         if sub_component.type == 4:
#                             sc_json = {
#                                 'topic': sub_component.name,
#                                 'type': sub_component.type,
#                                 'id': sub_component.id,
#                                 'sample': sub_component.no_of_check,
#                                 'checkbox': []
#                             }
#                             for defect_group in defect_groups:
#                                 if defect_group.sub_component == sub_component:
#                                     sc_json['checkbox'].append(defect_group.name)
#                     if component.type == 2:
#                         sc_json = {
#                             'topic': sub_component.name,
#                             'subtopics': []
#                         }
#                         for element in elements:
#                             if element.sub_component == sub_component:
#                                 el_json = {
#                                     'subtopic':element.name,
#                                     'id':element.id,
#                                     'sample':element.no_of_check,
#                                     'checkbox':[]
#                                 }
#                                 for defect_group in defect_groups:
#                                     if defect_group.element == element:
#                                         el_json['checkbox'].append(defect_group.name)
#                                 sc_json['subtopics'].append(el_json)
#                     c_json['items'].append(sc_json)
#             response.append(c_json)
        

#         return Response(response)

class GetProjectDataView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data
        id = data['projectID']
        ad = AssessmentData.objects.get(qaa__id=id)
        qaa = ad.qaa
        response = []
        
        components = Component.objects.all()
        sub_components = SubComponent.objects.all()
        elements = Element.objects.all()
        defect_groups = DefectGroup.objects.all()
        for component in components:
            c_json = {
                'category': component.name,
                'type': component.type,
                'items': []
            }
            for sub_component in sub_components:
                if sub_component.component == component:
                    sc_json = {}
                    if component.type == 1:
                        # if sub_component.type == 3 or sub_component.type == 2:
                        #     if sub_component.type == 3:
                        #         sc_json = {
                        #             'topic': sub_component.name,
                        #             'type': sub_component.type,
                        #             'ptotal': ad.get_ptotal(),
                        #             'ctotal': ad.get_ctotal(),
                        #             'stotal': ad.get_stotal(),
                        #             'subtopics': []
                        #         }
                        #     if sub_component.type == 2:
                        #         sc_json = {
                        #             'topic': sub_component.name,
                        #             'type': sub_component.type,
                        #             'items': []
                        #         }
                        #         sc2_json = {
                        #             'topic': sub_component.name,
                        #             'subtopics': []
                        #         }
                        #     for element in elements:
                        #         if element.sub_component == sub_component:
                        #             el_json = {
                        #                 'subtopic':element.name,
                        #                 'id':element.id,
                        #                 'sample':element.no_of_check,
                        #                 'checkbox':[]
                        #             }
                        #             for defect_group in defect_groups:
                        #                 if defect_group.element == element:
                        #                     el_json['checkbox'].append(defect_group.name)
                        #             if sub_component.type == 3:
                        #                 sc_json['subtopics'].append(el_json)
                        #             if sub_component.type == 2:
                        #                 sc2_json['subtopics'].append(el_json)
                        #     if sub_component.type == 2:
                        #         sc_json['items'].append(sc2_json)
                        
                        if sub_component.type == 2:
                            sc_json = {
                                'topic': sub_component.name,
                                'type': sub_component.type,
                                'items': []
                            }
                            sc2_json = {
                                'topic': sub_component.name,
                                'subtopics': []
                            }
                            for element in elements:
                                if element.sub_component == sub_component:
                                    el_json = {
                                        'subtopic':element.name,
                                        'id':element.id,
                                        'sample':element.no_of_check,
                                        'checkbox':[]
                                    }
                                    for defect_group in defect_groups:
                                        if defect_group.element == element:
                                            el_json['checkbox'].append(defect_group.name)
                                    sc2_json['subtopics'].append(el_json)
                            sc_json['items'].append(sc2_json)

                        if sub_component.type == 3:
                            sc_json = {
                                'topic': sub_component.name,
                                'type': sub_component.type,
                                'ptotal': ad.get_ptotal(),
                                'ctotal': ad.get_ctotal(),
                                'stotal': ad.get_stotal(),
                                'subtopics': []
                            }
                            for element in elements:
                                if element.sub_component == sub_component:
                                    el_json = {
                                        'subtopic':element.name,
                                        'id':element.id,
                                        'sample':element.no_of_check,
                                        'checkbox':[]
                                    }
                                    for defect_group in defect_groups:
                                        if defect_group.element == element:
                                            el_json['checkbox'].append(defect_group.name)
                                    sc_json['subtopics'].append(el_json)
                            for element in elements:
                                if element.sub_component == sub_component:
                                    el_json = {
                                        'subtopic':element.name,
                                        'id':element.id,
                                        'sample':element.no_of_check,
                                        'checkbox':[]
                                    }
                                    for defect_group in defect_groups:
                                        if defect_group.element == element:
                                            el_json['checkbox'].append(defect_group.name)
                                    sc_json['subtopics'].append(el_json)

                        # if sub_component.type == 4:
                        #     sc_json = {
                        #         'topic': sub_component.name,
                        #         'type': sub_component.type,
                        #         'id': sub_component.id,
                        #         'sample': sub_component.no_of_check,
                        #         'checkbox': []
                        #     }
                        #     for defect_group in defect_groups:
                        #         if defect_group.sub_component == sub_component:
                        #             sc_json['checkbox'].append(defect_group.name)
                    if component.type == 2:
                        sc_json = {
                            'topic': sub_component.name,
                            'subtopics': []
                        }
                        for element in elements:
                            if element.sub_component == sub_component:
                                el_json = {
                                    'subtopic':element.name,
                                    'id':element.id,
                                    'sample':element.no_of_check,
                                    'checkbox':[]
                                }
                                for defect_group in defect_groups:
                                    if defect_group.element == element:
                                        el_json['checkbox'].append(defect_group.name)
                                sc_json['subtopics'].append(el_json)
                    c_json['items'].append(sc_json)
            response.append(c_json)
        

        return Response(response)

import json

class SyncView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        # Request Data
        data = request.data
        result1 = data['result1']
        result2 = data['result2']
        photos = data['photos']
        partners = data['partner']
        projectID = data['projectID']
        assessorName = data['assessorName']
        assessorId = data['assessorId']
        coordinate = data['coordinate']
        print(result1)
        print(result2)
        # print(partners)
        # print(projectID)
        # print(assessorName)
        # print(assessorId)
        # print(coordinate)
        # str(data)

        # print(type(result1))
        # for result in json.loads(result1):
        #     id = result['id']
        #     id_qaa = id.split('_', 1)[0]
        #     print(id_qaa)
        #     # id = result.id
