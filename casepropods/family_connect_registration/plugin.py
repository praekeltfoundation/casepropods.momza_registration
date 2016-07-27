from confmodel import fields
from casepro.pods import Pod, PodConfig, PodPlugin


class RegistrationPodConfig(PodConfig):
    url = fields.ConfigText("URL to query for the registration data",
                            required=True)
    token = fields.ConfigText("Authentication token for registration endpoint",
                              required=True)


class RegistrationPod(Pod):
    def read_data(self, params):
        pass


class RegistrationPlugin(PodPlugin):
    label = 'family_connect_registration_pod'
    pod_class = RegistrationPod
    config_class = RegistrationPodConfig
    title = 'Registration Pod'
