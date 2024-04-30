import httpx

response_post = httpx.post('https://httpbin.org/post', data={'key': 'value'})
response_post_json = response_post.json()
print(response_post_json)


response_get = httpx.get('https://httpbin.org/get', headers={'key': 'value'})
response_get_json = response_get.json()
print(response_get_json)
