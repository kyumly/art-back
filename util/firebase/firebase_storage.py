import google.api_core.exceptions
from firebase_admin import credentials, initialize_app, storage

class FirebaseCustom:
    cred = credentials.Certificate("util/firebase/serviceAccountKey.json")
    default_app = initialize_app(cred, {
        'storageBucket': 'test-27776.appspot.com'  # gs://가 없는 경로 - 붙이면 에러남
    })
    bucket = storage.bucket()



    def __init__(self, file, uuid):
        """
        file : 파일
        file_name : 파일 이름
        file_uuid : 사용자 고유 아이디
        content_type : 파일 확장자명
        """
        self.file = file
        self.file_name = file.name
        self.uuid = uuid
        self.content_type = file.content_type

    def uploadFirebase(self, user_uuid):
        """
        파이어베이스 파일 업로드
        """
        path = f"art/{self.uuid}/{self.file_name}"
        blob = self.bucket.blob(path)
        metadata = {"firebaseStorageDownloadTokens": self.uuid} #access token이 필요하다.
        blob.metadata = metadata
        blob.upload_from_file(self.file, content_type=self.content_type)

        path = f'{blob.path}?alt=media&token={self.uuid}'
        return path

    @staticmethod
    def deleteFirebase(uuid, filename):
        """
        파이어베이스 파일 업로드
        """
        path = f"art/{uuid}/{filename}"

        bucket = storage.bucket()
        blob = bucket.blob(path)
        metadata = {"firebaseStorageDownloadTokens": uuid} #access token이 필요하다.
        blob.metadata = metadata
        try :
            delete = blob.delete()
            return True
        except google.api_core.exceptions.NotFound:
            print("첨부파일 삭제 에러")
            return 400


    @staticmethod
    def getFirebase(path):
        """
        파일 가져오기
        """
        url = 'https://firebasestorage.googleapis.com/v0'
        url_path = f"{url}{path}"

        return url_path

    def setFile(self, path, uuid):
        pass
