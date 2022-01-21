from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def app_start(self):
        self.client.get("/city/list")
        self.client.get("/offer/banner")
        self.client.get("/service/tag/list")
        self.client.get("/store/list/bang")
    
    @task
    def vehicle_list(self):
        self.client.get("/vehicle/type/list")
        self.client.get("/vehicle/wheel/list")
    
    # @task
    # def external_attack(self):
    #     self.client.post('/consumer/login/checkOTP/', data={
    #         'phone': '+918989820993',
    #         'otp': '1234',
    #         'token': '123456789'
    #     })