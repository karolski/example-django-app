# Centric Assignement
[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/10902164-76782cbc-9f83-46ed-9f9f-7510809b9427?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D10902164-76782cbc-9f83-46ed-9f9f-7510809b9427%26entityType%3Dcollection%26workspaceId%3D5fc90e7a-5b3e-4f50-92b8-d935279aa7fe)

- The db has a superuser preloaded for the sake of testing (I would not do that in any production database):
  - user: admin
  - password: password 
- [documentation is here](https://documenter.getpostman.com/view/10902164/2s9Xy6opCW) and the [postman collection is also here](Centric%20App.postman_collection.json)
- I left the Django secret in the code
- The images and the database are committed in the repository
- I opted for using requests to crawl images - it is too simple of a task to make a scrapy project for it. 

### relevant links
- [localhost:8080/music/artists](localhost:8080/music/artists)



## Development
### One line and start development
```shell script
docker-compose up --build -d
```
and start playing usnig postman or other tools

### To develop locally run
```shell
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
pipenv shell
```

### Script to scrape and update artist images
```shell
PYTHONPATH=. python artist_image_scraping/scrape_artists_images.py
```

### Test
```shell
coverage run manage.py test
coverage report
```

### Static checks/fixes
```shell
mypy .
isort .
black .
```
