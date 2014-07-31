# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import validate,signup,checkuser,editor,imageUp,index,yzm,show,login,logout,kong,show2,shoucang,guanzhu,bangui,shoucang,shoucang2,newshoucang,delshoucang,changeshoucang,delshoucang2,moveshoucang,newarticle,show4,newcomment,click1,geren,resetgx,change1,jcrop,imageUp2,caijian,liaotian1,checkemail,forgetmm,a,jianyi,guanzhu1,guanzhu2,beiguanzhu2,qxgz,addshoucang1,shantie,jinyan,geren2,show5,newcommentzt,guide,gonggao,gonggao2,editor2,changearticle
from django.conf.urls.static import static 
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^validate/$',validate), 
	(r'^onlygodknowadmin/',include(admin.site.urls)),
	(r'^signup/$',signup),
	(r'^checkuser/$',checkuser),
	(r'^editor/$',editor),
	(r'^image/imageUp/$',imageUp),
	(r'^image/imageUp2/$',imageUp2),
	(r'^$',index),
	(r'^yzm/$',yzm),
	(r'^show/$',show),
	(r'^show2/$',show2),
	(r'^shoucang/$',shoucang),
	(r'^guanzhu/$',guanzhu),
	(r'^login/$',login),
	(r'^logout/$',logout),
	(r'^bangui/',bangui),
	(r'^shoucang/$',shoucang),
	(r'^shoucang2/$',shoucang2),
	(r'^newshoucang/$',newshoucang),
	(r'^delshoucang/$',delshoucang),
	(r'^changeshoucang/$',changeshoucang),
	(r'^delshoucang2/$',delshoucang2),
	(r'^moveshoucang/$',moveshoucang),
	(r'^newarticle/$',newarticle),
	(r'^show4/$',show4),
	(r'^newcomment/$',newcomment),
	(r'^click1/$',click1),
	(r'^geren/$',geren),
	(r'^geren2/$',geren2),
	(r'^resetgx/$',resetgx),
	(r'^change1/$',change1),
	(r'^jcrop/$',jcrop),
	(r'^caijian/$',caijian),
	(r'^liaotian1/$',liaotian1),
	(r'^checkemail/$',checkemail),
	(r'^forget/$',forgetmm),
	(r'^jianyi/$',jianyi),
	(r'^guanzhu1/$',guanzhu1),
	(r'^guanzhu2/$',guanzhu2),
	(r'^beiguanzhu2/$',beiguanzhu2),
	(r'^qxgz/$',qxgz),
	(r'^addshoucang1/$',addshoucang1),
	(r'^shantie/$',shantie),
	(r'^jinyan/$',jinyan),
	(r'^a/$',a),
	(r'^show5/$',show5),
	(r'^newcommentzt/$',newcommentzt),
	(r'^guide/$',guide),
	(r'^gonggao/',gonggao),
	(r'^gonggao2/',gonggao2),
	(r'^editor2/$',editor2),
	(r'^changearticle/$',changearticle),
	(r'^',kong),
	(r'$',kong),
	(r'^static/(?P<path>.*)$','django.views.static.serve'),
    # Examples:
    # url(r'^$', 'langman1dian.views.home', name='home'),
    # url(r'^langman1dian/', include('langman1dian.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
#urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT ) 
#urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )

