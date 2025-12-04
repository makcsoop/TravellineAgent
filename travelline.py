import requests
import pprint
import json
from flask import Flask, request


app = Flask(__name__)

id_test_hotel = 11983
id_work_hotel = 17355

start_date = "2025-12-05"
end_date = "2025-12-08"


headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "X-ApiKey": "5eaf7e43724a2290d1c4b34034ded03a",
}


@app.route("/", methods=["GET"])
def test():
    return {"status": 200}


#вся информация об отеле
#http://127.0.0.1:3000/get_all_info_hotel?hotel_id=17355 <- пример запроса
@app.route("/get_all_info_hotel", methods=["GET"])
def get_info_hotel():
    args = request.args
    hotel_id = args.get("hotel_id")
    response = requests.get(
        "https://ibe.tlintegration.com/ChannelDistributionApi/BookingForm/hotel_info",
        headers=headers,
        params={"language": "ru-ru", "hotels[0].code": hotel_id},
    )
    with open("hotel_all_info.txt", "w", encoding="utf-8") as f:
        pprint.pprint(response.json(), stream=f, width=120, depth=None)
    return response.json()


def get_info_ready_room():
    response = requests.get(
        "https://ibe.tlintegration.com/ChannelDistributionApi/BookingForm/hotel_availability",
        headers=headers,
        params={
            "include_rates": "true",
            "include_transfers": "true",
            "include_all_placements": "true",
            "include_promo_restricted": "true",
            "criterions[0].adults": "1",
            "language": "ru-ru",
            "criterions[0].hotels[0].code": 17355,
            "criterions[0].dates": "2025-12-01;2025-12-08",
            "criterions[0].adults": 0,
        },
    )
    with open("ready_room.txt", "w", encoding="utf-8") as f:
        pprint.pprint(response.json(), stream=f, width=120, depth=None)

    print("Данные сохранены в файл ready_room.txt")
    # print(response.json())


def get_open_room():
    response = requests.get(
        "https://ibe.tlintegration.com/ChannelDistributionApi/BookingForm/hotel_availability_2",
        headers=headers,
        params={
            "criterions[0].adults": "1",
            "include_rates": "true",
            "criterions[0].hotels[0].code": 17355,
            "include_all_placements": "true",
            "criterions[0].dates": "2025-11-24;2025-11-27",
            "language": "ru-ru",
        },
    )
    print(response.json())

#все свободные номера
#http://127.0.0.1:3000/get_free_rooms?hotel_id=17355&end_date=2025-12-08&start_date=2025-12-05  <- пример запроса
@app.route("/get_free_rooms", methods=["GET"])
def get_open_room_2():
    args = request.args
    hotel_id = args.get("hotel_id")
    start_date = args.get("start_date")
    end_date = args.get("end_date")
    response = requests.get(
        "https://ibe.tlintegration.com/ChannelDistributionApi/BookingForm/hotel_offer_availability",
        headers=headers,
        params={
            "include_rates": "true",
            "criterions[0].hotels[0].code": hotel_id,
            "include_transfers": "true",
            "include_promo_restricted": "true",
            "criterions[0].dates": f"{start_date};{end_date}",
            "language": "ru-ru",
        },
    )
    with open("hotel_info.txt", "w", encoding="utf-8") as f:
        pprint.pprint(response.json(), stream=f, width=120, depth=None)

    return response.json()


def get_all_time_reservation_settings():
    response = requests.get(
        "https://ibe.tlintegration.com/ChannelDistributionApi/BookingForm/booking_form_settings",
        headers=headers,
        params={"criterions[0].hotels[0].code": 17355},
    )
    print(response.json())


def get_all_info_reservation_room():
    response = requests.get(
        "https://ibe.tlintegration.com/ChannelDistributionApi/BookingForm/room_type_availability",
        headers=headers,
        params={
            "criterions[0].adults": "1",
            "include_rates": "true",
            "criterions[0].hotels[0].code": 17355,
            "include_all_placements": "true",
            "criterions[0].dates": "2025-11-24;2025-11-27",
            "language": "ru-ru",
        },
    )
    print(response.json())


def create_reservation():
    url = "https://ibe.tlintegration.com/ApiWebDistribution/BookingForm/hotel_reservation_2"

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    settings = {
"language": "ru-ru",
    "hotel_reservations": [
        {
            "hotel_ref": {
                "code": "11983"
            },
            "room_stays": [
                {
                    "stay_dates": {
                        "start_date": "2025-12-05 16:00:00",
                        "end_date": "2025-12-08 14:00:00"
                    },
                    "room_types": [
                        {
                            "code": "82751",
                            "placements": [
                                {
                                    "index": 0,
                                    "kind": "adult",
                                    "code": "173229"
                                }
                            ],
                            "preferences": []
                        }
                    ],
                    "rate_plans": [
                        {
                            "code": "439601"
                        }
                    ],
                    "guest_count_info": {
                        "guest_counts": [
                            {
                                "count": 1,
                                "age_qualifying_code": "adult",
                                "placement_index": 1
                            }
                        ]
                    },
                    "services": [],
                    "guests": [
                        {
                            "first_name": "Иван",
                            "middle_name": "Иванович",
                            "last_name": "Иванов",
                            "placement": {
                                "index": 0
                            },
                            "citizenship": "RUS"
                        }
                    ]
                }
            ],
            "transfers": [],
            "services": [],
            "number": "11111111-11983-11111111111",
            "verification": {
                "cancellation_code": "AABBCC"
            },
            "guarantee": {
                "code": "73851",
                "success_url": "https://ibe.tlintegration.com/booking2/hotel/index.html?path=%2Fs%2Fpayment%2Fsuccess&language=ru&env=prod&isProdEnv=true&r=0.7750535679299602",
                "decline_url": "https://ibe.tlintegration.com/booking2/hotel/index.html?path=%2Fs%2Fpayment%2Ffailure&language=ru&env=prod&isProdEnv=true&r=0.5275001621896225"
            },
            "customer": {
                "first_name": "Иван",
                "middle_name": "Иванович",
                "last_name": "Иванов",
                "comment": "",
                "confirm_sms": True,
                "subscribe_email": True,
                "contact_info": {
                    "phones": [
                        {
                            "phone_number": "+79101286517"
                        }
                    ],
                        
                    "emails": [
                        {
                            "email_address": "ivanov@test.mail"
                        }
                    ]
                }
            }
        }
    ],
    "currency": "RUB",
    "include_extra_stay_options": False,
    "point_of_sale": {
        "source_url": "https://b.tlintegration.com/?hotel=11983",
        "integration_key": "TL-INT-travelline.booking"
    }
    }

    try:
        response = requests.post(url, headers=headers, json=settings, timeout=30)

        print("Status Code:", response.status_code)
        print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

# get_info_ready_room()
# create_reservation()
#get_open_room_2(id_test_hotel, start_date, end_date)
#create_reservation()
#create_reservation()
#get_info_hotel()

if __name__ == '__main__':
    app.run(port=3000, host='127.0.0.1')