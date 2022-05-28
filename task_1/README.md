1. Setup a pod or isolated container comprising a SQL Database

Use this docker-compose.yml
```yaml
version: '3.1'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: maryblack
      POSTGRES_USER: maryblack
      POSTGRES_PASSWORD: maryblack
    ports:
      - 5432:5432
```
Start container with  `docker-compose up`.

2. Import testset_B.tsv into the SQL DB.

Copy file to docker container `docker cp testset_B.tsv <container-id>:/tmp/`
Check if we copied file
```bash
docker exec -it <container-name> bash
root@<container-id>: cd /tmp
root@<container-id>: ls -a | grep testset_B
```
3. Create a Python script that connects to the database, calculates the following KPIs and stores each of them in a separate CSV file: `task_1/task_1_script.py`
