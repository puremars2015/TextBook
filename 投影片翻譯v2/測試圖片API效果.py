import base64
from openai import OpenAI
client = OpenAI()

prompt = """
Replace all Chinese text in this image with Thai text. Keep everything else exactly the same - same colors, same layout, same design, same images. Only change the text from Chinese to Thai.
"""

result = client.images.edit(
    model="gpt-image-1",
    image=[
        open("image.png", "rb")
    ],
    prompt=prompt
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("converted.png", "wb") as f:
    f.write(image_bytes)
