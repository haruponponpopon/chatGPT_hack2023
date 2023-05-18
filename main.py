import os
import openai
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from typing import Annotated
import shutil

openai.api_key = os.environ['OPENAI_API_KEY']


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
  messages = [{"role": "user", "content": prompt}]
  response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=
    temperature,  # this is the degree of randomness of the model's output
  )
  return response.choices[0].message["content"]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
  return {"message": "Hello World"}


class Item(BaseModel):
  json_str: str


@app.post("/json2html")
async def json2html(item: Item):
  _json = item.json_str
  prompt = "以下のJSONをHTMLに変換してください。:\n" + str(_json)
  html = get_completion(prompt)
  return html


class Item2(BaseModel):
  command: str
  html: str


@app.post("/paint")
async def paint(item: Item2):
  command = item.command
  html = item.html
  prompt = f"""
  以下のhtmlに、以下の「操作」を加えたhtmlを出力してください。
  
  html: {html}
  操作: {command}
  """
  html = get_completion(prompt)
  return html


class Item3(BaseModel):
  email_str: str

@app.post("/replyEmail")
async def replyEmail(item: Item3):
  email = item.email_str
  prompt = "以下の文章に対する返信を記述してください。:\n" + str(email)
  html = get_completion(prompt)
  return html

# @app.post("/upload_audio")
# async def upload_audio(file: Annotated[bytes, File()]):
#   audio_file = file.file
#   transcript = openai.Audio.transcribe("whisper-1", audio_file)
#   print(transcript)

#   return {"filename": file.filename}


@app.post("/upload_audio")
async def fileupload_post(request: Request):
  '''docstring
    アップロードされたファイルを保存する
    '''
  form = await request.form()
  for formdata in form:
    uploadfile = form[formdata]
    file_temp = uploadfile.file.read()
    # file = open("data/test.audio", mode="w")
    with open("data/test.mp3", "wb+") as f:
      f.write(file_temp)
    with open("data/test.mp3", "rb") as f:
      transcript_text = openai.Audio.transcribe("whisper-1", f)["text"]
    response = get_completion(transcript_text)
  return {"transcript": transcript_text, "response": response}


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
