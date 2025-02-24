from fastapi.testclient import TestClient
from main import app  # Replace with your FastAPI app import

client = TestClient(app)

def test_get_profile_with_token():
    # Example token (you should use a valid token here)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0M0BnbWFpbC5jb20iLCJleHAiOjE3NDAzOTE2NjJ9.n0foZ35daNu_fXCZQE-ntLGJIH3nj-0VWsQu4WOzFKI"
    
    # Send a GET request with the Authorization header
    response = client.get("/profile", headers={"Authorization": f"Bearer {token}"})
    
    # Check if the response is successful
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Hello" in response.json()["message"]

def test_get_profile_with_cookie():
    # Simulate a cookie (your cookie should have the proper token)
    cookies = {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0M0BnbWFpbC5jb20iLCJleHAiOjE3NDAzOTE2NjJ9.n0foZ35daNu_fXCZQE-ntLGJIH3nj-0VWsQu4WOzFKI"}
    
    # Send a GET request with the cookie
    response = client.get("/profile", cookies=cookies)
    
    # Check if the response is successful
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Hello" in response.json()["message"]
