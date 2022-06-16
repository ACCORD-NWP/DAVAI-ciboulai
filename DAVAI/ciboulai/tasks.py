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


#def generateSummaryString(dictJson):
#    if len(dictJson.keys())==0:
#        summary={'ok':"<td class='table-warning'>undef</td>",
#                 'cr':"<td class='table-warning'>undef</td>",
#                 'ko':"<td class='table-warning'>undef</td>",
#                 'tc':"<td class='table-warning'>undef</td>",
#                 'nc':"<td class='table-warning'>undef</td>",
#                 }
#    else:
#        
#        summaryDict={
#            'count':{"ok":0,"ko":0,"cr":0,"tc":0,"nc":0},
#            'string':{"ok":"","ko":"","cr":"","tc":"","nc":""},
#            'color':{"ok":"","ko":"","cr":"","tc":"","nc":""}
#            }        
#    
#        for t in dictJson.keys():
#            if dictJson[t]['itself']['Status']['symbol']!="E":
#                summaryDict['count'][symbolToCode[dictJson[t]['itself']['Status']['symbol']]]+=1
#                continue
#            if dictJson[t].get('continuity') is None or dictJson[t].get('consistency') is None:
#                summaryDict['count']["tc"]+=1
#                continue
#
#       
#            if dictJson[t]['continuity'].get('comparisonStatus') is None:
#                summaryDict['count']["tc"]+=1
#                continue
#
#            l=[dictJson[t]['continuity']['comparisonStatus']['symbol'],
#               dictJson[t]['consistency']['comparisonStatus']['symbol']]
#            if 'KO' in l:
#                summaryDict['count']['ko']+=1
#            elif '?' in l or '!' in l:
#                summaryDict['count']['tc']+=1
#            elif 'OK' in l:
#                summaryDict['count']['ok']+=1
#            else:
#                summaryDict['count']['nc']+=1
#                
#         
#        if  summaryDict['count']['ko']>0:
#            summaryDict['color']['ko']='table-danger'  
#        elif summaryDict['count']['cr']>0:    
#            summaryDict['color']['cr']='table-danger'
#        else:
#            if  summaryDict['count']['tc']>0:
#                summaryDict['color']['tc']='table-warning'
#            else:
#                summaryDict['color']['ok']='table-success'
#        
#            
#        for k in summaryDict['count'].keys():
#            summaryDict['string'][k]="<td class='{}'>{:.1%} ({})</td>".format(summaryDict['color'][k],summaryDict['count'][k]/float(len(dictJson.keys())),summaryDict['count'][k])
#        summary=summaryDict['string']              
#    return json.dumps(summary)


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
#            xp.summary=generateSummaryString({})
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
#                    summary=generateSummaryString({}))
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
            
# @shared_task
# def importSummary(xpid):
#     
#     baseFootprint={
#         'cutoff':'a',
#         'date':datetime.datetime.strptime('201712100600','%Y%m%d%H%M') ,
#         'model':'arpifs',
#         'block':'summaries_stack',
#         'namespace': 'vortex.archive.fr',
#         'vapp':    "arpifs",
#         'vconf':   'davai',
#         'experiment':xpid,
#         'unknown':True,
#         'nickname':'trolley.json',
#         'shouldfly':True,
#     }    
#     rh=toolbox.rh(**baseFootprint)
#     try:
#         checkResult=rh.check() 
#     except Exception as err:
#         pass
#     
#     if checkResult:
#         rh.get()
#  
#         with open(rh.container.localpath(), 'r') as outfile:
#             js=outfile.read()    
#             globalDico= json.loads(js)
#         
#         if "Error" in globalDico.keys():
#             return {
#                 'xpid':xpid,
#                 'error':globalDico.get("Error")
#             }    
#         else:
#             d=processFile(globalDico)
#             
#             uenv.clearall()
# 
#     else:
#         d={
#             'xpid':xpid,
#             'error':'Error, XPID unknown! Tried: %s' % (rh.locate())
#         }    
#     
#     
#     return d

