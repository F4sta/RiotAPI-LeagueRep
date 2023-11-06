
API_KEY = open("riot_api.txt", "r").readline()
DEFAULT_REGION_CODE = "eun1"
DEFAULT_REGION = "europe"

REGION_CODES = [i.removesuffix("\n") for i in open("region_codes.txt", "r").readlines()]
REGIONS = [i.removesuffix("\n") for i in open("regions.txt", "r").readlines()]
