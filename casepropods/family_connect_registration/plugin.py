from confmodel import fields
from casepro.cases.models import Case
from casepro.pods import Pod, PodConfig, PodPlugin
import requests


class RegistrationPodConfig(PodConfig):
    url = fields.ConfigText("URL to query for the registration data",
                            required=True)
    token = fields.ConfigText("Authentication token for registration endpoint",
                              required=True)


class RegistrationPod(Pod):
    def read_data(self, params):
        # Setup
        url = self.config.url
        token = self.config.token
        session = requests.Session()
        session.headers.update({'Authorization': "Token " + token})
        session.headers.update({'Content-Type': "application/json"})
        case_id = params["case_id"]
        case = Case.objects.get(pk=case_id)

        # Get and format registration response
        r = session.get(url, params={'mother_id': case.contact.uuid})
        response = r.json()
        content = {"items": []}
        for reg in response["results"]:
            for k in reg:
                if k != "data":
                    content['items'].append({"name": k, "value": reg[k]})
        return content


class RegistrationPlugin(PodPlugin):
    label = 'family_connect_registration_pod'
    pod_class = RegistrationPod
    config_class = RegistrationPodConfig
    title = 'Registration Pod'
