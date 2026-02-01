from conftest import SQLALCHEMY_DATABASE_URL
def test_create_user(client):
    print("Test_DB_url: ", SQLALCHEMY_DATABASE_URL)
    data = {"email":"testuser@nofoobar.com","password":"testing"}
    response = client.post("/users",json=data)
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True

def test_create_user_bad_data(client):
    data = {"email":"testuser#nofoobar.com","password":"testing"}
    response = client.post("/users",json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid email address: An email address must have an @-sign."
    assert response.json()["detail"][0]["input"] == "testuser#nofoobar.com"

