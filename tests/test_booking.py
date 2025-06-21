import allure
import pytest
import requests
import jsonschema
from core.models.booking import BookingResponse
from tests.schemas.booking_schema import BOOKING_SCHEMA
from pydantic import ValidationError


@allure.feature('Test Booking')
@allure.story('Create Booking')
class TestCreateBooking:
    def test_create_booking_random_data(self, create_booking, generate_random_booking_data):
        ''' Это тест который я написл  самостоятельно до урока с pydantic '''
        with allure.step("Проверка структуры ответа бронирования"):
            jsonschema.validate(create_booking, BOOKING_SCHEMA)

        with allure.step("Проверка соответствия данных запроса и ответа"):
            booking = create_booking['booking']
            assert booking['firstname'] == generate_random_booking_data['firstname'], "Firstname не совпадает"
            assert booking['lastname'] == generate_random_booking_data['lastname'], "Lastname не совпадает"
            assert booking['totalprice'] == generate_random_booking_data['totalprice'], "Total price не совпадает"
            assert booking['depositpaid'] == generate_random_booking_data['depositpaid'], "Deposit paid не совпадает"
            assert booking['bookingdates'] == generate_random_booking_data['bookingdates'], "Booking dates не совпадают"
            assert booking['additionalneeds'] == generate_random_booking_data[
                'additionalneeds'], "Additional needs не совпадают"

    @allure.story('Positive: creating booking with custom data')
    def test_create_booking_with_custom_data(self, api_client):
        ''' Этот тест копия кода после  урока с pydantic '''

        booking_data = {
            "firstname": "Ivan",
            "lastname": "Ivanovich",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-02-01",
                "checkout": "2025-02-10"
            },
            "additionalneeds": "Dinner"
        }

        response = api_client.create_booking(booking_data)

        try:
            BookingResponse(**response)
        except ValueError as e:
            raise ValidationError(f'response validation errpor {e}')

    @allure.story('Positive: creating booking without custom additional needs')
    def test_create_booking_without_additional_needs(self, api_client):

        booking_data = {
            "firstname": "Ivan",
            "lastname": "Ivanovich",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-02-01",
                "checkout": "2025-02-10"
            }
        }

        response = api_client.create_booking(booking_data)

        try:
            BookingResponse(**response)
        except ValueError as e:
            raise ValidationError(f'response validation errpor {e}')

    @allure.story('Negative: creating booking without required field - firstname ')
    def test_create_booking_without_firstname(self, api_client):
        booking_data = {
            "lastname": "Ivanovich",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-02-01",
                "checkout": "2025-02-10"
            }
        }

        try:
            api_client.create_booking(booking_data)
            assert False, "Ожидалась ошибка HTTP 500"
        except requests.exceptions.HTTPError as e:
            assert e.response.status_code == 500, f"Ожидался статус 500, получен {e.response.status_code}"


    @allure.story('Negative: creating booking without required field - firstname ')
    def test_create_booking_without_body(self, api_client):
        booking_data = {}

        try:
            api_client.create_booking(booking_data)
            assert False, "Ожидалась ошибка HTTP 500"
        except requests.exceptions.HTTPError as e:
            assert e.response.status_code == 500, f"Ожидался статус 500, получен {e.response.status_code}"
