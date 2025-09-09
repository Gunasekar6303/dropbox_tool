import dropbox
from dropbox.exceptions import ApiError, AuthError
from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os


app = FastAPI()



APP_KEY = "please add your app APP_KEY here"
APP_SECRET = "please add your app APP_SECRET here"
ACCESS_TOKEN = "please add your app ACCESS_TOKEN here"
dbx = dropbox.Dropbox(
    oauth2_refresh_token=ACCESS_TOKEN,
    app_key=APP_KEY,
    app_secret=APP_SECRET
)



class DropboxService:
    def __init__(self, access_token: str):
        try:
            self.dbx = dropbox.Dropbox(access_token)
            self.dbx.users_get_current_account()
            print("✅ Dropbox authentication successful.")
        except AuthError as e:
            raise Exception("❌ Dropbox authentication failed.") from e

    def upload_file(self, local_path: str, dropbox_path: str):
        with open(local_path, "rb") as f:
            self.dbx.files_upload(
                f.read(),
                dropbox_path,
                mode=dropbox.files.WriteMode.overwrite,
            )

    def download_file(self, dropbox_path: str, local_path: str):
        metadata, res = self.dbx.files_download(dropbox_path)
        with open(local_path, "wb") as f:
            f.write(res.content)

    def list_files(self, folder: str = ""):
        response = self.dbx.files_list_folder(folder)
        return [entry.name for entry in response.entries]


# Initialize service
dropbox_service = DropboxService(ACCESS_TOKEN)


@app.post("/dropbox/{action}")
async def dropbox_action(action: str, body: DropboxService):
    print("Params:", body.params)
    print("Credentials:", body.credentials)

    return {"action": action, "params": body.params}
