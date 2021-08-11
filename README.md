<h1 align="center">
  PyAPI
</h1>
<p align="center">Restfull API framework built by and for python</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v1.0.0-blue?style=for-the-badge&logo=none" alt="cli version" />
</p>

<p align="center">
  Tested Supported OS <br/><br/>
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="" />
  <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="" />
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



(Optional) - register 404 endpoint
```python
# override 404 not found callback
def __not_found_callback():
    return HttpResponder.build(404, '<h1>This API endpoint is not found!</h1>', {'Content-type': 'text/html'})

# initialize endpoints handler
endpoints = RestEndPoints(not_found_callback=__not_found_callback)
```


Register the imported endpoints
```python
# add some endpoints
endpoints.add('/clients', clients.callback)
endpoints.add('/clients/add', clients_add.callback)
```

Start the restfull API server
```python
# start the server
server = RestServer('127.0.0.1', endpoints=endpoints, env='local')
server.start()
```

Or start the server with the example "entry.py" file via the terminal:
```python
> sudo python3 entry.py
```


Open the browser and type the following in the address bar to see the example endpoints in action:
```python
> 127.0.0.1:8820
```
<br/>
<br/>

## ❕ Notes
- If you notice and bug or error, or if you have a suggestion, please dont hesitate and let me know <br/>
  so that i could fix it and make the framework even better!
<br/>

## ⚠️ License

`PyAPI` is free and open-source software licensed under the [GNU 3.0 License](https://github.com/levkany/PyAPI/blob/master/LICENSE)
