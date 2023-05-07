from google.cloud import vision

client = vision.ImageAnnotatorClient()
response = client.annotate_image({
  'image': {'source': {'image_uri': 'gs://my-test-bucket/image.jpg'}},
  'features': [{'type_': vision.Feature.Type.FACE_DETECTION}]
})
