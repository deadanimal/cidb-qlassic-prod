from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep.settings import Settings

from zeep.plugins import HistoryPlugin

from django.http import HttpResponse

import json
import requests
import xmltodict
import datetime

create_transaction_wsdl = "http://202.171.33.96/Financeservice/?wsdl"
payment_gateway_url = "http://202.171.33.96:8085/Payment/MakePayment"
# payment_gateway_url = "http://202.171.33.96/securepay/Listener.aspx"

# Production
# create_transaction_wsdl = "http://202.171.33.96/Financeservice/?wsdl"
# payment_gateway_url = "https://www.icims.cidb.gov.my:8085/Payment/MakePayment"

def test_create_transaction(request):

    # payload = {
    #     "token": "tLh-KkVgm8yUgA30ulJNFA",
    #     "data": {
    #     "name": "nameFirst",
    #     "email": "internetEmail",
    #     "phone": "phoneHome",
    #     "_repeat": 300
    #     }
    # };

    # r = requests.post("http://167.71.199.123:8080/getEmployee.php", json = payload)
    # return json.loads(r.content);

    wsdl = "http://202.171.33.96/Financeservice/?wsdl"

    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))
    
    
    history = HistoryPlugin()
    client = Client(wsdl,plugins=[history])
    request_data = {
        'obj': {
            'Id':'1',
            'SubType':'CIMS',
            'Category':'PROFORMA INVOICE',
            'SubCategory':'Third Party System - QLASSIC Portal',
            'SourceType':'Third Party System - QLASSIC Portal',
            'CustomerId': '1004',
            'CreatedDate': datetime.datetime.now().strftime("%Y-%m-%d"),
            'ReceiptDate': datetime.datetime.now().strftime("%Y-%m-%d"),
            'TransactionDate': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
            'DueDate': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
            'Description': 'This is test',
            'Amount': 1000,
            'AmountDec': 2,
            'DiscountAmount': 0,
            'Tax': 0,
            'TaxDec': 2,
            'SMISRefId': 'Ref001',
            'CreatedBy': 'Admin',
            'CustomerName': 'Admin',
            'address': 'Add',
            'address1': 'Add1',
            'address2': 'Add2',
            'city': 'Shah ',
            'state': 'Selangor',
            'zipCode': '40000',
            'BranchCode': 'SL',
            'ModuleCode': 'B4',
            'ComId': 0,
            'PaymentTerm': '1',
            'isWriteOff': False,
            'isRefund': False,
            'isDoubtfulDebts': False,
            'Items' : {
                'TransactionDetail': [{
                    'Id': '1',
                    'DiscountAmount': 0,
                    'DiscountPer': 0,
                    'KodHasil': 'QLC',
                    'Qty': 1,
                    'QtyAmount': 1000,
                    'QtyAmountDec': 2,
                    'UnitPrice': 1000,
                    'UnitPriceDec': 2,
                    'TaxCode': 'SZ',
                    'TaxPerAmount': 0,
                    'TaxPerAmountDec': 2,
                    'TaxAmount': 0,
                    'TaxAmountDec': 2,
                    'Amount': 1000,
                    'AmountDec': 2,
                    'CMISRefId': 'Ref001',
                    'Description': 'PERMOHONAN PENILAIAN QLASSIC',
                }]
            }
        }
    }

    response = client.service.CreateTransaction(**request_data)
    # print(history.last_sent)
    # print(history.last_received)
    # response_xml = response.content
    # print(response_xml)
    # print(type(response_xml))
    return HttpResponse(str(response))

# def get_employee(request):

#     # payload = {
#     #     "token": "tLh-KkVgm8yUgA30ulJNFA",
#     #     "data": {
#     #     "name": "nameFirst",
#     #     "email": "internetEmail",
#     #     "phone": "phoneHome",
#     #     "_repeat": 300
#     #     }
#     # };

#     # r = requests.post("http://167.71.199.123:8080/getEmployee.php", json = payload)
#     # return json.loads(r.content);

#     wsdl = "http://202.171.33.96/Financeservice/?wsdl"

#     # session = Session()
#     # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

#     # client = Client(wsdl, transport=Transport(session=session),
#     #                 settings=Settings(strict=False, raw_response=True))
    
