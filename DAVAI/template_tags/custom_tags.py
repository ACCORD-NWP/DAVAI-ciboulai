from django.template.defaulttags import register
import json
import string
import random
from django.utils.encoding import uri_to_iri
#########################################################################
#########################################################################

#-------------------------------------------Davaï

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

statusSymbolToColor={
    'E':'outline-success',
    'E!':'outline-warning',
    'X':'outline-danger',
    'X=R':'outline-danger',
    'X:R?':'outline-danger',
    None:'outline-danger'
    }

compStatusSymbolToColor={
    'OK':'success',
    'KO':'danger',
    '!':'orange',
    '?':'warning',
    '+':'warning',
    '0':'secondary',
    '-':'secondary',
    }


@register.filter
def leadExpertItselfValue(dictionary):
    dico=json.loads(dictionary)
    c=dico.get('continuity')
    if c:
        lE=c.get('leadExpert')
        if lE:
            it=dico.get('itself')
            if it:
                r=it.get(lE)
                stri=""
                for k,v in r.items():
                    stri+='{}: {}\n'.format(k,v)
                return dictToString2(r)


@register.filter
def mainMetricValue(dictionary):
    if 'mainMetrics' in dictionary.keys():
        k=dictionary['mainMetrics']['expert']
        v=dictionary['mainMetrics']['metrics']
        return dictionary[k][v]
    else:
        return str(dictionary)

@register.filter
def newappenv(dictionary):
    return 'appenv_global' in dictionary

@register.filter
def base_cycle(dictionary):
    t=str(type(dictionary))
    if 'str' in t:
        try:
            d=json.loads(dictionary)
        except:
            return 'ERROR get item, json load'
        if hasattr(d, 'keys'):
            commonenv=d.get('commonenv')
            if commonenv:
                return commonenv.split('uenv:')[-1].split('.')[0]
            else:
                return ' -- '
        else:
            return 'ERROR get item'
    elif 'dict' in t:
        return dictionary.get(key)
    else:
        return 'none'

    
        

    
@register.filter
def dateUpdate(stri):
    if stri:
        return '<br>'.join(stri.split('T'))
    else:
        return '?'

@register.filter
def dateItself(di):
    
    try:
        date=json.loads(di).get('itself').get('Updated')
    except:
        date='Problem occured in the json'
    return date

@register.filter
def status_btn(dictionary,stri):
    if hasattr(dictionary,'get'):
        return "<span><button id='sClickDetail_%s' data-toggle='tooltip' data-placement='top' title='' data-original-title='%s' class='ajaxClickDetail btn btn-%s'>%s</button></span>"%(stri,dictionary.get('text').replace('\"','`').replace('\'','`'),statusSymbolToColor.get(dictionary.get('symbol')),dictionary.get('short'))
    else:
        return "<button id='sClickDetail_%s' data-toggle='tooltip' data-placement='top' title='' data-original-title='%s' class='ajaxClickDetail btn btn-%s'>%s</button>"%(stri,dictionary,'outline-danger','Expertise failed')
@register.filter
def compStatus_btn(dictionary,stri):
    if hasattr(dictionary,'get'):
        return "<span><button id='clickDetail_%s' data-toggle='tooltip' data-placement='top' title='' data-original-title='%s' class='ajaxClickDetail btn btn-%s'>%s</button></span>"%(stri,str(dictionary.get('text').replace('\"','`').replace('\'','`')),compStatusSymbolToColor.get(dictionary.get('symbol')),dictionary.get('short'))
    else:
        return "<span><button id='clickDetail_%s' data-toggle='tooltip' data-placement='top' title='' data-original-title='%s' class='ajaxClickDetail btn btn-%s'>%s</button></span>"%(stri,'Comparison is not available','outline',' --- ')


@register.filter
def leadExpertDescription(dictionary):
    if hasattr(dictionary,'get'):
        lead=dictionary.get('leadExpert')
        leadDict=dictionary.get(lead)
        if hasattr(leadDict,'get'):
            return leadDict.get('mainMetrics')
        else:
            return ' - '
        
    else:
        return ' --- '

