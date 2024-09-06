from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import shutil
import uvicorn
import os

app = FastAPI()

UPLOAD_DIRECTORY = "uploaded_images"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return JSONResponse(content={"filename": file.filename, "filepath": filepath})

@app.get("/getimage")
def get_image(imagename: str):
    filepath = os.path.join("uploaded_images", imagename)
    if os.path.exists(filepath):
        #If thefile exists, this line returns FileResponseobject.FileResponse is a FastAPI
        #class used to return a file as a response.It streams the
        #file to the client who made the request, allowing them to download or view the image.
        return FileResponse(filepath)
    else:
        raise HTTPException(status_code=404, detail="Image not found")




@app.delete("/delete")
def deleteimage(name:str):
    path=os.path.join("uploaded_images",name)
    if path:
        os.remove(path)
        return JSONResponse(content={name:"was deleted"})
    return "nothing was found"



@app.get("/allimages")
def getallimage():
    files=os.listdir(UPLOAD_DIRECTORY)
    if files:
        return JSONResponse(content={"images":files})
    return {"error":"error occured"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

