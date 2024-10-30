from mangum import Mangum

from schafkopf.api import api

handler = Mangum(api.app, lifespan="off")
