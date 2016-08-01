import json
import responses
from django.apps import apps
from casepro.cases.models import Case
from casepro.test import BaseCasesTest
from .plugin import RegistrationPodConfig, RegistrationPod


class RegistrationPodTest(BaseCasesTest):
    def setUp(self):
        super(RegistrationPodTest, self).setUp()
        self.contact = self.create_contact(self.unicef, 'test_id', "Mother")
        self.msg1 = self.create_message(
            self.unicef, 123, self.contact, "Hello")
        self.case = Case.get_or_open(
            self.unicef, self.user1, self.msg1, "Summary", self.moh)
        self.url = 'http://example.com/registration/?mother_id=' + \
            self.contact.uuid

        self.pod = RegistrationPod(
                apps.get_app_config('family_connect_registration_pod'),
                RegistrationPodConfig({
                    'index': 23,
                    'title': "My registration Pod",
                    'url': "http://example.com/registration/",
                    'token': "test_token",
                    'field_mapping': {
                        "hoh_id": "Head of Household ID",
                        "receiver_id": "Receiver ID",
                        "operator_id": "Operator ID",
                        "language": "Language Preference",
                        "msg_type": "Receives Messages As",
                        "last_period_date": "Date of last period",
                        "msg_receiver": "Message Receiver",
                        "hoh_name": "Head of Household Name",
                        "hoh_surname": "Head of Household Surname",
                        "mama_name": "Mother Name",
                        "mama_surname": "Mother Surname",
                        "mama_id_type": "ID Type",
                        "mama_id_no": "ID Number"
                    }
                }))

    def registration_callback_no_matches(self, request):
        headers = {'Content-Type': "application/json"}
        headers = {'Authorization': "Token test_token"}
        resp = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }
        return (200, headers, json.dumps(resp))

    def registration_callback_one_match(self, request):
        headers = {'Content-Type': "application/json"}
        headers = {'Authorization': "Token test_token"}
        resp = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{
                "id": "b03d0ba0-3baf-4acb-9943-f9ff89ef2412",
                "stage": "postbirth",
                "mother_id": "test_id",
                "validated": True,
                "data": {
                    "hoh_surname": "the builder",
                    "hoh_id": "hoh00001-63e2-4acc-9b94-26663b9bc267",
                    "receiver_id": "hoh00001-63e2-4acc-9b94-26663b9bc267",
                    "operator_id": "hcw00001-63e2-4acc-9b94-26663b9bc267",
                    "language": "eng_UG",
                    "msg_type": "text",
                    "msg_receiver": "head_of_household",
                    "mama_id_no": "12345",
                    "last_period_date": "20150202",
                    "mama_surname": "zin",
                    "mama_id_type": "ugandan_id",
                    "hoh_name": "bob",
                    "mama_name": "sue"},
                "source": 1,
                "created_at": "2016-07-27T15:41:55.102172Z",
                "updated_at": "2016-07-27T15:41:55.102200Z",
                "created_by": 1,
                "updated_by": 1
            }]}
        return (200, headers, json.dumps(resp))

    @responses.activate
    def test_read_data_no_registrations(self):
        # Add callback
        responses.add_callback(
            responses.GET, self.url,
            callback=self.registration_callback_no_matches,
            match_querystring=True, content_type="application/json")

        result = self.pod.read_data({'case_id': self.case.id})

        self.assertEqual(result, {"items": []})

    @responses.activate
    def test_read_data_one_registration(self):
        # Add callback
        responses.add_callback(
            responses.GET, self.url,
            callback=self.registration_callback_one_match,
            match_querystring=True, content_type="application/json")

        result = self.pod.read_data({'case_id': self.case.id})

        self.assertEqual(result, {"items": [
            {"name": "Head of Household Surname", "value": "the builder"},
            {"name": "Head of Household ID", "value": "hoh00001-63e2-4acc-9b94-26663b9bc267"},
            {"name": "Receiver ID", "value": "hoh00001-63e2-4acc-9b94-26663b9bc267"},
            {"name": "Operator ID", "value": "hcw00001-63e2-4acc-9b94-26663b9bc267"},
            {"name": "Language Preference", "value": "eng_UG"},
            {"name": "Receives Messages As", "value": "text"},
            {"name": "Head of Household Name", "value": "bob"},
            {"name": "ID Number", "value": "12345"},
            {"name": "Date of last period", "value": "20150202"},
            {"name": "Mother Surname", "value": "zin"},
            {"name": "ID Type", "value": "ugandan_id"},
            {"name": "Message Receiver", "value": "head_of_household"},
            {"name": "Mother Name", "value": "sue"}]})
