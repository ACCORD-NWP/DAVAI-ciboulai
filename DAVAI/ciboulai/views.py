from django.shortcuts import render
from .models import Ciboulexp,GmapReference,Note,Task,TaskInstance
from django.http import Http404
from django.http import JsonResponse
from .tasks import updateCiboulexp
import json
import datetime
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import os
from template_tags.custom_tags import prettyJson3
from math import ceil

def Front(request):
    context=dict()
    template='ciboulai.html'

    allXp = request.GET.get('all', False)
    
    olddb = request.GET.get('old', False)


    if allXp:
        query=Ciboulexp.objects.filter().order_by('-pk')
        pageH1='Davai all tests'
    else:
        if olddb:
            TrueCiboulexp=Ciboulexp.objects.using('old')
        else:
            TrueCiboulexp=Ciboulexp.objects.filter().order_by('-pk')
        if False:
            #maybe not cheap
            dt=datetime.datetime.now()-datetime.timedelta(days=31)
            query=TrueCiboulexp.filter(updated__gt=dt).order_by('-pk')
        else:
            #last pk
            pkmax=TrueCiboulexp[0].pk
            query=TrueCiboulexp.filter(pk__gt=pkmax-100)


        pageH1='Davai recent tests'

    countExp=query.count()
    page = int(request.GET.get('page', 1))
    numberPerPage=10
    pageList=list(range(1,1+ceil(countExp/numberPerPage)))
    
    start=(page-1)*numberPerPage

    context = {
        'gmapReferences':GmapReference.objects.order_by('-mainCycle'),
        'ciboulexps':query[start:start+numberPerPage],
        'taskCount':Task.objects.filter().count(),
        'taskInstanceCount':TaskInstance.objects.filter().count(),
        'page':page,
        'pageList':pageList,
        'pageH1':pageH1,
        'countExp':countExp
    }
    return render(request, template, context)


def NotesView(request):
    context=dict()
    template='ciboulaiNotes.html'
    context = {
        'notes':Note.objects.order_by('-pk'),
    }
    return render(request, template, context)

def TaskView(request,tid):
    template = 'ciboulaiTaskView.html'
    if Task.objects.filter(pk=tid).exists():
        task=Task.objects.get(pk=tid)
        tasksInstances=TaskInstance.objects.filter(taskRef=task).order_by('-pk')
        headers=['XPID','Base cycle', 'User','Updated','Main Metric','Value','Status','More']
        context = {
            'task':task,
            'headers':headers,
            'tasksInstances':tasksInstances,
             }
        
        return render(request, template, context)
        
    else:
        raise Http404("Task does not exist") 

def AllTasks(request):
    template = 'ciboulaiAllTasks.html'
    tasksDict={}
    for t in Task.objects.filter():
        tasksDict[t.name]={
                'pk':t.pk,
                'count':TaskInstance.objects.filter(taskRef=t).count(),
                'notes':Note.objects.filter(task=t.name).count(),
                'ok':TaskInstance.objects.filter(taskRef=t,symbol='ok').count(),
                'ko':TaskInstance.objects.filter(taskRef=t,symbol='ko').count(),
                'tc':TaskInstance.objects.filter(taskRef=t,symbol='tc').count(),
                'cr':TaskInstance.objects.filter(taskRef=t,symbol='cr').count(),
                'nc':TaskInstance.objects.filter(taskRef=t,symbol='nc').count()}
    context = {
        'tasksDict':tasksDict,
    }
    return render(request, template, context)

def LastTaskInstances(request):
    template = 'ciboulaiLastTaskInstances.html'
    taskInstancesList=TaskInstance.objects.order_by('-updated')[0:100] 
    context = {
        'taskInstancesList':taskInstancesList,
    }
    return render(request, template, context)
    
    
