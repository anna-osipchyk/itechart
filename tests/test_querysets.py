from rest_framework.reverse import reverse
from rest_framework import test
import pytest
from users.models import Employee, PersonalData
from companies.models import Bank, Company


@pytest.fixture(autouse=True)
def api_client():
    return test.APIClient()


@pytest.mark.django_db()
@pytest.fixture
def test_create_bank_and_company():
    # import pdb;
    # pdb.set_trace()
    kwargs = {'name': 'bank', 'web_site': 'https://djbook.ru/rel1.9/ref/models/instances.html',
              'email': 'bank1@gmail.com'}
    bank = Bank.objects.create(**kwargs)
    kwargs = {'name': 'cum', 'web_site': 'https://djbook.ru/rel1.9/ref/models/instances.html', 'email': '1@gmail.com',
              'post_index': 1}
    company = Company.objects.create(**kwargs)
    company.bank.add(bank)
    company.id = 1
    company.save()
    yield company, bank


@pytest.mark.django_db(transaction=True)
@pytest.fixture
def test_create_superuser(test_create_bank_and_company):
    user = {'username': 'user2', 'email': 'user2@gmail.com', 'password': 'user2'}
    user1 = Employee(**user)
    user1.set_password(user['password'])
    user1.save()
    profile = PersonalData(employee=user1, salary=10, date_of_birth='2000-01-01', home_address='Minsk')
    profile.save()
    yield user1, user['password']


@pytest.mark.django_db
@pytest.fixture
def test_create_user(test_create_bank_and_company):
    user = {'username': 'user1', 'email': 'user1@gmail.com', 'password': 'user1', 'company_id': 1}
    user1 = Employee(**user)
    user1.set_password(user['password'])
    user1.save()
    profile = PersonalData(employee=user1, salary=10, date_of_birth='2000-01-01', home_address='Minsk')
    profile.save()
    return user1, user['password']


@pytest.mark.django_db(transaction=True)
def test_superuser_login(api_client, test_create_superuser):
    url = reverse('user_login')
    response = api_client.post(url,
                               {'username': test_create_superuser[0].username, 'password': test_create_superuser[1]})
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_user_login(api_client, test_create_user):

    url = reverse('user_login')
    response = api_client.post(url, {'username': test_create_user[0].username, 'password': test_create_user[1]})
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_get_user(api_client, test_create_user, test_create_bank_and_company):

    url = reverse('get-employee')
    response = api_client.get(url)
    assert response.data[0]['id'] == test_create_user[0].id
    assert response.data[0]['company'] == test_create_bank_and_company[0].id


@pytest.mark.django_db(transaction=True)
def test_get_bank(api_client, test_create_bank_and_company):

    url = reverse('banks-list')
    response = api_client.get(url)
    assert response.data[0]['id'] == test_create_bank_and_company[1].id
