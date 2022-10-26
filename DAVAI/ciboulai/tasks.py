from __future__ import absolute_import, unicode_literals


import json
from .models import Ciboulexp,TaskInstance
from django import db
import datetime


symbolToCode={
    'OK':'ok',
    'KO':'ko',
    '?':'tc',
    '!':'tc',
    '+':'tc',
    'X':'cr',
    'X=R':'cr',
    'X:R?':'cr',
    '0':'nc',
    '-':'nc',
    'E!':'tc',
    }



def updateCiboulexp(confDict,fromFile=False):

    suppr=''
    message=''
    rc=-2
    if fromFile:
        confDict['xpid']='%s@file'%(confDict.get('xpid'))
        
    else:
        if Ciboulexp.objects.filter(xpid=confDict.get('xpid')).exists():
            xp=Ciboulexp.objects.get(xpid=confDict.get('xpid'))
            xp.xpid=confDict.get('xpid')
            xp.user=confDict.get('user')
            xp.json=json.dumps({})
            xp.xpinfo=json.dumps(confDict)
            xp.summary=""
            if confDict.get('ref_xpid'):
                if Ciboulexp.objects.filter(xpid=confDict.get('ref_xpid')).exists():
                    xp.reference=Ciboulexp.objects.get(xpid=confDict.get('ref_xpid'))
            else:
                xp.reference=None
            xp.save()
            TaskInstance.objects.filter(expRef=xp).delete()
            suppr="(the existing ciboulExp with the same XPID has been reset). "
            rc=0
        else:
            try:
                xp=Ciboulexp.objects.create(
                    xpid=confDict.get('xpid'), 
                    user=confDict.get('user'),
                    xpinfo=json.dumps(confDict),
                    json=json.dumps({}),
                    summary="")
                if Ciboulexp.objects.filter(xpid=confDict.get('ref_xpid')).exists():
                    xp.reference=Ciboulexp.objects.get(xpid=confDict.get('ref_xpid'))
                xp.save()
                rc=0
                message='ciboulexp creation succeed !%s '%(suppr)
                
            except Exception as e:
                message='ciboulexp creation failed : %s '%e
                rc=-9
                
    return {                
        'xpid':confDict['xpid'],
        'message':message,
        'rc':rc
    }
            

