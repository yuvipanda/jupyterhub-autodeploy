# JupyterHub - Autodeployment for Cluster/Cloud Notebooks
JupyterHub, a multi-user server, manages and proxies multiple instances of the single-user <del>IPython</del> Jupyter notebook server. 
This extension allows a JupyterHub front-end to spawn the JupyterNotebooks into cloud computing infrastructure.

## AWS Auto Deploy Setup Steps: 
### 0. __Optional__ : Create AWS Access Keys
  * Open Amazon AWS "Your Security Credentials"
  * Click "Create New Access Key"
  * Store Credentials in a home directory, ~/.aws/credentials
-------
    [default]
    aws_access_key_id = <your_access_key_id>
    aws_secret_access_key = <your_secret_access_key>
-------

### 1. Create the Kubernetes Cluster
    autoaws$ python3 run.py <cluster_name>
 * NOTE: Wait patiently! 
    
--------------
####  OUTPUT 

    Success! Created cluster.yaml
    
    Next steps:
    1. (Optional) Edit cluster.yaml to parameterize the cluster.
    2. Use the "kube-aws render" command to render the stack template.
    Success! Stack rendered to stack-template.json.
    
    Next steps:
    1. (Optional) Validate your changes to cluster.yaml with "kube-aws validate"
    2. (Optional) Further customize the cluster by modifying stack-template.json or files in ./userdata.
    3. Start the cluster with "kube-aws up".
    Creating AWS resources. This should take around 5 minutes.
    Success! Your AWS resources have been created:
    Cluster Name:	<cluster_name>
    Controller IP:	52.70.194.118
    
    The containers that power your cluster are now being dowloaded.
    
    You should be able to access the Kubernetes API once the containers finish downloading.
    Cluster Name:	<cluster_name>
    Controller IP:	52.70.194.118

----------------------
  NOTE: You can see your running instances using the AWS Dashboard, EC2 instances, Running Instances

----------------------
### 2. Add an entry to /etc/hosts

    sudo sed -i '$s/$/\n52.70.194.118 <cluster_name>.omgwtf.in/' /etc/hosts

----------------------

### 3. Kubectl "install":
    Link :
[kubectl Guide](http://thockin.github.io/kubernetes/v1.0/docs/getting-started-guides/aws/kubectl.html "kubectl Guide Site")

#### Download the kubectl CLI tool

    wget https://storage.googleapis.com/kubernetes-release/release/v1.0.1/bin/linux/amd64/kubectl

#### Copy kubectl to your path

    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/


----------------------
### 4. Kubectl to Standup Cluster:
    
    $ kubectl --kubeconfig=<cluster_name>/kubeconfig get nodes
    NAME                        LABELS                                                                                                                                                                                             STATUS
    ip-10-0-0-50.ec2.internal   kubernetes.io/hostname=ip-10-0-0-50.ec2.internal                                                                                                                                                   Ready,SchedulingDisabled
    ip-10-0-0-64.ec2.internal   beta.kubernetes.io/instance-type=m3.medium,failure-domain.beta.kubernetes.io/region=us-east-1,failure-domain.beta.kubernetes.io/zone=us-east-1c,kubernetes.io/hostname=ip-10-0-0-64.ec2.internal   Ready
    
----------------------











--------------
## TO DESTROY AWS CLUSTER

    autoaws$ cd <cluster_name>	
    autoaws/<cluster_name>$ ../kube-aws destroy
    CloudFormation stack is being destroyed. This will take several minutes

----------------------------



