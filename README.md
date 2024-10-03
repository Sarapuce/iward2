# IWard2

## Disclaimer : 

This is a side project to learn how to reverse a mobile app and create a webapp in a Kubernetes cluster. I won't use it since I have a job and don't care about 30€ vouchers. If you are part of the WW team and want me to hide this project, don't hesitate to contact me at alexandre.herve97@gmail.com

## Usage :

### Docker container :

1. Build the container `docker build . -t iward:2`
2. Run it by exposing port 8000, specifying the path of the database, and mounting the volumes with the following command: `docker run -e DBPATH=/db/db.sqlite3 -e PASSWORD=pass -v /path/to/db.sqlite3:/db/ -p 8000:8000 iward:2`
3. Connect to http://localhost:8000 in your favorite browser

### Local :

1. [Install poetry](https://python-poetry.org/docs/)
2. Install poetry dependencies `poetry install`
3. Start a poetry shell `poetry shell`
4. Set `PASSWORD` variable
5. Start the uvicorn server `cd iward2` and `uvicorn main:app --reload`
6. Connect to http://localhost:8000 in your favorite browser.

### Kubernetes :

1. You need to create a PV with ReadWriteMany. You don't need a lot a space 10Mi should be enough

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: iward-pv
  namespace: iward2
  labels:
    name: iward2
spec:
  storageClassName: standard
  capacity:
    storage: 10Mi
  accessModes:
    - ReadWriteMany
  local:
    path: /mnt
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - kind-control-plane
```

2. Create a PVC to attach it to the pods

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: iward-pvc
  namespace: iward2
spec:
  storageClassName: standard
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Mi
  selector:
    matchLabels:
      name: iward2
```

3. Create the deployment

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iward2
  namespace: iward2
spec:
  replicas: 2   # Multiple pods sharing the same file
  selector:
    matchLabels:
      app: iward2
  template:
    metadata:
      labels:
        app: iward2
    spec:
      containers:
      - name: iward2
        image: sarapuce/iward:2
        env:
        - name: PASSWORD
          value: "PASSWORD" # Please use a real secret
        - name: DBPATH
          value: "/db/db.sqlite3"
        volumeMounts:
        - name: iward-db
          mountPath: /db
      volumes:
      - name: iward-db
        persistentVolumeClaim:
          claimName: iward-pvc
```

4. Expose everything with a service

```
apiVersion: v1
kind: Service
metadata:
  name: iward2
spec:
  selector:
    app: iward2
  ports:
    - port: 8000
      targetPort: 8000
  type: ClusterIP
```

5. Now, use what is specific to your cluster to access your application

## How does it works ?

1. Log in to the app with the `PASSWORD` set in env variable. The default one is `password` (I should use a hash but I'm lazy)
2. There are CSRF but I'm also to lazy to patch them
3. Input the email you want to use in the first field
4. Copy the link in your email address and paste it in the second field
5. You should have an interface which shows you how much ward you have
6. You can just let the application validate your steps automatically every day or input a number to do a manual validation
