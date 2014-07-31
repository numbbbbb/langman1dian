import re

class IgnoreCrsfMiddleware(object):
	def process_request(self,request, **karg):
		if re.match(r'^/image/imageUp/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/sb/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/signup/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/login/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/shoucang2/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/newarticle/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/changearticle/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/newcomment/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/newcommentzt/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/image/imageUp2/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/caijian/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/liaotian1/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^/jianyi/?$',request.path):
			request.csrf_processing_done = True
			return None
		if re.match(r'^validate/?$',request.path):
			request.csrf_processing_done = True
			return None