@register.filter
def leadExpertValue(dictionary):
    if hasattr(dictionary,'get'):
        lead=dictionary.get('leadExpert')
        leadDict=dictionary.get(lead)
        
        if hasattr(leadDict,'get'):
            mm=leadDict.get('mainMetrics')
            return leadDict.get(mm)
        else:
            return ' - '
        
    else:
        return ' --- '
    
@register.filter
def getDrHookRelDiff(dictionary,key):
    if hasattr(dictionary,'get'):
        val=dictionary.get(key)
        if hasattr(val,'startswith'):
            if val.startswith('-'):
                color='info'
            else:
                color='danger'
            return "<p class='text-%s'>%s</p>"%(color,val)
        else:
            return 'problem %s'%(val)
         
    else:
        return ' --- '




@register.filter
def drHookMetric(dictionary):
    if hasattr(dictionary,'keys'):
        if 'mainMetrics' in dictionary.keys():
            return dictionary[dictionary['mainMetrics']]
        else:
            return 'problem'
    else:
        return 'not a dict'

@register.filter
def note_btn(dictionary, key):
    if key in dictionary.keys():
        stri=''
        for v in dictionary.get(key):
            stri+="""<a  class='btn btn-outline-primary' data-toggle='popover' role='button'  data-trigger='focus' tabindex='0' data-placement='top' title='' data-content="{popover}" data-html='true' data-original-title=''><i class='fas fa-fw fa-sticky-note'></i>{message}</a>""".format(popover=v.replace('\n','<br>').replace('"','\''),message='Notes sur cette tâche')
        return stri
    else:
        return ''


@register.filter
def get_item(dictionary, key):
    t=str(type(dictionary))
    if 'str' in t:
        try:
            d=json.loads(dictionary)
        except:
            return 'ERROR get item, json load'
        if hasattr(d, 'keys'):
            return d.get(key)
        else:
            return 'ERROR get item'
    elif 'dict' in t:
        return dictionary.get(key)
    else:
        return 'none'


@register.filter
def get_itemdetails(dictionary, key):

    t=str(type(dictionary))
    if 'str' in t:
        try:
            d=json.loads(dictionary)
        except:
            return 'ERROR get item, json load'
        if hasattr(d, 'keys'):
            return d.get(key+"_details")
        else:
            return 'ERROR get item'
    elif 'dict' in t:
        return dictionary.get(key+"_details")
    else:
        return 'none'


@register.filter
def prettyJson(dictionary):

    tableStri=""
    if hasattr(dictionary,'keys'): 
        
        for table in sorted(dictionary.keys()):
            header=['expert']
            line=[table]
            striH="<table class='table'><tr><thead><th>expert</th>"
            striB="<tbody><tr><td>%s</td>"%(table)
            if hasattr(dictionary[table],'keys'): 
                for col in dictionary[table].keys():
                    if col == 'Spectral norms evolution graph (SVG)':
                        tableStri+="<div class='card'><div class='card-title'>%s</div><div class='card-body'>%s</div></div>"%(table,dictionary[table][col])
                        continue

                    striH+='<th>%s</th>'%(col)
                    if hasattr(dictionary[table][col],'keys'):
                        striB+='<td>%s</td>'%(dictToString(dictionary[table][col]))
                    elif hasattr(dictionary[table][col],'append'):
                        striB+='<td>%s</td>'%(listToString(dictionary[table][col]))
                    else:
                        striB+='<td>%s</td>'%(dictionary[table][col])
                    
                    
                striH+='</tr></thead>'
                striB+='</tr></tbody></table> '
                tableStri+=striH+striB+'<br><br>'
            elif hasattr(dictionary[table],'append'):
                tableStri+=', '.join(dictionary[table])
            else:
                tableStri+=dictionary[table]
    else:
        tableStri+=dictionary
            
    return tableStri


