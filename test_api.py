import unittest
from app import create_app
from config import TestConfig
from exts import db


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        # self.app.testing = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            #db.init_app(self.app)
            
            db.create_all()
            

        
    def test_signup(self):
        
        signup_response=self.client.post('/auth/signup',
            json={"username":"testuser",
                  "phone_number":"123",
                  "email":"testuser@example.com",
                  "password":"password"}
        ) 
        
        status_code = signup_response.status_code 
        
        self.assertEqual(status_code, 201)
                 
    def test_login(self):
        
        signup_response=self.client.post('/auth/signup',
            json={"username":"testuser",
                  "phone_number":"123",
                  "email":"testuser@example.com",
                  "password":"password"}
        ) 
        
        login_response=self.client.post('/auth/login',
            json={"username":"testuser",
                  "password":"password"}
        )
        
        status_code = login_response.status_code 
        
        json=login_response.json
        #print(json)
              
        self.assertEqual(status_code, 200)   
        
    def test_get_all_itineraries(self):

        response = self.client.get('/itinerary/itinerary')
        #print (response.json)
        
        status_code = response.status_code
        
        self.assertEqual(status_code, 200)
         
        
    def test_get_one_itinerary(self):
        id=1
        
        response = self.client.get(f'/itinerary/itinerary/{id}')
        
        status_code = response.status_code
        
        self.assertEqual(status_code, 404)
        #print(status_code)
    
    def test_create_itinerary(self):
        signup_response=self.client.post('/auth/signup',
            json={"username":"testuser",
                  "phone_number":"123",
                  "email":"testuser@example.com",
                  "password":"password"}
        ) 
        
        self.assertEqual(signup_response.status_code, 201)
        
        login_response=self.client.post('/auth/login',
            json={"username":"testuser",
                  "password":"password"}
        )
        
        self.assertEqual(login_response.status_code, 200)
        
        access_token = login_response.json["access_token"]

        create_itinerary_response = self.client.post(
        '/itinerary/itinerary',
        json={
            "title": "Archery",
            "user_id": 1,
            "destination": "Cookie Island",
            "details": "A cookie island in a bustling city.",
            "date": "2022-01-01"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
        status_code = create_itinerary_response.status_code
        response_json = create_itinerary_response.json
        #print(response_json)
        
        self.assertEqual(status_code, 201)
  
    def test_update_itinerary(self):
        signup_response=self.client.post('/auth/signup',
            json={"username":"testuser",
                  "phone_number":"123",
                  "email":"testuser@example.com",
                  "password":"password"}
        ) 
        
        self.assertEqual(signup_response.status_code, 201)
        
        login_response=self.client.post('/auth/login',
            json={"username":"testuser",
                  "password":"password"}
        )
        
        self.assertEqual(login_response.status_code, 200)
        
        access_token = login_response.json["access_token"]

        create_itinerary_response = self.client.post(
        '/itinerary/itinerary',
        json={
            "title": "Archery",
            "user_id": 1,
            "destination": "Cookie Island",
            "details": "A cookie island in a bustling city.",
            "date": "2022-01-01"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
        status_code = create_itinerary_response.status_code
        
        id=1
        update_response = self.client.put(
            f'/itinerary/itinerary/{id}',
            json={
                "title": "Archery Update",
                "user_id": 1,
                "destination": "Cookie Island Updated",
                "details": "A cookie island in a bustling city. Updated",
                "date": "2022-01-02"
            },
            headers={"Authorization": f"Bearer {access_token}"}
            )
        status_code = update_response.status_code
        self.assertEqual(status_code, 200)
        print (update_response.json)           
        

    
    def test_delete_itinerary(self):
        signup_response=self.client.post('/auth/signup',
            json={"username":"testuser",
                  "phone_number":"123",
                  "email":"testuser@example.com",
                  "password":"password"}
        ) 
        
        self.assertEqual(signup_response.status_code, 201)
        
        login_response=self.client.post('/auth/login',
            json={"username":"testuser",
                  "password":"password"}
        )
        
        self.assertEqual(login_response.status_code, 200)
        
        access_token = login_response.json["access_token"]

        create_itinerary_response = self.client.post(
        '/itinerary/itinerary',
        json={
            "title": "Archery",
            "user_id": 1,
            "destination": "Cookie Island",
            "details": "A cookie island in a bustling city.",
            "date": "2022-01-01"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
        id = 1
        delete_itinerary_response = self.client.delete(
            f'/itinerary/itinerary/{id}',
            headers={"Authorization": f"Bearer {access_token}"}
            
        )    
        status_code = delete_itinerary_response.status_code
        
        print (delete_itinerary_response.json)
        
        self.assertEqual(status_code, 200)    

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
            
if __name__ == "__main__":
    unittest.main()            