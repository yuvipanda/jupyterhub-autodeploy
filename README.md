# JupyterHub - Autodeployment for Cluster/Cloud Notebooks
JupyterHub, a multi-user server, manages and proxies multiple instances of the single-user <del>IPython</del> Jupyter notebook server. 
This extension allows a JupyterHub front-end to spawn the JupyterNotebooks into cloud computing infrastructure.

## AWS Auto Deploy Setup Steps

Change into the __autoaws__ folder

    cd autoaws
 
### 0. Optional : Create AWS Access Keys
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

    autoaws$ sudo sed -i '$s/$/\n52.70.194.118 <cluster_name>.omgwtf.in/' /etc/hosts

----------------------

### 3. Kubectl "install":
For Linux:

```
wget https://storage.googleapis.com/kubernetes-release/release/v1.2.4/bin/linux/amd64/kubectl
```

For OS X:

```
wget https://storage.googleapis.com/kubernetes-release/release/v1.2.4/bin/darwin/amd64/kubectl
```

#### Copy kubectl to your path

    autoaws$ chmod +x kubectl
    autoaws$ sudo mv kubectl /usr/local/bin/


----------------------
### 4. Kubectl to Standup Cluster:
    
    autoaws$ kubectl --kubeconfig=<cluster_name>/kubeconfig get nodes
    NAME                        LABELS                                                                                                                                                                                             STATUS
    ip-10-0-0-50.ec2.internal   kubernetes.io/hostname=ip-10-0-0-50.ec2.internal                                                                                                                                                   Ready,SchedulingDisabled
    ip-10-0-0-64.ec2.internal   beta.kubernetes.io/instance-type=m3.medium,failure-domain.beta.kubernetes.io/region=us-east-1,failure-domain.beta.kubernetes.io/zone=us-east-1c,kubernetes.io/hostname=ip-10-0-0-64.ec2.internal   Ready
    
----------------------


## JupyterHub Setup in AWS

### 1. Create the Hub Install into the EC2 instances
```
hub$ kubectl --kubeconfig=../autoaws/mudsa/kubeconfig create -f hub.yaml
hub$ kubectl --kubeconfig=../autoaws/mudsa/kubeconfig create -f config.yaml
```
----------------------
### 2. Download Pods

```
hub$ kubectl --kubeconfig=../autoaws/mudsa/kubeconfig --namespace=jupyter get pods 
NAME        READY     STATUS    RESTARTS   AGE
hub-vi9xy   1/1       Running   0          1m
```

### 2. View Services

```
hub$ kubectl --kubeconfig=../autoaws/mudsa/kubeconfig --namespace=jupyter get svc
NAME         CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
jupyterhub   10.3.0.40                  8000/TCP   13m
```

  * NOTE: Due to bug in AWS(?) the EXTERNAL-IP is not provided.

  * To find the public endpoint of the elastic load balancer:
     * In AWS Dashboard > EC2 Dashboard > Load Balancers
     * Click on Load Balancer and view description
``` 
DNS name: 
a3c48b0dc211311e685a612e85b7665b-1960005297.us-east-1.elb.amazonaws.com (A Record)
```
     * Copy the name and append the port in the Browser to access JupyterHub
```
http://a3c48b0dc211311e685a612e85b7665b-1960005297.us-east-1.elb.amazonaws.com:8000/hub/login
```










--------------
## TO DESTROY AWS CLUSTER

  1. Log into AWS Dashboard > EC2 Dashboard > Load Balancers
  1. Remove the load balancer
  1. Use the Kubernetes to destroy the AWS cluster
```
autoaws$ cd <cluster_name>	
autoaws/<cluster_name>$ ../kube-aws destroy
CloudFormation stack is being destroyed. This will take several minutes
```
----------------------------



