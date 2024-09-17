from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport


def get_service():
    wsdl = 'http://адрес?wsdl'
    session = Session()
    session.auth = HTTPBasicAuth('логин', 'пароль')

    client = Client(wsdl, transport=Transport(session=session))
# ѕодмена адреса в wsdl, потребовалась из-за проброса порта с сервера, чтобы иметь возможность показать проект на сдаче
    service = client.create_service(
        'путь который подмен€ем',
        'путь на который подмен€ем')
    return service


def get_rubric_cl():
    service = get_service()
    return service.GetRubricCl()


def get_appeal_date(date_from, date_to):
    service = get_service()
    return service.GetOgData(date_from, date_to)
