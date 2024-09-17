from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport


def get_service():
    wsdl = 'http://�����?wsdl'
    session = Session()
    session.auth = HTTPBasicAuth('�����', '������')

    client = Client(wsdl, transport=Transport(session=session))
# ������� ������ � wsdl, ������������� ��-�� �������� ����� � �������, ����� ����� ����������� �������� ������ �� �����
    service = client.create_service(
        '���� ������� ���������',
        '���� �� ������� ���������')
    return service


def get_rubric_cl():
    service = get_service()
    return service.GetRubricCl()


def get_appeal_date(date_from, date_to):
    service = get_service()
    return service.GetOgData(date_from, date_to)
