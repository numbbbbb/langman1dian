# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from yanzhengma import create_validate_code
from django.shortcuts import render_to_response
from django.template import RequestContext 
from django.core.context_processors import csrf
from base.models import User,Article,ZhuanTi,Look,ShouCang,HuiFu,Clicked,Jianyi,Look,Looked,HuiFu2,GongGao
from django.utils import simplejson 
from base.widgets import Ueditor
from django import forms
from django.db import models
from forms import PostForm
from django.conf import settings 
from django.db.models import Q
from django.core.paginator import Paginator,InvalidPage,EmptyPage 
from PIL import Image, ImageDraw, ImageFont, ImageFilter 
from django.core.cache import cache
from django.core.mail import send_mail
import shutil
import random
import datetime
import time
import re


dengdai = {}
type2 = 0
id2 = 0
rs = {}
def validate(request):
	#try:     
	#	import cStringIO as StringIO 
	#except ImportError:     
	import StringIO 
	mstream = StringIO.StringIO()           
	validate_code = create_validate_code()     
	img = validate_code[0]     
	#	path1 = "/langman1dian/rte/static/yzmtp/"+str(time.time())+str(random.random())+".png"
	img.save(mstream,"png")           
	img1 = open('/langman1dian/rte/static/yzmtp/xxx.gif','r')
	img1 = mstream.getvalue()
	mstream.close()
	request.session['validate'] = validate_code[1].upper()           
	return HttpResponse(img1,"image/png") 

def signup(request):
	user=User.objects.create(name = request.POST['username'],
							password = request.POST['password'],
							sex = request.POST['sex'],
							level = 1,
							gold = 0,
							looknb = 0,
							lookednb = 0,
							date = time.strftime("%Y-%m-%d %X", time.localtime()),
							recentdate = time.strftime("%Y-%m-%d %X", time.localtime()),
							recentclickdate =  time.strftime("%Y-%m-%d %X", time.localtime()),
							email = request.POST['email'],
							feng = 0,
							iconaddress = "/static/pic/default.gif",
							gly = 0,
							color = "000000"
							)
	shou = ShouCang.objects.create(name = request.POST['username'],
									title = "默认文件夹")
	if user is not None:
		request.session['iflog'] = True
		request.session['username'] = request.POST['username']
		request.session['sex'] = request.POST['sex']
		request.session['peidui'] = False
		request.session['ifgly'] = user.gly
		return HttpResponse(simplejson.dumps({'msg':'注册成功'}))  
	else:  
		return HttpResponse(simplejson.dumps({'msg':'注册失败'})) 
	
def checkuser(request):
	try:  
		user = User.objects.get(name = request.GET['username']) 
		if user is not None:  
			return HttpResponse(simplejson.dumps({'msg':'用户名已存在'}))  
	except:  
		return HttpResponse(simplejson.dumps({'msg':'用户名可以使用'}))  	
		
def checkemail(request):
	try:  
		user = User.objects.get(email = request.GET['email'])
		if user is not None:  
			return HttpResponse(simplejson.dumps({'msg':'邮箱已注册'}))  
	except:  
		return HttpResponse(simplejson.dumps({'msg':''}))  	
		
def editor(request):
	try:
		user1 = User.objects.get(name = request.session['username'])
	except:
		title2 = "请登录！"
		return render_to_response("error1.html",locals());
	if user1.feng == 1:
		title2 = "对不起！您已被禁言！"
		return render_to_response("error1.html",locals());
	form = PostForm(request.POST)
	try:
		request.session['peidui'] = False
		hh = request.GET['hh']
		user = User.objects.get(name=request.session['username'])
		return render_to_response('editor.html',{'form':form,'hh':hh})
	except:
		title2 = "请登录！"
		return render_to_response("error1.html",locals());
		
def imageUp2(request):
	if request.method == 'POST':
		try:
			b = save_file2(request.FILES['upfile'])
		except:
			title2="请选择要上传的图片！"
			return render_to_response("error1.html",locals())
		if b == "large":
			title2 = "图片过大！"
			return render_to_response("error1.html",locals());
		url1 = b['url']
		t = get_template('jcrop1.html') 
		c = RequestContext(request,locals()) 
		return HttpResponse(t.render(c))
	
