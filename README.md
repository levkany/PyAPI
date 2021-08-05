<h1 align="center">
  PyAPI
</h1>
<p align="center">Restfull API framework built by and for python</p>

<p align="center">
  <a href="https://github.com/create-go-app/cli/releases" target="_blank">
    <img src="https://img.shields.io/badge/version-v1.0.0-blue?style=for-the-badge&logo=none" alt="cli version" />
  </a>
</p>

## 📄 Intro
<p>
  PyAPI is a framework for building restfull api servers the fast, easy and right way! <br/>
  It aims to be the fastest restfull api framework on the internet yet also providing the developer enought flexability and power to control everything, <br/>
  from simple to use endpoint overrides , to total control over what is being recieved and responded. <br/><br/>
  If you need a quick yet powerfull way to create a restfull api, search no more!
</p>
<br/>

## ⚡️ Quick start

Import framework dependencies
```python
# import framework dependencies
from PyAPI.class_server import RestServer
from PyAPI.class_endpoints import RestEndPoints
from PyAPI.class_http_responder import HttpResponder
```


Import example endpoints
```python
# import endpoint callbacks
from endpoints.clients import clients, clients_add
```

Initialize endpoints handler
```python
# initialize endpoints handler
endpoints = RestEndPoints()
```


Register the imported endpoints
```python
# add some endpoints
endpoints.add('/clients', clients.GET, clients.POST)
endpoints.add('/clients/add', clients_add.GET, clients_add.POST)
```

Start the restfull API server
```python
# start the server
server = RestServer('127.0.0.1', endpoints=endpoints, env='local')
server.start()
```

Open the browser and navigate to the clients endpoint to see the example
![image](https://user-images.githubusercontent.com/58599501/128392485-1fb1df8d-6587-4dda-8dde-cc84ce981813.png)

<br/>

## ⚠️ License

`PyAPI` is free and open-source software licensed under the [GNU 3.0 License](https://github.com/levkany/PyAPI/blob/master/LICENSE)
