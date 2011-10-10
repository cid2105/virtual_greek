import S3_class as S3

AWS_ACCESS_KEY_ID = 'AKIAJVJFVRKY6F6Q3TSA'
AWS_SECRET_ACCESS_KEY = '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'
conn = S3.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
generator = S3.QueryStringAuthGenerator(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
def save_s3_data(key, data, bucket_name, content_type):
  print key +  " " + bucket_name + " " + content_type
  conn.put(
    bucket_name,
    key,
    S3.S3Object(data),
    { 'x-amz-acl': 'public-read' , 'Content-Type': content_type }
  )
  return key

def delete_s3_data(bucket_name, key):
  return conn.delete(bucket_name, key)
def get_s3_url(bucket_name, key):
  return generator.make_bare_url(bucket_name, key)