@register.filter
def prettyJson2(dictionary):

    tableStri="<div id='accordion'>"
    if hasattr(dictionary,'keys'): 
        tableStri+="<div class='card'>"
        for table in sorted(dictionary.keys()):
            headId=randomString(10)
            colId=randomString(10)
            
            
            collapsible="<div class='card-header' id='{}'>".format(headId)
            collapsible+="<h5 class='mb-0'><button class='btn btn-link' data-toggle='collapse' data-target='#{}' aria-expanded='false' aria-controls='{}'>{}</button></h5></div>".format(colId,colId,table)
            collapsible+="<div id='{}' class='collapse' aria-labelledby='{}' data-parent='#accordion'>".format(colId,headId)
                                                                                                                                                                               
            striH="<table class='table'><tr><thead><th>expert</th>"
            striB="<tbody><tr><td>%s</td>"%(table)
            if hasattr(dictionary[table],'keys'): 
                for col in dictionary[table].keys():
                    striH+='<th>%s</th>'%(col)
                    if hasattr(dictionary[table][col],'keys'):
                        striB+='<td>%s</td>'%(dictToString(dictionary[table][col]))
                    elif hasattr(dictionary[table][col],'append'):
                        striB+='<td>%s</td>'%(listToString(dictionary[table][col]))
                    else:
                        striB+='<td>%s</td>'%(dictionary[table][col])
                    
                    
                striH+='</tr></thead>'
                striB+='</tr></tbody></table> '
                collapsible+="<div class='card-body'>{}<br><br></div></div>" .format(striH+striB) 
                tableStri+=collapsible

        tableStri+="</div>"
#     else:
#         tableStri+=dictionary
    tableStri+='</div>'        
    return tableStri

@register.filter
def prettyJson3(dictionary):

    tableStri="<div id='accordion'>"
    if hasattr(dictionary,'keys'): 
        tableStri+="<div class='card'>"
        for table in sorted(dictionary.keys()):
            headId=randomString(10)
            colId=randomString(10)
            collapsible="<div class='card-header' id='{}'>".format(headId)
            collapsible+="<h5 class='mb-0'><button class='btn btn-link' data-toggle='collapse' data-target='#{}' aria-expanded='false' aria-controls='{}'>{}</button></h5></div>".format(colId,colId,table)
            collapsible+="<div id='{}' class='collapse' aria-labelledby='{}' data-parent='#accordion'>".format(colId,headId)
            if hasattr(dictionary[table],'keys'): 
                stri=""                 
                for col in sorted(dictionary[table].keys()):
                    littleSize='col-lg-2'
                    bigSize='col-lg-10'
                    if col == 'Spectral norms evolution graph (SVG)':
                        littleSize='col-lg-12'
                        bigSize='col-lg-12'                   
                    stri+="<div class='row'>"
                    stri+="<div class='{}'>{}</div>".format(littleSize,col)
                    
                    
                    
                    #---------
#                    dictionnaryKeys=dictionary.keys()
#                    dictionnaryTableKeys=dictionary[table].keys()
                    #----------
                    
                    if col == 'Jo-Tables':
                        bigSize='col-lg-12'
                        stri+="<div class='{}'>{}</div>".format(bigSize,dictToJotables(dictionary[table][col],itself=True))
                    elif col=='All comparisons':
                        bigSize='col-lg-12'
                        stri+="<div class='{}'>{}</div>".format(bigSize,dictToJotables(dictionary[table][col],itself=False))
#                    elif col=='canari_stats':
#                        bigSize='col-lg-12'
#                        stri+="<div class='{}'>{}</div>".format(bigSize,dictToCanari(dictionary[table][col]))
#                    elif col=='Observation counts':
#                        bigSize='col-lg-12'
#                        stri+="<div class='{}'>{}</div>".format(bigSize,dictToBator(dictionary[table][col]))
                    elif col=='Task listing uri(s)' or col=='Compare listings at uri(s)':
                        bigSize='col-lg-12'
                        stri+="<div class='{}'>{}</div>".format(bigSize,dictToDiffBtn(dictionary[table][col]))
                    elif col=='Last step with spectral norms':
                        bigSize='col-lg-12'
                        stri+="<div class='{}'>{}</div>".format(bigSize,dictToNorms(dictionary[table][col]))
