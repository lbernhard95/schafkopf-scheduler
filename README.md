# Schafkopf Scheduler
Creates new bitpolls and when finding a date with enough participants, sends out invitations via gmail.
![Schafkopf Scheduler](SchafkopfScheduler.drawio.svg)

# BeachBooker
Looks for a free date for beach volleyball slots at ZHS
![BeachBooker Diagram](BeachBooker.drawio.svg)

## Running locally
### Setup the environment
Create a `.env` file
```bash
READ_ONLY=0
ZHS_USERNAME=<username>
ZHS_PASSWORD=<password>

```

### Run without docker
Execute `poetry run python beachbooker/main.py`

### Run with docker
Execute `run_beachbooker.sh` to build and run the docker container.
