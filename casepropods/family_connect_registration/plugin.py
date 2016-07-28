from casepro.pods import Pod, PodConfig, PodPlugin


class RegistrationPodConfig(PodConfig):
    pass


class RegistrationPod(Pod):
    def read_data(self, params):
        pass


class RegistrationPlugin(PodPlugin):
    name = 'casepropods.family_connect_registration'
    label = 'family_connect_registration_pod'
    pod_class = RegistrationPod
    config_class = RegistrationPodConfig
    title = 'Registration Pod'
