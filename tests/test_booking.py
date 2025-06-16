import allure
import pytest
import requests
import jsonschema

from tests.schemas.booking_schema import BOOKING_SCHEMA


@allure.feature('Test Booking')
@allure.story('Create Booking')
def test_create_booking(create_booking, generate_random_booking_data):
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
