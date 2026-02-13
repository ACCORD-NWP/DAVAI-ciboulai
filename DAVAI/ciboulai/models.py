from django.db import models
import json
# Create your models here.
class Ciboulexp(models.Model):
    user=models.CharField(max_length=200,unique=False,default='UNDEF')
    xpid=models.CharField(max_length=200,unique=False,default='UNDEF')
    json=models.TextField(blank=True) 
    xpinfo=models.TextField(blank=True) 
    summary=models.TextField(blank=True)
    reference=models.ForeignKey("Ciboulexp",blank=True,on_delete=models.CASCADE,null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.xpid
    class Meta:
        db_table = u'main_ciboulexp'
    
    @property
    def jsonFromTasksInstances(self):
        d={}
        for t in self.tasksInstances.filter():
            d[t.taskRef.name]=t.jsonTask
        return json.dumps(d)
    
    @property
    def symbolSummary_ok(self):
        return self.symbolSummary('ok')
    @property
    def symbolSummary_ko(self):
        return self.symbolSummary('ko')
    @property
    def symbolSummary_cr(self):
        return self.symbolSummary('cr')
    @property
    def symbolSummary_tc(self):
        return self.symbolSummary('tc')
    @property
    def symbolSummary_nc(self):
        return self.symbolSummary('nc')
    
    @property
    def symbolSummary_nan(self):
        return self.symbolSummary('NAN')
  
    @property
    def jsonSummary(self):
        total= TaskInstance.objects.filter(expRef=self)
        totalCount=total.count()
        ans={"sum":totalCount,"ok":0,"ko":0,"cr":0,"tc":0,"nc":0,"NAN":0}

        for t in total:
            ans[t.symbol]+=1
        return ans 

    def symbolSummary(self,code='ok'):
        cssClass=""
        count= TaskInstance.objects.filter(expRef=self,symbol=code).count()
        total= TaskInstance.objects.filter(expRef=self).count()
        if count > 0:
            if code=='ko':
                cssClass='table-danger'
            elif (code=="cr" or code=='tc'):
                cssClass='table-warning'
            elif code=='ok':
                cssClass='table-success'
        if total>1:    
            stri="<td class='align-middle {}'>{} <small>({:.1%})</small></td>".format(cssClass,count,count/float(total))
        else:
            stri="<td class='align-middle {}'>{} <small>({:.1%})</small></td>".format(cssClass,count,0)

        return stri


class Task(models.Model):
    name=models.CharField(max_length=200,unique=True,default='UNDEF')
    def __str__(self):
        return self.name
    class Meta:
       db_table = u'main_task'

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


class TaskInstance(models.Model):
    taskRef=models.ForeignKey("Task",blank=True,on_delete=models.CASCADE,null=True)
    jsonTask=models.TextField(blank=True)
    expRef=models.ForeignKey("Ciboulexp",blank=True,on_delete=models.CASCADE,null=True)
    symbol=models.CharField(max_length=3,default='NAN')
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = u'main_taskinstance'
        unique_together = ('taskRef','expRef',)

    def __str__(self):
        return self.taskRef.name+' : '+self.expRef.xpid

    def updateSymbol(self):
        j=json.loads(self.jsonTask)
        sym='NAN'
        try:
            if j['itself']['Status']['symbol']!="E":
                sym=symbolToCode[j['itself']['Status']['symbol']]
            else:
                if j.get('continuity') is None or j.get('consistency') is None:
                    sym='tc'
                else:
                    if j['continuity'].get('comparisonStatus') is None:
                        sym='tc'
                    else:
                        l=[j['continuity']['comparisonStatus']['symbol'],j['consistency']['comparisonStatus']['symbol']]
                        if 'KO' in l:
                            sym='ko'
                        elif '?' in l or '!' in l:
                            sym='tc'
                        elif 'OK' in l:
                            sym='ok'
                        else:
                            sym='nc'
        except:
            pass
        self.symbol=sym
        self.save()


class GmapReference(models.Model):
    ciboulexp=models.ForeignKey("Ciboulexp",blank=True,on_delete=models.CASCADE,null=True)
    mainCycle=models.CharField(max_length=200,unique=False,default='UNDEF')
    class Meta:
       db_table = u'main_gmapreference'
 

class Note(models.Model):
    xpid=models.CharField(max_length=200,unique=False,default='UNDEF')
    task=models.CharField(max_length=200,unique=False,default='UNDEF')
    message=models.TextField(blank=True) 
    class Meta:
       db_table = u'main_note'

