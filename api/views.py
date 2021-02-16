from django.urls import path, include
from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.http import HttpResponse

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend

# Models
from assessments.models import QlassicAssessmentApplication
from projects.models import ProjectInfo
from users.models import CustomUser

from .serializers import *

## REST
# ViewSets define the view behavior.
@permission_classes(IsAuthenticated)
class QlassicScoreViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = QlassicAssessmentApplication.objects.all()
    serializer_class = QlassicScoreSerializer
    

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'qaa_number',
        'created_date'
    ]
    def get_permissions(self):
        # permission_classes = [AllowAny] # AllowAny IsAuthenticated
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    
    
    def get_queryset(self):
        queryset = QlassicAssessmentApplication.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Company.objects.none()
        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = User.objects.all()
            else:
                queryset = User.objects.filter(company=company.id)
        """
        return queryset    

class QlassicInformationViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = QlassicAssessmentApplication.objects.all()
    serializer_class = QlassicInformationSerializer
    def get_permissions(self):
        # permission_classes = [AllowAny] # AllowAny IsAuthenticated
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    
    
    def get_queryset(self):
        queryset = QlassicAssessmentApplication.objects.all()
        return queryset    


class ProjectInfoViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ProjectInfo.objects.all()
    serializer_class = ProjectInfoSerializer
    def get_permissions(self):
        # permission_classes = [AllowAny] # AllowAny IsAuthenticated
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    
    
    def get_queryset(self):
        queryset = ProjectInfo.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Company.objects.none()
        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = User.objects.all()
            else:
                queryset = User.objects.filter(company=company.id)
        """
        return queryset    


class UserViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        # permission_classes = [AllowAny] # AllowAny IsAuthenticated
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]    
    
    def get_queryset(self):
        queryset = CustomUser.objects.all()

        """
        if self.request.user.is_anonymous:
            queryset = Company.objects.none()
        else:
            user = self.request.user
            company_employee = CompanyEmployee.objects.filter(employee=user)
            company = company_employee[0].company
            
            if company.company_type == 'AD':
                queryset = User.objects.all()
            else:
                queryset = User.objects.filter(company=company.id)
        """
        return queryset    

## SOAP
# import zeep
# from zeep import Client

# header = zeep.xsd.Element(
#             'soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"',
#             zeep.xsd.ComplexType([
#                 zeep.xsd.Element(
#                     'UsernameToken',
#                     zeep.xsd.ComplexType([
#                         zeep.xsd.Element('Username',zeep.xsd.String()),
#                         zeep.xsd.Element('Password',zeep.xsd.String()),
#                     ])
#                 ),
#                 zeep.xsd.Element(
#                     'ServiceAccessToken',
#                     zeep.xsd.ComplexType([
#                         zeep.xsd.Element('AccessLicenseNumber',zeep.xsd.String()),
#                     ])
#                 ),
#             ])
#         )
# headers = {'content-type': 'text/xml'}
# body = """
# <?xml version="1.0" encoding="utf-8"?>
# <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
#   <soap12:Body>
#     <CreateReceipt xmlns="http://tempuri.org/">
#       <obj>
#         <ReceiptCode>string</ReceiptCode>
#         <InvoiceCode>string</InvoiceCode>
#         <Category>string</Category>
#         <PayAmount>double</PayAmount>
#         <Description>string</Description>
#         <VIPId>string</VIPId>
#         <TransactionRef>string</TransactionRef>
#         <TransactionResult>string</TransactionResult>
#         <ErrorMessage>string</ErrorMessage>
#         <BranchCode>string</BranchCode>
#         <ModuleCode>string</ModuleCode>
#       </obj>
#     </CreateReceipt>
#   </soap12:Body>
# </soap12:Envelope>
# """

# ### Admin - Application Module ###
# def soap_hello_world(request):
#     wsdl = 'http://202.171.33.96/Financeservice/?wsdl'
#     print(header)
#     client = Client(wsdl)

#     response = requests.post(wsdl,data=body,headers=headers)

#     # result = client.service.Search(**request_data, _soapheaders=header_value)
#     return HttpResponse('SOAP')

# from .soap.create_transaction import create_transaction

# def test_create_transaction(request):
#     response = create_transaction(request, 1000, 6, 'QLC', '10001', request.user)
#     print(response.Code)
#     return HttpResponse(str(response))