def save_file2(file,path=''):
	if file._get_size()/1024/1024 >4 :
		return "large"
	filename = str(time.time())+str(random.random())+file._get_name()[-4:]
	fd = open('%s/%s'%(settings.STATICFILES_DIRS[0],str("media/tmp/"+path)+str(filename)),'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()
	a = {'url':'/static/media/tmp/'+filename,'title':filename,'state':'SUCCESS'}
	return a
	
def imageUp(request):
	if request.method == 'POST':
		b = save_file(request.FILES['upfile'])
		return HttpResponse(b)
	
def save_file(file,path=''):
	filename = str(time.time())+str(random.random())+file._get_name()[-4:]
	fd = open('%s/%s'%(settings.STATICFILES_DIRS[0],str("media/tmp/"+path)+str(filename)),'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()
	a = "{'url':'/static/media/tmp/"+filename+"','title':'"+filename+"','state':'SUCCESS'}" 
	return a
	
def index(request):
	dd2 = ""
	try:
		if request.session['guide']:
			dd2 = "none"
	except:
		pass
	try:
		if request.session['iflog']:
			request.session['peidui'] = False
			return render_to_response('index1.html',{'username':request.session['username']})
		return render_to_response('index.html',locals())
	except:
		return render_to_response('index.html',locals())
def yzm(request):
	aa = request.session['validate']
	try:
		bb = request.GET['yzm'].upper()
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	if bb == aa:
		return HttpResponse(simplejson.dumps({'msg':'验证码输入正确'}))
	else:
		return HttpResponse(simplejson.dumps({'msg':'验证码错误'}))
		
def show(request):
	request.session['peidui'] = False
	form = PostForm(request.POST) 
	h2 = request.GET['hh']
	global type2
	try:
		type1 = request.GET['type']
		type2 = type1
	except:
		type1 = type2
	if type1 == '4':
		lls = [1,2,3]
		if h2 == '1':
			posts_list  = Article.objects.filter(type__in=lls).order_by('-recentdate')
		if h2 == '2':
			posts_list  = Article.objects.filter(type__in=lls).order_by('-click')
		if h2 == '3':
			posts_list  = Article.objects.filter(type__in=lls).order_by('?')
	else:
		if h2 == '1':
			posts_list  = Article.objects.filter(type=type1).order_by('-recentdate')
		if h2 == '2':
			posts_list  = Article.objects.filter(type=type1).order_by('-click')
		if h2 == '3':
			posts_list  = Article.objects.filter(type=type1).order_by('?')
	paginator = Paginator(posts_list,10)  #显示20条记录
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	hh = h2
	try:
		gly = request.session['ifgly']
	except:
		gly = 0
	if gly == 1:
		t = get_template('blog1admin.html')
	else:
		t = get_template('blog1.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def show2(request):
	request.session['peidui'] = False
	global type2
	form = PostForm(request.POST) 
	try:
		type1 = request.GET['type']
		type2 = type1
	except:
		type1 = type2
	if type1 == '4':
		posts_list  = ZhuanTi.objects.order_by('-recentdate').all()
	else:
		posts_list  = ZhuanTi.objects.filter(type=type1).order_by('-recentdate')
	paginator = Paginator(posts_list,10)  #显示20条记录
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	
	t = get_template('zhuanti.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def login(request):
	try:
		name1 = request.GET['username']
		pwd = request.GET['password']
		user = User.objects.get(name=name1)
	except:
		return HttpResponse(simplejson.dumps({'msg':'用户名不存在'}))
	if user is None:
		return HttpResponse(simplejson.dumps({'msg':'用户名不存在'}))
	if user.password != pwd:
		return HttpResponse(simplejson.dumps({'msg':'密码错误'}))
	request.session['iflog'] = True
	request.session['username'] = name1
	request.session['sex'] = user.sex
	request.session['peidui'] = False
	request.session['ifgly'] = user.gly
	return HttpResponse(simplejson.dumps({'msg':'登陆成功'}))
	
def logout(request):
	request.session['iflog']=False
	request.session['username']=False
	request.session['peidui'] = False
	request.session['ifgly']=0
	return HttpResponse(simplejson.dumps({'msg':'注销成功'}))
	
def kong(request):
	return index(request)
	
def guanzhu(request):
	request.session['peidui'] = False
	form = PostForm(request.POST) 
	try:
		name1 = request.session['username']
	except:
		title2 = "请登录！"
		return render_to_response("error1.html",locals());
	try:
		name1 = request.session['username']
		date1 = User.objects.get(name=name1).recentclickdate
		user1 = User.objects.get(name=name1)
		user1.recentclickdate = time.strftime("%Y-%m-%d %X", time.localtime())
		user1.save()
		look = Look.objects.get(name=name1)
		ll = Look.objects.all()
		user_list = list(look.look.values_list('name',flat=True))
		#posts_list = Article.objects.filter(author__name__in=user_list,date__gte=date1,type__in=[1,2,3]).order_by('-date')
		posts_list = Article.objects.filter(author__name__in=user_list,type__in=[1,2,3]).order_by('-date')
	except:
		title2 = "您还没有关注任何人！"
		return render_to_response("error1.html",locals());
	if posts_list == None:
		title2 = "您关注的人没有发表任何点子！"
		return render_to_response("error1.html",locals());
	paginator = Paginator(posts_list,10)
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	t = get_template('blog1.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def bangui(request):
	try:
		request.session['peidui'] = False
	except:
		t = get_template('bangui.html') 
		c = RequestContext(request,locals()) 
		return HttpResponse(t.render(c)) 
	t = get_template('bangui.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def shoucang(request):
	request.session['peidui'] = False
	form = PostForm(request.POST) 
	try:
		user1 = request.session['username']
		posts_list = ShouCang.objects.filter(name=user1)
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	paginator = Paginator(posts_list,10)
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	t = get_template('shoucang.html')
	c = RequestContext(request,locals())
	return HttpResponse(t.render(c))
	
def shoucang2(request):
	form = PostForm(request.POST) 
	try:
		type1 = request.GET['type']
		name1 = request.session['username']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	posts_list2 = ShouCang.objects.filter(name=name1).exclude(title=type1)
	shou1 = ShouCang.objects.get(title=type1,name=name1)
	user_list = list(shou1.article.values_list('id',flat=True))
	posts_list = Article.objects.filter(id__in=user_list).order_by('-date')
	paginator = Paginator(posts_list,5)	#显示20条记录
	paginator2 = Paginator(posts_list2,100)
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	posts2 = paginator2.page(page) 
	t = get_template('shoucang2.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def newshoucang(request):
	try:
		type1 = request.GET['name']
		name1 = request.session['username']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	shou = ShouCang.objects.create(name = name1,
									title = type1)
	return HttpResponse(status=204)
	
def delshoucang(request):
	try:
		type1 = request.GET['name']
		name1 = request.session['username']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	type_list = type1.split(",")
	shou = ShouCang.objects.filter(title__in=type_list,name = name1)
	try:
		shou.delete().all()
	except:
		return HttpResponse(status=204)
	return HttpResponse(status=204)
	
def changeshoucang(request):
	try:
		type1 = request.GET['name1']
		type2 = request.GET['name2']
		name1 = request.session['username']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	shou = ShouCang.objects.get(title=type1,name = name1)
	shou.title = type2
	shou.save()
	return HttpResponse(status=204)
	
def delshoucang2(request):
	try:
		type1 = request.GET['name']
		name1 = request.session['username']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	type_list = type1.split(",")
	shou1 = ShouCang.objects.get(article__id=type_list[0],name = name1)
	shou = Article.objects.filter(id__in=type_list)
	for aa in shou:
		try:
			shou1.article.remove(aa)
		except:
			return HttpResponse(status=204)
	return HttpResponse(status=204)
	
def moveshoucang(request):
	try:
		type1 = request.GET['name']
		name1 = request.session['username']
		mubiao = request.GET['mubiao']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	type_list = type1.split(",")
	shou1 = ShouCang.objects.get(article__id=type_list[0],name = name1)
	shou = Article.objects.filter(id__in=type_list)
	shou2 = ShouCang.objects.get(title=mubiao,name = name1)
	for aa in shou:
		try:
			shou1.article.remove(aa)
			shou2.article.add(aa)
		except:
			return HttpResponse(status=204)
	return HttpResponse(status=204)
	
def newarticle(request):
	try:
		title1 = request.POST['TITLE']
		text1 = request.POST['TEXT']
		type2 = request.POST['TYPE']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	if type2 == u"纪念日、生日" :
		type1 = 1
	if type2 == u"节日" :
		type1 = 2
	if type2 == u"日常" :
		type1 = 3
	wenzhang = Article.objects.create(type = type1,
							sex = request.session['sex'],
							title = title1,
							author = User.objects.get(name=request.session['username']),
							date = time.strftime("%Y-%m-%d %X", time.localtime()),
							recentdate = time.strftime("%Y-%m-%d %X", time.localtime()),
							click = 0,
							reply = 0,
							text = text1
							)
	if wenzhang != None:
		return HttpResponse(status=200)
	else:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
		
def show4(request):
	global id2
	form = PostForm(request.POST)
	try:
		id1 = request.GET['id']
		id2 = id1
		arti = Article.objects.get(id=id1)
	except:
		id1 = id2
		arti = Article.objects.get(id=id1)
	try:
		namee = request.session['username']
	except:
		namee = 0
	id1 = arti.id
	text1 = arti.text
	text1 = tupianchuli(text1)
	arti.text = text1
	arti.save()
	title1 = arti.title
	date1 = arti.date
	author1 = arti.author
	jy = author1.jy
	click1 = arti.click
	posts_list = HuiFu.objects.filter(article__id=id1).order_by('-date')
	posts_list2 = ShouCang.objects.filter(name=namee)
	paginator2 = Paginator(posts_list2,20)
	posts3 = paginator2.page(1)
	paginator = Paginator(posts_list,10)  #显示20条记录
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	dd1 = "none"
	display1 = "none"
	dd2 = "none"
	try:
		xx = Look.objects.get(name=namee).look.all()
		if author1 in xx :
			display1 = "none"
	except:
		display1 = ""
	if namee:
		dd1 = ""
		display1 = ""
		dd2 = "none"
	else:
		dd1 = "none"
		display1 = "none"
	if author1.name == namee:
		display1 = "none"
		if namee == author1.name:
			dd2 = ""
	try:
		gly = request.session['ifgly']
	except:
		gly = 0
	if gly == 1:
		t = get_template('blogadmin.html')
	else:
		t = get_template('blog.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def show5(request):
	global id2
	form = PostForm(request.POST)
	try:
		id1 = request.GET['id']
		id2 = id1
		arti = ZhuanTi.objects.get(id=id1)
	except:
		id1 = id2
		arti = ZhuanTi.objects.get(id=id1)
	id1 = arti.id
	text1 = arti.text
	text1 = tupianchuli(text1)
	arti.text = text1
	arti.save()
	title1 = arti.title
	date1 = arti.date
	author1 = arti.author
	jy = author1.jy
	click1 = arti.click
	posts_list = HuiFu2.objects.filter(zhuanti__id=id1).order_by('-date')
	paginator = Paginator(posts_list,10)  #显示20条记录
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	dd1 = "none"
	display1 = "none"
	try:
		test11 = request.session['username']
	except:
		test11 = False
	if test11:
		dd1 = ""
		display1 = ""
	else:
		dd1 = "none"
		display1 = "none"
	try:
		xx = Look.objects.get(name=request.session['username']).look.all()
		if author1 in xx :
			display1 = "none"
	except:
		display1 = ""
	if author1.name == test11:
		display1 = "none"
	try:
		gly = request.session['ifgly']
	except:
		gly = 0
	t = get_template('blogzt.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def tupianchuli(text1):
	aa = text1.find("tmp/")
	while aa!=-1 :
		bb = aa
		while text1[bb]!="\"":
			bb += 1
		dz = text1[aa+4:bb]
		'%s/%s'%(settings.STATICFILES_DIRS[0],str("media/tmp/"+dz))
		shutil.copy('%s%s'%(settings.STATICFILES_DIRS[0],str("media/tmp/"+dz)), '%s/%s'%(settings.STATICFILES_DIRS[0],str("media/article/")))
		text1 = text1[0:aa]+"article/"+dz+text1[bb:] 
		aa = text1.find("tmp/")
	return text1
	
def newcomment(request):
	try:
		id1 = request.POST['ID']
		text1 = request.POST['TEXT']
		arti = Article.objects.get(id=id1)
		user1 = request.session['username']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	arti.reply += 1
	arti.recentdate = time.strftime("%Y-%m-%d %X", time.localtime())
	arti.save()
	hf = HuiFu.objects.create(name = User.objects.get(name=user1),
							  article = arti,
							  text = text1,
							  date = time.strftime("%Y-%m-%d %X", time.localtime()) 
							  )
	if hf != None:
		return HttpResponse(status=200)
	else:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
		
def newcommentzt(request):
	try:
		id1 = request.POST['ID']
		text1 = request.POST['TEXT']
		arti = ZhuanTi.objects.get(id=id1)
		user1 = request.session['username']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	arti.reply += 1
	arti.recentdate = time.strftime("%Y-%m-%d %X", time.localtime())
	arti.save()
	hf = HuiFu2.objects.create(name = User.objects.get(name=user1),
							  zhuanti = arti,
							  text = text1,
							  date = time.strftime("%Y-%m-%d %X", time.localtime()) 
							  )
	if hf != None:
		return HttpResponse(status=200)
	else:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
		
def click1(request):
	try:
		id1 = request.GET['id']
		arti = Article.objects.get(id=id1)
		name1 = request.session['username']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	if not name1:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	click2 = 0
	try:	
		click2 = Clicked.objects.get(name__name=name1,article=arti)
	except:
		pass
	if click2 == False:
		arti.click +=1
		arti.save()
		click2 = Clicked.objects.create(name=User.objects.get(name=name1),article=arti)
		return  HttpResponse(simplejson.dumps({'msg':'成功'}))
	else:
		return  HttpResponse(simplejson.dumps({'msg':'重复'}))
		
def geren(request):
	request.session['peidui'] = False
	try:
		user1 = User.objects.get(name=request.session['username'])
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	name1 = user1.name
	color1 = user1.color
	guanzhu1 = user1.looknb
	beiguanzhu1 = user1.lookednb
	url1 = user1.iconaddress
	posts_list = Article.objects.filter(author__name=name1,type__in=[1,2,3]).order_by('-date')
	paginator = Paginator(posts_list,10)  #显示20条记录
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	t = get_template('geren.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def geren2(request):
	request.session['peidui'] = False
	try:
		user1 = User.objects.get(name=request.GET['name'])
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	name1 = user1.name
	color1 = user1.color
	guanzhu1 = user1.looknb
	beiguanzhu1 = user1.lookednb
	url1 = user1.iconaddress
	posts_list = Article.objects.filter(author__name=name1,type__in=[1,2,3]).order_by('-date')
	paginator = Paginator(posts_list,10)  #显示20条记录
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	t = get_template('geren2.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def resetgx(request):
	try:
		user1 = User.objects.get(name=request.session['username'])
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	t = get_template('resetgx.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c))
	
def change1(request):
	try:
		pwd1 = request.GET['pwd']
		user1 = User.objects.get(name=request.session['username'])
		user1.password = pwd1
		user1.save()
	except:
		return  HttpResponse(simplejson.dumps({'msg':'失败'}))
	return  HttpResponse(simplejson.dumps({'msg':'成功'}))
	
def jcrop(request):
	try:
		user1 = User.objects.get(name=request.session['username'])
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	return render_to_response('jcrop.html',{})
	
def caijian(request):
	abs_path=settings.STATICFILES_DIRS[0]
	if request.method=='POST':       
		try:
			img=Image.open(abs_path+request.POST['path1'][8:])
		except:
			title2 = "出错了！"
			return render_to_response("error1.html",locals());
		img=img.transform((int(request.POST['w']),int(request.POST['h'])),Image.EXTENT,(int(request.POST['x1']),int(request.POST['y1']),int(request.POST['x2']),int(request.POST['y2']))) 
		img.thumbnail((100, 100))
		file_name=str(time.time())+str(random.random())+request.POST['path1'][-4:]
		img.save(abs_path+"media/icon/"+file_name)
		user1 = User.objects.get(name=request.session['username'])
		user1.iconaddress = "/static/media/icon/"+file_name
		user1.save()
		name1 = user1.name
		sex1 = user1.sex
		guanzhu1 = user1.looknb
		url1 = user1.iconaddress
		beiguanzhu1 = user1.lookednb
		posts_list = Article.objects.filter(author__name=name1).order_by('-date')
		paginator = Paginator(posts_list,10)  #显示20条记录
		try : 
			page = int(request.GET.get('page','1')) 
		except ValueError: 
			page = 1 
		try : 
			posts = paginator.page(page) 
		except (EmptyPage,InvalidPage): 
			posts = paginator.page(paginator.num_pages) 
		t = get_template('geren.html') 
		c = RequestContext(request,locals()) 
		return HttpResponse(t.render(c)) 
		
def liaotian1(request):
	global rs
	if request.method=='POST':
		if request.POST['fangfa'] == '1':
			cache.set("%s%s"%(request.session['username'],cache.get("%s"%request.session['username'])),"%s"%request.POST['hua'])
			cache.incr("%s"%request.session['username'])
			cache.set("q%s"%request.session['username'],"1",10)
			return HttpResponse(simplejson.dumps({'msg':'发送成功'}))
		if request.POST['fangfa'] == '2':
			if request.session['peidui'] == True:
				cc = cache.get("q%s"%cache.get("u%s"%request.session['username']))
				if cc == None:
					request.session['peidui'] = False
					try:
						del rs[request.session['username']]
					except:
						pass
					return HttpResponse(simplejson.dumps({'msg':'断开'}))
				if cache.get("%s"%request.session['username']) == '-1':
					request.session['peidui'] = False
					try:
						del rs[request.session['username']]
					except:
						pass
					return HttpResponse(simplejson.dumps({'msg':'断开'}))
				bb = cache.get("%s"%cache.get("u%s"%request.session['username']))
				if bb != '0':
					neirong = {}
					for aa in range(int(cache.get("%s"%cache.get("u%s"%request.session['username'])))):
						neirong['%s'%aa]=cache.get("%s%s"%(cache.get("u%s"%request.session['username']),aa))
					cache.set("%s"%cache.get("u%s"%request.session['username']),'0')
					cache.set("q%s"%request.session['username'],"1",10)
					return HttpResponse(simplejson.dumps({'msg':neirong}))
				cache.set("q%s"%request.session['username'],"1",10)
				return HttpResponse(simplejson.dumps({'msg':''}))
			else:
				rs[request.session['username']]=1
				if ((cache.get("%s"%request.session['username']) != '-1')and(cache.get("%s"%request.session['username']) != None)and(cache.get("q%s"%cache.get("u%s"%request.session['username'])) != None)):
					request.session['peidui'] = True
					cache.set("q%s"%request.session['username'],"1",10)
					return HttpResponse(simplejson.dumps({'msg':'配对成功'}))
				try:
					mubiao = dengdai.popitem()
				except:
					dengdai['%s'%request.session['username']] = '1'
					cache.set("q%s"%request.session['username'],"1",10)
					return HttpResponse(simplejson.dumps({'msg':'请等待'}))
				if mubiao[0] != request.session['username']:
					cc = cache.get("q%s"%mubiao[0])
					if cc == None:	
						cache.set("q%s"%request.session['username'],"1",10)
						return HttpResponse(simplejson.dumps({'msg':'请等待'}))
					cache.set("%s"%mubiao[0],"0")
					cache.set("%s"%request.session['username'],"0")
					cache.set("u%s"%request.session['username'],"%s"%mubiao[0])
					cache.set("u%s"%mubiao[0],"%s"%request.session['username'])
					request.session['peidui'] = True
					cache.set("q%s"%request.session['username'],"1",10)
					return HttpResponse(simplejson.dumps({'msg':'配对成功'}))
				else:
					cache.set("q%s"%request.session['username'],"1",10)
					dengdai['%s'%request.session['username']] = '1'
					return HttpResponse(simplejson.dumps({'msg':'请等待'}))
		if request.POST['fangfa'] == '3':
			try:
				cache.set("%s"%cache.get("u%s"%request.session['username']),'-1') 
				cache.set("%s"%request.session['username'],'-1')
			except:
				pass
			request.session['peidui'] = False
			try:
				del rs[request.session['username']]
			except:
				pass
			return HttpResponse(simplejson.dumps({'msg':'断开成功'}))
	else:
		try:
			request.session['peidui'] = False
			user2 = User.objects.get(name=request.session['username'])
		except:
			title2 = "出错了！"
			return render_to_response("error1.html",locals());
		rs1 = len(rs.keys())
		return render_to_response('liaotian1.html',locals())
	
def forgetmm(request):
	try:
		yx = request.GET['yx']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	try:
		user1 = User.objects.get(email=yx)
	except:
		user1 = ""
	if user1 != "":
		send_mail(u'浪漫1点--找回密码', u'您的密码：%s'%user1.password, 'langman1dian@hotmail.com',[user1.email],fail_silently=True)
		return HttpResponse(simplejson.dumps({'msg':'您的密码已发送到邮箱。请注意查收。'}))
	return HttpResponse(simplejson.dumps({'msg':'失败'}))
	
def a(request):
	return render_to_response('a.html',{})
	
def jianyi(request):
	try:
		name1 = User.objects.get(name=request.session['username'])
	except:
		name1 = User.objects.get(name="匿名用户")
	text1 = request.POST['jy']
	jianyi1 = Jianyi.objects.create(name=name1,text=text1)
	if jianyi1 != None:
		return HttpResponse(status=204)
	else:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
		
def guanzhu1(request):
	try:
		user1 = User.objects.get(name=request.GET['id'])
		user2 = User.objects.get(name=request.session['username'])
		try:
			look1 = Look.objects.get(name=user2.name)
		except:
			look1 = Look.objects.create(name=user2.name)
		if user1 in look1.look.all():
			return HttpResponse(simplejson.dumps({'msg':'您已关注过TA!'}))
		look1.look.add(user1)
		look1.save()
		try:
			look2 = Looked.objects.get(name=user1.name)
		except:
			look2 = Looked.objects.create(name=user1.name)
		look2.looked.add(user2)
		look2.save()
		user1.lookednb += 1
		user1.save()
		user2.looknb += 1
		user2.save()
		return HttpResponse(simplejson.dumps({'msg':'关注成功'}))
	except:
		return HttpResponse(simplejson.dumps({'msg':'关注失败'}))
		
def guanzhu2(request):
	request.session['peidui'] = False
	form = PostForm(request.POST) 
	try:
		name1 = request.session['username']
	except:
		title2 = "请登录！"
		return render_to_response("error1.html",locals());
	try:
		look1 = Look.objects.get(name=name1)
		posts_list = look1.look.all()
	except:
		title2 = "您还没有关注任何人！"
		return render_to_response("error1.html",locals());
	paginator = Paginator(posts_list,10)
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	t = get_template('guanzhu1.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def beiguanzhu2(request):
	request.session['peidui'] = False
	form = PostForm(request.POST) 
	try:
		name1 = request.session['username']
	except:
		title2 = "请登录！"
		return render_to_response("error1.html",locals());
	try:
		look1 = Looked.objects.get(name=name1)
		posts_list = look1.looked.all()
	except:
		title2 = "您还没有被任何人关注！"
		return render_to_response("error1.html",locals());
	paginator = Paginator(posts_list,10)
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	t = get_template('guanzhu2.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c))
	
def qxgz(request):
	try:
		name1 = request.GET['name1']
		user1 = User.objects.get(name=name1)
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	user2 = User.objects.get(name=request.session['username'])
	user2.looknb -= 1
	user2.save()
	look1 = Look.objects.get(name=user2.name)
	look1.look.remove(user1)
	look1.save()
	look2 = Looked.objects.get(name=user1.name)
	look2.looked.remove(user2)
	look2.save()
	user1.lookednb -= 1
	user1.save()
	return HttpResponse(status=204)
	
def addshoucang1(request):
	try:
		name1 = request.session['username']
	except:
		return HttpResponse(simplejson.dumps({'msg':'请登录！'}))
	arti1 = Article.objects.get(id=request.GET['id'])
	sc1 = ShouCang.objects.get(name=name1,title=request.GET['sc'])
	sc1.article.add(arti1)
	return HttpResponse(simplejson.dumps({'msg':'成功'}))
	
def shantie(request):
	arti1 = Article.objects.get(id=request.GET['id'])
	arti1.type = 4
	arti1.save()
	return HttpResponse(status=204)
	
def jinyan(request):
	user1 = User.objects.get(name=request.GET['name1'])
	user1.feng = 1
	user1.jy = "none"
	user1.save()
	return HttpResponse(status=204)
	
def guide(request):
	request.session['guide'] = True
	return HttpResponse(status=204)
	
def gonggao(request):
	request.session['peidui'] = False
	form = PostForm(request.POST) 
	posts_list  = GongGao.objects.all().order_by('-date')
	paginator = Paginator(posts_list,10)  #显示20条记录
	try : 
		page = int(request.GET.get('page','1')) 
	except ValueError: 
		page = 1 
	try : 
		posts = paginator.page(page) 
	except (EmptyPage,InvalidPage): 
		posts = paginator.page(paginator.num_pages) 
	t = get_template('gonggao.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 

def gonggao2(request):
	form = PostForm(request.POST)
	try:
		id1 = request.GET['id']
		arti = GongGao.objects.get(id=id1)
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	id1 = arti.id
	text1 = arti.text
	text1 = tupianchuli(text1)
	arti.text = text1
	arti.save()
	title1 = arti.title
	date1 = arti.date
	author1 = arti.author
	jy = author1.jy
	t = get_template('gonggao2.html') 
	c = RequestContext(request,locals()) 
	return HttpResponse(t.render(c)) 
	
def editor2(request):
	try:
		user1 = User.objects.get(name = request.session['username'])
	except:
		title2 = "请登录！"
		return render_to_response("error1.html",locals());
	if user1.feng == 1:
		title2 = "对不起！您已被禁言！"
		return render_to_response("error1.html",locals());
	form = PostForm(request.POST)
	try:
		request.session['peidui'] = False
		hh = request.GET['hh']
		id1 = request.GET['id1']
		arti1 = Article.objects.get(author=user1,id=id1)
		title1 = arti1.title
		text1 = arti1.text
		text1 = re.sub(r'</?\w+[^>]*>','',text1)  
		text1 = replaceCharEntity(text1)
		return render_to_response('editor2.html',locals())
	except:
		title2 = "请登录！"
		return render_to_response("error1.html",locals())
		
def replaceCharEntity(htmlstr):    
	CHAR_ENTITIES={'nbsp':' ','160':' ','lt':'<','60':'<','gt':'>','62':'>','amp':'&','38':'&','quot':'"','34':'"',}    
	re_charEntity=re.compile(r'&#?(?P<name>\w+);')    
	sz=re_charEntity.search(htmlstr)
	while sz:        
		entity=sz.group()#entity全称，如&gt;        
		key=sz.group('name') #去除&;后entity,如&gt;为gt
		try:            
			htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)            
			sz=re_charEntity.search(htmlstr)
		except KeyError:#以空串代替            
			htmlstr=re_charEntity.sub('',htmlstr,1)            
			sz=re_charEntity.search(htmlstr)
	return htmlstr
		
def changearticle(request):
	try:
		id1 = request.POST['id1']
		title1 = request.POST['TITLE']
		text1 = request.POST['TEXT']
		type2 = request.POST['TYPE']
	except:
		title2 = "出错了！"
		return render_to_response("error1.html",locals());
	if type2 == u"纪念日、生日" :
		type1 = 1
	if type2 == u"节日" :
		type1 = 2
	if type2 == u"日常" :
		type1 = 3
	arti1 = Article.objects.get(id=id1)
	arti1.text = text1
	arti1.type = type1
	arti1.title = title1
	arti1.save()
	return HttpResponse(status=200)