def CiboulexpLightView(request,cid):
    template = 'ciboulaiLightView.html'
    if Ciboulexp.objects.filter(pk=cid).exists():
        exp=Ciboulexp.objects.get(pk=cid)
    
        globalDico2={}
        for ti in TaskInstance.objects.filter(expRef=exp):
            try:
                td=json.loads(ti.jsonTask)
            except:
                td={'error':'error in json.loads'}

            globalDico2[ti.taskRef]=td

        #----

        #headers=['task','last update','status','comparison status','consistency','main metric','value','rss rel diff','more']
        headers=[
    ("update", "timestamp of latest update of the task"),
    ("task", "identifier of the task, described by a series of attributes such as job prefix/sequence, model, kind of task, families, compiler flavours etc..."),
    ("status", "status of the task"),
    ("continuity", "comparison to the same task of a reference experiment"),
    ("consistency", "(occasional) comparison to another task of the same experiment"),
    ("main metric", "most relevant metric to assess test results"),
    ("value", "value of the indicated main metric"),
    ("RSS reldiff", "relative difference in RSS (memory)"),
]
        #headers=['task','last update','status','comparison status','main metric','value','drHook rel diff','rss rel diff','more']

        headersSolo=[]
  
        notes={}
        for n in Note.objects.filter(xpid=exp.xpid):
            if n.task in notes.keys():
                notes[n.task].append(n.message)
            else:
                notes[n.task]=[n.message]
        try:
            xpinfo=json.loads(exp.xpinfo)
        except:
            xpinfo={}
        xpinfoKeys=list(xpinfo.keys())
        for it in ['appenv_lam_details', 'appenv_clim_details', 'appenv_global_details', 'commonenv_details']: # to hide
            xpinfoKeys.remove(it)
        xpinfoKeys.sort()
        headenv=['appenv_global','appenv_lam','appenv_fullpos_partners','appenv_clim','commonenv','davaienv']
        filterClick=["arpege","arome","alaro","forecast","ensemble","adjoint","3D","4D","obs_op","screening","fullpos","surfex","LAM","batodb","minim","OOPS","CNT0"]
        context = {
            'exp':exp,
            'xpinfo':xpinfo,
#            'solo':globalDico,
            'globalDico':globalDico2,
            'headers':headers,
            'headersSolo':headersSolo,
            'notes':notes,
            'xpinfoKeys':xpinfoKeys,
            'headenv':headenv,
            'filterClick':filterClick,
             }
        
        return render(request, template, context)
        
    else:
        raise Http404("Page does not exist") 



def getSummary(request,xpid_or_cid):
    if request.method == 'POST':
        pass
    else:
        summary={}
        if Ciboulexp.objects.filter(xpid=xpid_or_cid).exists():
            exp=Ciboulexp.objects.get(xpid=xpid_or_cid)
        else:
            try:
                theid=int(xpid_or_cid)
                exp=Ciboulexp.objects.get(pk=theid)
            except:
                return JsonResponse({"message":"Ciboulexp {} do no exists".format(xpid_or_cid)})
        summary={"id":exp.pk,"updated":exp.updated,"message":"OK","summary":exp.jsonSummary,"user":exp.user,"reference":exp.reference.xpid,"xpid":exp.xpid}
        return JsonResponse(summary)     
    
def addNote(request):
    if request.method == 'POST':
        pass
    else:
        xpid = str(request.GET.get('xpid', None))
        task = str(request.GET.get('task', None))
        message = str(request.GET.get('message', None))
        Note.objects.create(
            xpid=xpid,
            task=task,
            message=message
            ).save()
        #the content exist
        return JsonResponse({
            'message':'la note a été correctement ajoutée!'
            
            })   


def ajaxXpids(request):
    if request.method == 'POST':
        pass
    else:
        Ciboulexp.objects.filter()
        return JsonResponse(list(Ciboulexp.objects.filter().order_by('-xpid').values('xpid','pk')),safe=False)



