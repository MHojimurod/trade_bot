import re
from click import get_current_context
import requests




def get_current_context(request):
    data  = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/")
    return {"currency":data.json()[0]}
