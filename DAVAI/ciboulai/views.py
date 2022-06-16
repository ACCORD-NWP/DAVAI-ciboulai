from django.shortcuts import render
from .models import Ciboulexp,GmapReference,Note,Task,TaskInstance
from django.http import Http404
from django.http import JsonResponse
from .tasks import updateCiboulexp
import json
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from template_tags.custom_tags import prettyJson3


def Front(request):
    context=dict()
    template='ciboulai.html'

    countExp=Ciboulexp.objects.filter().count()
    page = int(request.GET.get('page', 1))
    numberPerPage=30
    pageList=list(range(1,1+int(countExp/numberPerPage)))
    
    start=(page-1)*numberPerPage

    context = {
        'gmapReferences':GmapReference.objects.order_by('-mainCycle'),
        'ciboulexps':Ciboulexp.objects.order_by('-pk')[start:start+numberPerPage],
        'taskCount':Task.objects.filter().count(),
        'taskInstanceCount':TaskInstance.objects.filter().count(),
        'page':page,
        'pageList':pageList,
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
    


def CiboulexpView(request,cid):
    template = 'ciboulaiView.html'
    if Ciboulexp.objects.filter(pk=cid).exists():
        exp=Ciboulexp.objects.get(pk=cid)
        #----
#        globalDico=json.loads(exp.json)

        globalDico2={}
        for ti in TaskInstance.objects.filter(expRef=exp):
            try:
                td=json.loads(ti.jsonTask)
            except:
                td={'error':'error in json.loads'}

            globalDico2[ti.taskRef]=td
        #----

        headers=['task','last update','status','comparison status','main metric','value','drHook rel diff','rss rel diff','more']
        xpinfoKeys=['user','xpid','ref_xpid','pack','git_branch','appenv','appenv_global','appenv_lam','appenv_clim','commonenv','input_store','input_store_lam','input_store_global','initial_time_of_launch','comment','usecase']

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
        context = {
            'exp':exp,
            'xpinfo':xpinfo,
#            'solo':globalDico,
            'globalDico':globalDico2,
            'headers':headers,
            'headersSolo':headersSolo,
            'notes':notes,
            'xpinfoKeys':xpinfoKeys,
             }
        
        return render(request, template, context)
        
    else:
        raise Http404("Page does not exist") 
    
def CiboulexpLightView(request,cid):
    template = 'ciboulaiLightView.html'
    if Ciboulexp.objects.filter(pk=cid).exists():
        exp=Ciboulexp.objects.get(pk=cid)
        #----
#        globalDico=json.loads(exp.json)
    
        globalDico2={}
        for ti in TaskInstance.objects.filter(expRef=exp):
            try:
                td=json.loads(ti.jsonTask)
            except:
                td={'error':'error in json.loads'}

            globalDico2[ti.taskRef]=td

        #----

        headers=['task','last update','status','comparison status','main metric','value','drHook rel diff','rss rel diff','more']
        xpinfoKeys=['user','xpid','ref_xpid','pack','git_branch','appenv','appenv_global','appenv_lam','appenv_clim','commonenv','input_store','input_store_lam','input_store_global','initial_time_of_launch','comment','usecase']

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
        context = {
            'exp':exp,
            'xpinfo':xpinfo,
#            'solo':globalDico,
            'globalDico':globalDico2,
            'headers':headers,
            'headersSolo':headersSolo,
            'notes':notes,
            'xpinfoKeys':xpinfoKeys,
             }
        
        return render(request, template, context)
        
    else:
        raise Http404("Page does not exist") 



def getSummary(request):
    if request.method == 'POST':
        pass
    else:
        xpid = str(request.GET.get('xpid', None))
        jsonSummary=importSummary(xpid)
        #the content exist
        return JsonResponse(jsonSummary)     
    
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
        
def importFile(request):
    if request.method == 'POST':
        q=request.FILES['file']
        globalDict=json.loads(q.read().decode('utf-8'))
        xpinfo=globalDict.pop("xpinfo")
#        reponseDict=updateCiboulexp(xpinfo,fromFile=True,dictJson=globalDict)
        if reponseDict.get('error'):
            raise Http404(reponseDict.get('error')) 
        else:
            return redirect(reponseDict.get('redirect'))





@csrf_exempt
def api(request):
    rc=-1
    message=""
    if request.method == 'POST':
        xpid = str(request.POST.get('xpid', None))
        jsonData = str(request.POST.get('jsonData', None))
        type = str(request.POST.get('type', None))
        if type=="xpinfo":
            #check if jsonData seems ok
            jsonDict=json.loads(jsonData)
            if not "xpinfo" in jsonDict:
                rc=1
                message="The json provided do not contains xpinfo key"
            else:
                returnDict=updateCiboulexp(jsonDict.get('xpinfo'),fromFile=False)             
                rc=returnDict.get('rc')
                message=returnDict.get('message')
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
#                globalDico2={}
#                for ti in TaskInstance.objects.filter(expRef=exp):
#                    globalDico2[ti.taskRef]=json.loads(ti.jsonTask)
#                exp.summary=generateSummaryString(globalDico2)
                exp.save()
                rc=0
                    
            else:
                rc=1
                message="The XPID %s do not exists. You need to call xpinfo task first with type='xpinfo'"%(xpid)

        else:
            rc=-2
            message="Type (3 argument) must be 'xpinfo' or 'task'"            
        

    else:
        rc=-1
        message="This url only accepts POST and not GET: fail! "
    
    return JsonResponse({
        'returnCode':rc,
        'message':message,
        
    })  

