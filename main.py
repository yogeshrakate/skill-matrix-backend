# from src.Api.views.view import app
# from src.urls import urls_dict

from fastapi import FastAPI

from src.Api.views import view, admin_view

app = FastAPI()

app.include_router(view.router)
app.include_router(admin_view.router)


# class Setup:
#     def __init__(self,app,url_dict) -> None:
#         self.url_dict=url_dict
#         #self.host=host
#         self.app=app
#         self.non_auth = ["user_singup"]

#     def intialise(self):
#         for route in self.url_dict['get']:
#             self.app.get(route)
#         for route in self.url_dict['post']:
#             self.app.post(route)
#         # return self.app
#         self.app.middleware("http") (self.auth_middleware())
    
#     def auth_middleware(self):
#         print("-----------------middle----------------")


# if __name__=="__main__":
#     runner=Setup(app,urls_dict)
#     app=runner.intialise()
#     import uvicorn
#     uvicorn.run(app,host="0.0.0.0",port=8000)
