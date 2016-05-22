import os

c.JupyterHub.hub_ip = '127.0.0.1'
c.JupyterHub.ip = '0.0.0.0'

c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

c.JupyterHub.db_url = os.environ['JPY_DB_URL']
c.JupyterHub.db_kwargs = {
    'pool_recycle': 60  # Do not keep connections for more than one minute
}

# Until we get DNS reliably working
c.KubeSpawner.kube_api_endpoint = 'https://%s:443' % os.environ['KUBERNETES_SERVICE_HOST']
c.KubeSpawner.kube_ca_path = False


c.KubeSpawner.start_timeout = 60 * 5  # First pulls can be really slow

c.KubeSpawner.hub_ip_connect = '%s:%s' % (os.environ['JUPYTERHUB_SERVICE_HOST'], os.environ['JUPYTERHUB_SERVICE_PORT'])

mem_limit = os.environ.get('JPY_SINGLEUSER_MEMLIMIT', '2Gi')
c.KubeSpawner.mem_limit  = mem_limit
c.KubeSpawner.mem_request = mem_limit