#                    elif col=='DrHookProfile':
#                        bigSize='col-lg-12'
#                        stri+="<div class='{}'>{}</div>".format(bigSize,dictToDrHook(dictionary[table][col]))
                    else:
                        if hasattr(dictionary[table][col],'keys'):
                            stri+="<div class='{}'>{}</div>".format(bigSize,dictToString(dictionary[table][col]))
                        elif hasattr(dictionary[table][col],'append'):
                            stri+="<div class='{}'>{}</div>".format(bigSize,listToString(dictionary[table][col]))
                        else:
                            stri+="<div class='{}'>{}</div>".format(bigSize,dictionary[table][col])
                    stri+="</div>"
                collapsible+="<div class='card-body'>{}<br><br></div></div>" .format(stri) 
                tableStri+=collapsible
            else:
                stri=""
                stri+="<div class='row'>"
                stri+="<div class='{}'>{}</div>".format('col-lg-12',table)
                stri+="<div class='{}'>{}</div>".format('col-lg-12',dictionary[table])
                stri+="</div>"
                collapsible+="<div class='card-body'>{}<br><br></div></div>".format(stri)
                tableStri+=collapsible
        tableStri+="</div>"
    tableStri+='</div>'        
    return tableStri

def dictToString(dict):
    stri="<ul>"
    for k in sorted(dict.keys()):
        if hasattr(dict[k],'keys'):
            stri+="<li>%s : %s </li>"%(k, dictToString(dict[k]))
        elif hasattr(dict[k],'append'):
            stri+="<li>%s : %s</li>"%(k, listToString(dict[k]))
        else:
            stri+="<li>%s : %s </li>"%(k, dict[k])
    stri+="</ul>"
    return stri

def dictToString2(dict):
    stri=""
    for k in sorted(dict.keys()):
        if hasattr(dict[k],'keys'):
            stri+="%s : %s\n"%(k, dictToString2(dict[k]))
        elif hasattr(dict[k],'append'):
            stri+="%s : %s\n"%(k, listToString(dict[k]))
        else:
            stri+="%s : %s\n"%(k, dict[k])
    return stri
def floatToColor(i):
    if i>0:
        return 'table-danger'
    elif i<0:
        return 'table-success'


def dictToCanari(dict):
    stri=""
    for step in dict.keys()-['Validated means',
                             'Maximum absolute error on OBS-MOD',
                             'Maximum absolute error on Observations number',
                             'Validated']:
        stri+="<div class='row'>{}<table class='table table-hover customTables'>".format(step)
        stri+="<thead><tr><th>step</th><th>obstype</th><th>var</th><th>NUMBER</th><th>OBS-MOD</th><th>SIGMA</th></tr></thead><tbody>"
        for obstype in dict[step].keys():
            for var in dict[step][obstype].keys():
                stri+="<tr><th>{}</th><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                    step,obstype,var,
                    dict[step][obstype][var].get('NUMBER'),
                    dict[step][obstype][var].get('OBS-MOD'),
                    dict[step][obstype][var].get('SIGMA'))

        stri+="</tbody></table></div>"
    return stri
  

def dictToDiffBtn(input):
    stri=""
    if hasattr(input,'keys'):
        #2 listings
        urls={}
        for x in ['ref','test']:
            urls[x]={}
            if input.get(x):
                for l in input.get(x):
                    if 'hendrix' in l:
                        urls[x]['hendrix']='ftp://'+l.split('@')[1]
                    elif 'scratch' in l:
                        urls[x]['scratch']=l
        if urls.get('test').get('hendrix') is None:
            stri="<p>Listing cache Xp : {}</p><p>Listing ftp Ref : {}</p>".format(
                uri_to_iri(urls.get('test').get('scratch')),
                uri_to_iri(urls.get('ref').get('hendrix')))
        else:
            stri="<a target='_blank' class='btn btn-lg btn-success' href='/gws/diff/?path1={}&path2={}'>View listings diffs</a><p>Listing Ref : {} <br>cache: {}</p><p>Listing Xp : {}</p>".format(
            uri_to_iri(urls.get('ref').get('hendrix')),uri_to_iri(urls.get('test').get('hendrix')),
            uri_to_iri(urls.get('ref').get('hendrix')),uri_to_iri(urls.get('ref').get('scratch')),
            uri_to_iri(urls.get('test').get('hendrix')))    
    elif hasattr(input,'append'):
        for l in input:
            stri+="<p>Listing : {}</p>".format(uri_to_iri(l))

    else:
        #1 listing
        url="undef"
        urlCache="undef"
        for l in input:
            if 'hendrix' in l:
                url='ftp://'+l.split('@')[1]
            elif 'scratch' in l:
                urlCache=l
        if url == "undef":
            stri="<p>Listing cache: {}</p>".format(uri_to_iri(urlCache))    
        else:
            stri="<a target='_blank' class='btn btn-lg btn-success' href='/gws/diff/?path1={}'>View listing</a><p>Listing : {}<br>cache: {}</p>".format(uri_to_iri(url),uri_to_iri(url),uri_to_iri(urlCache))    
    return stri



