# COMPSCI401-Project2

Personal Repo for COMPSCI 401 Project 2, 22SP@DKU

## Project 2: DevOps and Cloud Computing

1. Students will train an ML prediction model using the training.csv dataset.
2. Students will create a public repository to maintain their model and others application specs (Kubernetes YAML file). For each new update in this repository, e.g., a new ML model version, ArgoCD will be capable of updating the deployment using the new configuration.
3. Students will write a Dockerfile to build a container to run the prediction service. The container will be uploaded to a hosting platform.
4. After creating the model, the Git repository, and the Docker image, students will configure the ArgoCD deployment. Students must deploy their services in their own Kubernetes namespace (defined by the login name) and in their own ArgoCD project area (defined by login name plus the suffix **-project**).

> Steps (5) to (8) are performed indirectly when ArgoCD finds a new update in the repository configured in step (4).

5. ArgoCD pulls the Kubernetes specs and subsequent changes to the Git repository.
6. ArgoCD sends a request to Kubernetes to create or update a service.
7. Kubernetes downloads the image from the hosting platform if it is not present in the cluster. If the image is already present, it will only check if it has any update.
8. Kubernetes creates the service in a pod using the resources defined in the YAML file.
9. Once the service is started, students can send requests to their service's address.

### ML Model

Train the model

```bash
python build_model.py
```

### Flask API

Build the Flask API

```
python app.py
```

Test the Flask API

```
curl -X POST 152.3.65.126:5016//api/american -d '{"text": "#covid19 new york"}' -H 'Content-Type: application/json'
```

### Docker Image

Build image

```
docker build -t yufan-model .
```

Run image

```
docker run -it -p 5016:5016 yufan-model python3 app.py
```

Test image

```
curl -X POST 172.17.0.7:5016/api/american -d '{"text": "#covid19 new york"}' -H 'Content-Type: application/json'
```

Push iamge to dockerhub

```
docker images
docker tag 80cc5aef3479 helloyufan/american-predictor:0.2
docker push helloyufan/american-predictor:0.2
```

Pull image from dockerhub

```
docker build . -t docker.io/helloyufan/american-predictor
docker run -p 5016:5016 docker.io/helloyufan/american-predictor python3 app.py
curl -X POST http://172.17.0.7:5016/api/american -d '{"text": "#covid19 new york"}' -H 'Content-Type: application/json'
```

### Kubernetes Deployment and Service

Configure the Kubernetes deployment and service

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get deployments
kubectl get services
```

Test the service

```
curl -X POST http://10.106.204.16:5016/api/american -d '{"text": "#covid19 new york"}' -H 'Content-Type: application/json'
```

### ArgoCD

Open a Web UI

```
ssh -L 8888:127.0.0.1:32535 yz605@vcm-23691.vm.duke.edu
```

Create app

```
argocd app create yufan-american-predictor \
      --repo https://github.com/iambrucez/COMPSCI401-Project2 \
      --path . \
      --project yz605-project \
      --dest-namespace yz605 \
      --dest-server https://kubernetes.default.svc \
      --sync-policy auto
```

List apps

```
argocd app list
```

### Make tests to exercise and evaluate continuous delivery

```
docker build . -t docker.io/helloyufan/american-predictor:0.2
docker push docker.io/helloyufan/american-predictor:0.2
```
