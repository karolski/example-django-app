# Centric Assignement
[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/10902164-76782cbc-9f83-46ed-9f9f-7510809b9427?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D10902164-76782cbc-9f83-46ed-9f9f-7510809b9427%26entityType%3Dcollection%26workspaceId%3D5fc90e7a-5b3e-4f50-92b8-d935279aa7fe)

- the db has a superuser for the sake of testing:
  - user: admin
  - password: password 

## Development
### One line and start development
```shell script
docker-compose up --build -d
```

### Test
```shell
coverage run manage.py test
coverage report
```
### Lint
```shell
black .

```
### Run script to scrape artist images

