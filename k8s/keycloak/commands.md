## Keycloak Commands for k8s setup
``` 
kubectl apply -f keycloak.yml
``` 

```
kubectl get pods -n theship-vendor
```

```
kubectl get svc -n theship-vendor
```

Keylcoak runs here:
```
http://<EXTERNAL-IP>:2015
```