def ajaxLoadModal(request):
    if request.method == 'POST':
        pass
    else:
        message=''
        error=''
        data={}
        ciboulexpId = str(request.GET.get('ciboulexpId', None))
        taskmodalId= int(request.GET.get('modalId', None))
        
        if Ciboulexp.objects.filter(pk=ciboulexpId).exists():
            exp=Ciboulexp.objects.get(pk=ciboulexpId)    
            try:  
                ti=list(TaskInstance.objects.filter(expRef=exp))[taskmodalId-1]
                data=json.loads(ti.jsonTask)
                message='OK'
                
                
            except:
                error='error in ajaxLoadModal json.loads'
            reponse={}
            for k in ['itself','continuity','consistency']:
                skipData=(k=='consistency') and (k in data.keys()) and ('comparisonStatus' in data[k].keys()) and ('symbol' in data[k]['comparisonStatus'].keys()) and (data[k]['comparisonStatus']['symbol']=="0")
                if k in data.keys() and not skipData:
                #if k in data.keys():
                    reponse[k]=prettyJson3(data[k])

            
        else:    
            error="Error, requested xpid do not exists. It should never happend"
         

        return JsonResponse({
            'message':message,
            'reponse':reponse,
            'error':error,
            })        
        

@csrf_exempt
def api(request):
    rc=-1
    message=""
    if request.method == 'POST':
        xpid = str(request.POST.get('xpid', None))
        jsonData = str(request.POST.get('jsonData', None))
        type = str(request.POST.get('type', None))
        pwd = request.POST.get('token', None)
        if pwd and os.getenv('DAVAI_POST_PWD') and pwd==os.getenv('DAVAI_POST_PWD'):
            message+="Token is OK!"
        else:
            message+="ERROR: Token is not present or wrong, Ciboulai feeding refused. Please provide a valid token.\n"
            rc=1
            return JsonResponse({
              'returnCode':rc,
              'message':message,
            })

        if type=="xpinfo":
            #check if jsonData seems ok
            jsonDict=json.loads(jsonData)
            if not "xpinfo" in jsonDict:
                rc=1
                message+="The json provided do not contains xpinfo key"
            else:
                returnDict=updateCiboulexp(jsonDict.get('xpinfo'),fromFile=False)             
                rc=returnDict.get('rc')
                message+=returnDict.get('message')
                message+="XPID: %s"%returnDict.get('xpid')
                
        elif type in ['taskinfo','task','statictaskinfo'] :
            if Ciboulexp.objects.filter(xpid=xpid).exists():
                exp=Ciboulexp.objects.get(xpid=xpid)
                taskDico=json.loads(jsonData)
                for task in taskDico.keys():
                    if not Task.objects.filter(name=task).exists():
                        Task.objects.create(name=task).save()
                    taskRef=Task.objects.get(name=task)

                    if TaskInstance.objects.filter(expRef=exp,taskRef=taskRef).exists():
                        ti=TaskInstance.objects.get(expRef=exp,taskRef=taskRef)
                        if 'itself' in taskDico[task].keys():
                            ti.jsonTask=json.dumps(taskDico[task])
                        else:
                            #in this case we just wants to update the dict
                            update=json.loads(ti.jsonTask)
                            update.update(taskDico[task])
                            ti.jsonTask=json.dumps(update)
                        message+="""The task %s on xpid %s has successfully
                        been updated into ciboulaï database!\n"""%(task,xpid)
                        ti.save()
                    else:
                        ti=TaskInstance.objects.create(expRef=exp,taskRef=taskRef,jsonTask=json.dumps(taskDico[task]))
                        ti.save()
                        message+="The task %s on xpid %s has successfully been created into ciboulaï database!"%(task,xpid)
                    ti.updateSymbol()
                exp.save()
                rc=0
                    
            else:
                rc=1
                message+="The XPID %s do not exists. You need to call xpinfo task first with type='xpinfo'"%(xpid)

        else:
            rc=-2
            message+="Type (3 argument) must be 'xpinfo' or 'task'"            
        

    else:
        rc=-1
        message+="This url only accepts POST and not GET: fail! "
    
    return JsonResponse({
        'returnCode':rc,
        'message':message,
    })  

