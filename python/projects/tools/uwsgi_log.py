text = '''
%(uri) -> REQUEST_URI
%(method) -> REQUEST_METHOD
%(user) -> REMOTE_USER
%(addr) -> REMOTE_ADDR
%(host) -> HTTP_HOST
%(proto) -> SERVER_PROTOCOL
%(uagent) -> HTTP_USER_AGENT
%(referer) -> HTTP_REFERER
%(status) -> HTTP_RESPONSE_CODE
%(micros) -> HTTP_RESPONSE_MICROSECS
%(msecs) -> HTTP_RESPONSE_MILISECS
%(secs) -> HTTP_RESPONSE_MICROSECS
%(time) -> timestamp_start_request
%(ctime) -> ctime_start_request
%(epoch) -> time_Unix_format
%(size) -> response_size
%(hsize) -> response_headers_size
%(rsize) -> response_body_size
%(cl) -> request_content_body_size
%(pid) -> pid
%(wid) -> wid
%(core) -> core
%(vszM) -> virtual_memory_usage_mb
%(rssM) -> rss_memory_usage_mb
%(pktsize) -> internal_request_uwsgi_packet_size
%(rerr) -> num_read_error
%(werr) -> num_write_error
%(ioerr) -> num_io_error
%(headers) -> num_generated_response_headers
'''

val = [x.strip() for x in text.split('\n') if x.strip()]
key = []
value = []
log_format = '{key}="{value}"'
log = []
for x in val:
    x = x.split('->')
    _value = x[0].strip()
    value.append(_value)
    _key = x[1].lower().strip()
    key.append(_key)
    log.append(log_format.format(key=_key, value=_value))

final = dict(zip(key, value))

print(', '.join(log))

print(', '.join(final.keys()))
# print(final)
