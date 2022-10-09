from datetime import datetime
from document.models import PRKData
from .models import LRPA_File
from recomposition.models import UsulanPeriod

def safe_div(x,y):
    if y==0: return 0
    return x/y

def this_month():
    return datetime.now().month

def is_production():
    return False

def get_last_lrpa():
    return LRPA_File.objects.order_by('-pk').first()

def get_all_prk_last_lrpa(rekap_user_induk=None):
    if rekap_user_induk == None:
        return PRKData.objects.select_related('prk').filter(file_lrpa=get_last_lrpa())
    
    return PRKData.objects.select_related('prk').filter(file_lrpa=get_last_lrpa(), prk__rekap_user_induk=rekap_user_induk)

def get_latest_rekom_period():
    return UsulanPeriod.objects.order_by('-pk').first()