#     history = HistoryPlugin()
#     client = Client(wsdl,plugins=[history])
#     request_data = {
#         'obj': {
#             'Id':'1',
#             'SubType':'CIMS',
#             'Category':'PROFORMA INVOICE',
#             'SubCategory':'PendaftaranKontraktor',
#             'SourceType':'PendaftaranKontraktor',
#             'CustomerId': '1004',
#             'TransactionDate': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
#             'DueDate': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
#             'Description': 'This is test',
#             'Amount': 20,
#             'AmountDec': 2,
#             'Tax': 0,
#             'TaxDec': 2,
#             'SMISRefId': 'Ref001',
#             'CreatedBy': 'Admin',
#             'CustomerName': 'Admin',
#             'address': 'Add',
#             'address1': 'Add1',
#             'address2': 'Add2',
#             'city': 'Shah ',
#             'state': 'Selangor',
#             'zipCode': '40000',
#             'BranchCode': 'SL',
#             'ModuleCode': 'K1',
#             'ComId': 0,
#             'PaymentTerm': '1',
#             'Items' : {
#                 'TransactionDetail': [{
#                     'Id': '1',
#                     'KodHasil': 'QLC',
#                     'Qty': 1,
#                     'QtyAmount': 20,
#                     'QtyAmountDec': 2,
#                     'UnitPrice': 20,
#                     'UnitPriceDec': 2,
#                     'TaxCode': 'SZ',
#                     'TaxPerAmount': 0,
#                     'TaxPerAmountDec': 2,
#                     'TaxAmount': 0,
#                     'TaxAmountDec': 2,
#                     'Amount': 20,
#                     'AmountDec': 2,
#                     'CMISRefId': 'Ref001',
#                     'Description': 'PERMOHONAN PENILAIAN QLASSIC',
#                 }]
#             }
#         }
#     }

#     response = client.service.CreateTransaction(**request_data)
#     # print(history.last_sent)
#     # print(history.last_received)
#     response_xml = response.content
#     print(response_xml)
#     print(type(response_xml))
#     middleware_response_json = json.loads(
#         json.dumps(xmltodict.parse(response_xml)))
#     return middleware_response_json['soap11:Envelope']['soap11`:Body']['CreateTransactionResponse']

# Create Transaction
def create_transaction(request, amount, tax, kod_hasil, ref_id, user):
    ## Notes
    # KOD HASIL : QLC - assessment, QLC-PUP - training

    wsdl = create_transaction_wsdl

    total_amount = tax + amount
    history = HistoryPlugin()
    client = Client(wsdl,plugins=[history])
    now_date = datetime.datetime.now()
    due_date = now_date + datetime.timedelta(days=30)
    request_data = {
        'obj': {
            'Id':'1',
            'SubType':'CIMS',
            'Category':'PROFORMA INVOICE',
            'SubCategory':'Third Party System - QLASSIC Portal',
            'SourceType':'Third Party System - QLASSIC Portal',
            'CustomerId': user.code_id,
            'CreatedDate': str(now_date.strftime("%Y-%m-%dT%H:%M:%S")),
            'ReceiptDate': str(now_date.strftime("%Y-%m-%dT%H:%M:%S")),
            'TransactionDate': str(now_date.strftime("%Y-%m-%dT%H:%M:%S")),
            'DueDate': str(due_date.strftime("%Y-%m-%dT%H:%M:%S")),
            'Description': 'QLASSIC',
            'Amount': total_amount,
            'AmountDec': 2,
            'DiscountAmount': 0,
            'Tax': tax,
            'TaxDec': 2,
            'SMISRefId': ref_id,
            'CreatedBy': 'Admin',
            'CustomerName': user.name,
            'address': user.address1,
            'address1': user.address2,
            'address2': '',
            'city': user.city,
            'state': user.state,
            'zipCode': user.postcode,
            'BranchCode': 'HQ',
            'ModuleCode': 'B4',
            'ComId': 0,
            'PaymentTerm': '1',
            'isWriteOff': False,
            'isRefund': False,
            'isDoubtfulDebts': False,
            'Items' : {
                'TransactionDetail': [{
                    'Id': '1',
                    'DiscountAmount': 0,
                    'DiscountPer': 0,
                    'KodHasil': kod_hasil,
                    'Qty': 1,
                    'QtyAmount': amount,
                    'QtyAmountDec': 2,
                    'UnitPrice': amount,
                    'UnitPriceDec': 2,
                    'TaxCode': kod_hasil,
                    'TaxPerAmount': tax,
                    'TaxPerAmountDec': 2,
                    'TaxAmount': tax,
                    'TaxAmountDec': 2,
                    'Amount': total_amount,
                    'AmountDec': 2,
                    'CMISRefId': ref_id,
                    'Description': 'PERMOHONAN PENILAIAN QLASSIC',
                }]
            }
        }
    }

    response = client.service.CreateTransaction(**request_data)
    # print(history.last_sent)
    # print(history.last_received)
    # response_xml = response.content
    # print(response_xml)
    # print(type(response_xml))
    return response
