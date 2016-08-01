from confmodel import fields
from casepro.cases.models import Case
from casepro.pods import Pod, PodConfig, PodPlugin
import requests


class RegistrationPodConfig(PodConfig):
    url = fields.ConfigText("URL to query for the registration data",
                            required=True)
    token = fields.ConfigText("Authentication token for registration endpoint",
                              required=True)
    field_mapping = fields.ConfigDict(
        "Mapping of field names to what should be displayed for them",
        required=True)


class RegistrationPod(Pod):
    def read_data(self, params):
        # Setup
        url = self.config.url
        token = self.config.token
        mapping = self.config.field_mapping
        session = requests.Session()
        session.headers.update({'Authorization': "Token " + token})
        session.headers.update({'Content-Type': "application/json"})
        case_id = params["case_id"]
        case = Case.objects.get(pk=case_id)

        # Get and format registration response
        r = session.get(url, params={'mother_id': case.contact.uuid})
        response = r.json()
        # TODO: handle error if request fails
        results = response["results"]

        content = {"items": []}
        for result in results:
            for k in mapping:
                if k in result:
                    value = result[k]
                elif k in result["data"]:
                    value = result["data"][k]
                else:
                    value = "Unknown"
                content['items'].append(
                    {"name": mapping[k], "value": value})
        return content


class RegistrationPlugin(PodPlugin):
    label = 'family_connect_registration_pod'
    pod_class = RegistrationPod
    config_class = RegistrationPodConfig
    title = 'Registration Pod'
