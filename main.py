import dropbox
from dropbox.exceptions import ApiError, AuthError
from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os


app = FastAPI()



APP_KEY = "ex4dfq9bymy0b5l"
APP_SECRET = "tvcezmnq4z8tkpn"
ACCESS_TOKEN = "sl.u.AF4XBN_9iiuTbZtkfMIyU-GOFBcyGNFWpcW9MDiguca9x-3NPbthZismFD6xsgde_va34C54TK83gAeDKhsV_0N1QB-X7iN8w6QUe_ERELsJEj8OuZSql1j6AhY6CLjy6-789_4gPPEsqU9GPqZQxI-LXswTp5j0B9_FLfLaeCMY_EQ5t5vCv4lMSvJDGJENIOQE1rP2kYkayxjzhhcwDp741UDQeaJofeHU9M1YFUhHb6vWnO3LeWtz6u2KEVZVDNT6LdalDol4AhhY6Ao7PhmRXAx2-Fe3echEDjmpNaJWBM7XgHLjgOI0WkcGbC5IrLJ7Sx4ZZguzk4ebJ8nQNUptpdMTu-BRlKWHnG0qBoni9cOsgyTVFqf9yGgbk4Ie-PrNznvx3VMdGjQ7wo9hFl5eWrp9ApbT3tOCJfPTzL-wfKXta6_Myw6NALX6unWdPHTlanUyTpvREjwsN4B3st2ohTTnPKckZ7vfnrAYLG2bmVliEOQqsMr3iM-HALIKFxhSNCemUFct7NPjiWcbgIbvgkrsQcdBNkYj-rA7d6nUfoR6ljNaD2Ys_auxhJxs_T8vzAciHgO0NGbfV-YDDF61DyCbgjzI3kwFA8JpBUjcLTGQ6NQrabvUyaSyIjeVle6xecdaR7n-qeleTrmPSPY4ZWvr1nSYvTrid0A2Ib3Co_zexq4Nqx1zxpxj_NGZ95ocE8ywePIDAzkptGcgHEcM8VOM0rLnzkh_7Y_Utmoa3LCaQR5UvMaFi6IyVZyCm5yfCDa0J7lu29Lqp3IoV7ISDOcbks4rJx1DH-atZ25ts57PPgy4KN1vIVc3ERfc1PkKAK_nCSrcspCzPEKxtiU1RBKMqTPaqYr5YQD1olYku-xvi884aZfCUqc4pjyKMCHm54EzWgAqHun-4WNeGB6sR5lfBb51BuzfmjYbCbZZiUrP2OmqN2k0RJ8AjoN4lgxLUKY0U5hSzb0jKIoWWwhVEqgfblOvsQbVxEIVp2lM24ql6aQb3PrMvw5fMi6ol-u_chKfbQmW1bCzu9HkAv7okQmH_Rr9RPtudKB_xC8h5Rk2e1B2M2PVWnktKHr8yH5GHKVtCJuDLgpg97deR9PMH8utDnZAEX5stRVI5Wu5cybDjAFE6ThsaGMnZhT4F5uJOFoh_i8ZDpiuMJz3K0j1KYUV28fdw65j2e2oAFV3I2EHS-aUKOn4CAP_KzmtgGvi5_N3cnayhk-GcgbKvma6DLCqMPcvSz5VwGKupSPfnOnZ5hI20SX-xlDChiUmV2GM9O9E865E69f-8xvq729MLETVpaZYe_rFz0v8ulE1-HxUhEPQlSO40JfcDBzgfKn_X7k00pEcdkxZ-VwdtWF_HYN9BiSycDsX7DuOYRHLRzZFmqTw9rBFf4gDKPDO46SwcmwwW4PiDTLWjL1CZ0_NCPQl7s1XKQA1O5wG47LO7Q"
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