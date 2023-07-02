# Your own helm syntax
Have you been using [helm](https://helm.sh/)? No? Oh, man, you're a lucky guy!   
Unfortunately, some of us are not so lucky, 'cause they have to.   
OK, so, it's not about pros and cons of helm, it's really subjective.    
Now, suppose that you deploy your applications using helm and it would be great for you to improve or simply shorten helm chart/values file syntax.   
Actually, the idea is that in most cases you have got almost the same helm chart/values file for all applications you have.   
Indeed, you tend to use the same amount of replicas, don't you?   
You tend to use the same repository to pull for your nginx.   
You are likely use the same external and internal service port, aren't you?    
Why does all this happen? The right answer can be copy/paste, kind of templates, skaffold and so on and so on.     
Taking into account all this kinda copy/paste, there is a question: why not decrease the amount of this stuff?    
Let's try to do so. 
Let's suppose it turned out that you only have applications with 1 (minimal) or 3 (maximum) replicas.   
Let's also suppose, that you only pull nginx latest image and have the same service configuration, 
probably with different internal and external ports.    
It's time to invent your own helm syntax!
## Expected input
You've been sitting a lot thinking and finally come up with a great and short helm syntax.
```yaml
replicaCount: minimum  # <<< or maximum
image: nginx_latest  # <<< the only available option
service: nginx_8080  # <<< the port can be different, but template `nginx_` can't
```
## Expected output
We are expecting that your compact and pretty syntax is transforming into the real part of helm (values) file.
```yaml
replicaCount: 1
image:
  pullPolicy: IfNotPresent
  repository: nginx
  tag: latest
service:
  externalPort: 8080
  internalPort: 8080
  name: nginx
  type: ClusterIP
```
## Run it
To make all this magic work you need to type following:
```bash
$ python3 -m sugaru values.yaml --plugin helm_values
```
