from flask import Response
import json
def response(msg = {}, status=200):
	print msg
	print status
	resp = Response(
		response=json.dumps(msg),
	    status=status, 
	    content_type="application/json"
	)
	return resp