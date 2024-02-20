# pyTeamQuiz

This is a small webservice for making a local quiz with your friends.
Run the webservice on a computer and open it in the browser of your smart TV or other device.

## Run in development

For development you can run the app using the following commands (the first three are for installing the dependencies).

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
flask --app pyteamquiz.main run
```

As a default, the program will search for question catalogues in the question directory.
However, by specifying an environment variable, you can set the directory to whatever you like:

```bash
export QUESTION_CATALOGUE_DIR="/path/to/questions"
flask --app pyteamquiz run
```


## Run in production

For production you should use docker.
We provide a `Dockerfile` and a `docker-compose` file which you can use to build and deploy your container.
You should probably edit at least the `docker-compose` file to map your question files into the container (otherwise you have to place them in the `./questions`directory).
You *can* also edit the `Dockerfile` in case you want to change, for instance, the WSGI server.

To build and run the container, you can run the following command in the project's root directory:
```
docker-compose -f docker-compose-example.yml up
```