def dictToNorms(dict):
    stri=""
    for normtype in dict.keys()-['step']:
        stri+="<div class='row'>{}<table class='table table-hover customTables'>".format(normtype)
        stri+="<thead><tr><th>field name</th><th>min</th><th>max</th><th>avg</th></tr></thead><tbody>"
        for field in dict[normtype].keys():
            if hasattr(dict[normtype][field],'keys'):
                stri+="<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                        field,
                        dict[normtype][field].get('minimum'),
                        dict[normtype][field].get('maximum'),
                        dict[normtype][field].get('average'))
            else:
                stri+="<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                        field,'-','-',dict[normtype][field])

        stri+="</tbody></table></div>"
    return stri

def dictToDrHook(dict):
    stri=""
    for normtype in dict.keys()-['step']:
        stri+="<div class='row'>{}<table class='table table-hover customTables'>".format(normtype)
        stri+="<thead><tr><th>field name</th><th>min</th><th>max</th><th>avg</th></tr></thead><tbody>"
        for field in dict[normtype].keys():
            if hasattr(dict[normtype][field],'keys'):
                stri+="<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                        field,
                        dict[normtype][field].get('minimum'),
                        dict[normtype][field].get('maximum'),
                        dict[normtype][field].get('average'))
            else:
                stri+="<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                        field,'-','-',dict[normtype][field])

        stri+="</tbody></table></div>"
    return stri

def dictToJotables(dict,itself=True):
    stri=""
    for step in dict.keys():
        stri+="<div class='row'>{}<table class='table table-hover customTables'>".format(step)
        if itself:
            stri+="<thead><tr><th>obstype</th><th>sensor</th><th>var</th><th>jo/n</th><th>jo</th><th>n</th></tr></thead><tbody>"
        else:
            stri+="<thead><tr><th>obstype</th><th>sensor</th><th>var</th><th>reldiff jo/n</th><th>jo/n (xp)</th><th>jo/n (ref)</th><th>reldiff n</th> <th>n (xp)</th><th>n (ref)</th></tr></thead><tbody>"
        for obstype in dict[step].keys():
            for sensor in dict[step][obstype].keys():
                if not 'n' in dict[step][obstype][sensor].keys():
                    for var in dict[step][obstype][sensor].keys():
                        if itself:
                            stri+="<tr><th>{}</th><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(obstype,sensor,var,
                             dict[step][obstype][sensor][var].get('jo/n'),dict[step][obstype][sensor][var].get('jo'),dict[step][obstype][sensor][var].get('n'))
                        else:
                            stri+="<tr><th>{}</th><td>{}</td><td>{}</td><td class='{}'>{}</td><td>{}</td><td>{}</td><td class='{}'>{}</td><td>{}</td><td>{}</td></tr>".format(obstype,sensor,var,
                             floatToColor(dict[step][obstype][sensor][var].get('jo/n').get('reldiff')),format(dict[step][obstype][sensor][var].get('jo/n').get('reldiff'),".3E"),
                             dict[step][obstype][sensor][var].get('jo/nxp'),dict[step][obstype][sensor][var].get('jo/nref'),
                             floatToColor(-dict[step][obstype][sensor][var].get('n').get('reldiff')),
                             format(dict[step][obstype][sensor][var].get('n').get('reldiff'),".3E"),
                             dict[step][obstype][sensor][var].get('nxp'),dict[step][obstype][sensor][var].get('nref'))
                else:
                    if itself:
                        stri+="<tr><th>{}</th><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(obstype,sensor,'-',
                             dict[step][obstype][sensor].get('jo/n'),dict[step][obstype][sensor].get('jo'),dict[step][obstype][sensor].get('n'))
                    else:
                        stri+="<tr><th>{}</th><td>{}</td><td>{}</td><td class='{}'>{}</td><td>{}</td><td>{}</td><td class='{}'>{}</td><td>{}</td><td>{}</td></tr>".format(obstype,sensor,'-',
                         floatToColor(dict[step][obstype][sensor][var].get('jo/n').get('reldiff')),format(dict[step][obstype][sensor][var].get('jo/n').get('reldiff'),".3E"),
                         dict[step][obstype][sensor][var].get('jo/nxp'),dict[step][obstype][sensor][var].get('jo/nref'),
                         floatToColor(-dict[step][obstype][sensor][var].get('n').get('reldiff')),
                         format(dict[step][obstype][sensor][var].get('n').get('reldiff'),".3E"),
                         dict[step][obstype][sensor][var].get('nxp'),dict[step][obstype][sensor][var].get('nref'))

        stri+="</tbody></table></div>"
    return stri


