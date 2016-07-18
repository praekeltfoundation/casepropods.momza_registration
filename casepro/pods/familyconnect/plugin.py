from casepro.pods import Pod, PodConfig, PodPlugin


class FamilyConnectPodConfig(PodConfig):
    pass


class FamilyConnectPod(Pod):
    def read_data(self, params):
        pass


class FamilyConnectPlugin(PodPlugin):
    label = 'family_connect_pod'
    pod_class = FamilyConnectPod
    config_class = FamilyConnectPodConfig
    title = 'Family Connect Pod'
