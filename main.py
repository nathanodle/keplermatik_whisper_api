#
#     Copyright (C) 2019-present Nathan Odle
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the Server Side Public License, version 1,
#     as published by MongoDB, Inc.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     Server Side Public License for more details.
#
#     You should have received a copy of the Server Side Public License
#     along with this program. If not, email mysteriousham73@gmail.com
#
#     As a special exception, the copyright holders give permission to link the
#     code of portions of this program with the OpenSSL library under certain
#     conditions as described in each individual source file and distribute
#     linked combinations including the program with the OpenSSL library. You
#     must comply with the Server Side Public License in all respects for
#     all of the code used other than as permitted herein. If you modify file(s)
#     with this exception, you may extend this exception to your version of the
#     file(s), but you are not obligated to do so. If you do not wish to do so,
#     delete this exception statement from your version. If you delete this
#     exception statement from all source files in the program, then also delete
#     it in the license file.
import shutil

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import whisper
import uvicorn
from fastapi.responses import JSONResponse
import requests
import json

app = FastAPI()
whisper_model_size = 'large-v2'
model = whisper.load_model(whisper_model_size)
satellite_prompt = ""

# api-endpoint
URL = "http://192.168.1.2:8001/satellite_list"

# sending get request and saving the response as response object
r = requests.get(url=URL)

# extracting data in json format
json_data = json.loads(r.text)
# print(json_data)
satellite_list = json_data

for satellite in satellite_list:
    satellite_prompt += f"{satellite}, "
# print(self.satellite_list)

prompt = satellite_prompt + " iss, picsat, horyu-4"

if __name__ == "__main__":
    config = uvicorn.Config("main:app", host="192.168.1.2", port=8002, log_level="info")
    server = uvicorn.Server(config)
    server.run()


@app.get("/status/")
async def status_request():
    status = "active"
    return status

@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    # Change here to LOGGER
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.post("/transcribe")
def upload(file: UploadFile = File(...)):
    try:
        result = ""
        with open(file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        result = model.transcribe(file.filename, fp16=False, language='en', task='transcribe', initial_prompt=prompt)
        print(result)

        return {"transcription_result": result}

    except Exception as e:
        print(e)
        return {"message": "There was an error uploading the file"}

    finally:
        file.file.close()

    #return {"message": f"Successfully uploaded {file.filename}"}