def listToString(list):
    stri="<ul>"
    for k in list:
        if hasattr(k,'keys'):
            stri+="<li>%s</li>"%(dictToString(k))
        elif hasattr(k,'append'):
            stri+="<li>%s</li>"%(listToString(k))
        else:
            stri+="<li>%s </li>"%(k)
    stri+="</ul>"
    return stri

@register.filter
def get_headkeys(dictionary):  
    return dictionary.get('head_headkeys')

@register.filter
def print_headkeys(dictionary):
    stri=""
    for k in dictionary.get('head_headkeys'):
        stri+='%s : %s \n' % (k,dictionary.get(k))
    return stri


@register.filter
def class_table(l):
    return 'table-%s'%(l[1])


@register.filter
def print_keys(dictionary):
    stri="<ul>"
    
    for k in dictionary.keys():
        if k=='DrHookProfile':

            popov=""
            if type(dictionary.get(k)) == dict:
                
                for u in dictionary.get(k).keys():
                    if type(dictionary.get(k).get(u)) == dict:
                        di
                    elif type(dictionary.get(k).get(u)) == list:
                        li
                    else:
                        oth
                    popov+="  %s %s "%(u,dictionary.get(k).get(u))
                stri+="<li><button class='btn btn-default btn-primary' data-html='true' data-toggle='popover' title='%s' data-content='%s'>%s</button></li>" % ('toto',popov,k)
            else:
                for u in list(dictionary.get(k)):
                    if type(u) == dict:
                        for a in u.keys():
                            if type(u.get(a)) == dict:
                                for b in u[a].keys():
                                    popov+="%s %s <br /> "%(b,u.get(a).get(b))
                            else:
                                popov+="%s %s <br /> "%(a,u.get(a))
                            
                    else:
                        popov+="%s <br /> "%(u)

                    
                stri+="<li><button class='btn btn-default btn-primary' data-html='true' data-toggle='popover' title='%s' data-content='%s'>%s</button></li>" % (k,popov,k)
        elif k=='Norms at each step':
            stri+="<li>%s : %s </li>" % (k,'TODO')
        else:
            stri+="<li>%s : %s </li>" % (k,dictionary.get(k))
    stri+="</ul>"
    return stri

@register.filter
def print_details(dictionary):
    popov=""
    popovTitle=""
    for k in dictionary.keys():
        if k == 'head_headkeys':
            continue
        elif k== 'Reference is':
            popovTitle='Ref:'
            for u in dictionary.get(k).keys():
                popovTitle+="  %s %s <br /> "%(u,dictionary.get(k).get(u))
            continue
        substr=""
        if type(dictionary.get(k)) == dict:
            for u in dictionary.get(k).keys()-'head_headkeys':
                substr+="  %s %s <br /> "%(u,dictionary.get(k).get(u))
        elif type(dictionary.get(k)) in [str,float,bool] :
            substr+=str(dictionary.get(k))
        else:
            substr+='TOTO %s'%(k)
        popov+="%s : %s <br />"%(k,substr)
    stri="<button class='btn btn-default btn-primary float-right' data-html='true' data-toggle='popover' title='%s' data-content='%s'>+</button>" % (popovTitle,popov)
    
    return stri


@register.filter
def print_btn(l):
    return "<button class='btn btn-%s'>%s</button>"%(l[1],l[0])

