import uvicorn
import threading
from AttendanceSystem.main import run as app_run

if __name__=="__main__":
    app = threading.Thread(target=app_run)
    app.start()
    uvicorn.run("api.api:app", reload=True)