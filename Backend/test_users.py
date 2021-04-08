import config
config.database = "test_data_base.sqlite"
#config.database = "data_base.sqlite"

from main import app
from fastapi.testclient import TestClient
from fastapi import Form
import pytest

client = TestClient(app)


#################################################### TEST REGISTER ENDPOINT ####################################################

def test_register_OK_user():
  """
  this user will be use in other tests that include login
  """
  response = client.post(
        "/users/",
          json = { 
                "userIn_email": "knd@a.com", 
                "userIn_password": "12345678", 
                "userIn_username": "Argentina"
                }
        )
  assert response.status_code == 201
  assert response.json() == {"userOut_username":"Argentina",
                          "userOut_email": "knd@a.com",
                          "userOut_operation_result": " Succesfully created!"}

def test_register_with_email_exists_user():
  response = client.post(
        "/users/",
          json = { 
                "userIn_email": "knd@a.com", 
                "userIn_password": "12345678", 
                "userIn_username": "Argentina"
                }
        )
  assert response.status_code == 409
  assert response.json()["detail"] == "Email already registered"

def test_register_email_exists_user():
  response = client.post(
        "/users/",
          json = { 
                "userIn_email": "knd@a.com", 
                "userIn_password": "12345678", 
                "userIn_username": "Argentina"
                }
        )
  assert response.status_code == 409
  assert response.json()["detail"] == "Email already registered"

def test_register_user_exists_user():
  response = client.post(
        "/users/",
          json = { 
                "userIn_email": "knd@a.com", 
                "userIn_password": "12345678", 
                "userIn_username": "Argentina"
                }
        )
  assert response.status_code == 409
  assert response.json()["detail"] == "Username already registered"

def test_register_user_exists_user():
  response = client.post(
        "/users/",
          json = { 
                "userIn_email": "qonda@a.com", 
                "userIn_password": "12345678", 
                "userIn_username": "Argentina"
                }
        )
  assert response.status_code == 409
  assert response.json()["detail"] == "Username already registered"


def test_register_short_username():
  response = client.post(
        "/users/",
          json = { 
                "userIn_email": "qonda1@a.com", 
                "userIn_password": "12345678", 
                "userIn_username": "jaj"
                }
        )
  assert response.status_code == 400
  assert response.json()["detail"] == "Can't parse username"


def test_register_long_username():
  response = client.post(
        "/users/",
          json = { 
                "userIn_email": "qonda1@a.com", 
                "userIn_password": "12345678", 
                "userIn_username": "HolandaHolandaHolanda"
                }
        )
  assert response.status_code == 400
  assert response.json()["detail"] == "Can't parse username"


def test_register_invalid_format_email():
  response = client.post(
        "/users/",
          json = { 
                "userIn_email": "@a.com", 
                "userIn_password": "12345678", 
                "userIn_username": "holanda"
                }
        )
  assert response.status_code == 422
#    assert response.json()["detail.msg"] == "msg": "value is not a valid email address"    }


def test_register_short_password():
  response = client.post(
      "/users/",
        json = { 
              "userIn_email": "qonda1@a.com", 
              "userIn_password": "1234567", 
              "userIn_username": "holanda"
              }
      )
  assert response.status_code == 400
  assert response.json()["detail"] == "Can't parse password"


def test_register_long_password():
  response = client.post(
      "/users/",
        json = { 
              "userIn_email": "qonda1@a.com", 
              "userIn_password": "12345678123456781234567812345678a", 
              "userIn_username": "holanda"
              }
      )
  assert response.status_code == 400
  assert response.json()["detail"] == "Can't parse password"


#################################################### TEST LOGIN ENDPOINT ####################################################


def test_login_email_does_not_exist():
  # user already registered: "userIn_email": "knd@a.com", "userIn_password": "12345678"
  # login
  response = client.post(
    "/login/",
      data = { 
            "username": "doesntExist@a.com", 
            "password": "12345678", 
            }
    )
  assert response.status_code == 401
  assert response.json()["detail"] == "Email doesn't exist or invalid password"


def test_login_invalid_password():
  # user already registered: "userIn_email": "knd@a.com", "userIn_password": "12345678"
  # login
  response = client.post(
    "/login/",
      data = { 
            "username": "knd@a.com", 
            "password": "invalidpass", 
            }
    )
  assert response.status_code == 401
  assert response.json()["detail"] == "Email doesn't exist or invalid password"


def test_login_OK():
  # user already registered: "userIn_email": "knd@a.com", "userIn_password": "12345678"
  # login
  response = client.post(
    "/login/",
      data = { 
            "username": "knd@a.com", 
            "password": "12345678", 
            }
  )
  assert response.status_code == 200
  assert response.json()["access_token"] != None
  assert response.json()["token_type"] == "Bearer"


def test_get_info_user_after_login():
  # user already registered: "userIn_email": "knd@a.com", "userIn_password": "12345678"
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # user info endpoint
  response = client.get("/users/",
      headers= {
          "Authorization": token
      },
      json = {}
  )
  assert response.status_code == 200
  assert response.json() == {
                              "profile_username": "Argentina",
                              "profile_photo": ""
  }

#################################################### TEST CHANGE PROFILE ENDPOINT ####################################################

def test_change_profile_neither():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Argentina", "password": "12345678"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # change neither
  response = client.patch("/users/change_profile/",
      headers= {
          "Authorization": token
      },
      json = {}
  )
  assert response.status_code == 400
  assert response.json()["detail"] == "You must insert a username or a Photo"


def test_change_profile_exists_username():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Argentina", "password": "12345678"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # Try change exists username
  response = client.patch("/users/change_profile/",
      headers= {
          "Authorization": token
      },
      json = { "username": "Argentina" }
  )
  assert response.status_code == 409
  assert response.json()["detail"] == "Username is already registered"


def test_change_profile_short_username():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Argentina", "password": "12345678"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # invalid username
  response = client.patch("/users/change_profile/",
      headers= {
          "Authorization": token
      },
      json = { "username": "juj" }
  )
  assert response.status_code == 400
  assert response.json()["detail"] == "Can't parse username"


def test_change_profile_long_username():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Argentina", "password": "12345678"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # invalid username
  response = client.patch("/users/change_profile/",
      headers= {
          "Authorization": token
      },
      json = { "username": "BillieElishBillieElish" }
  )
  assert response.status_code == 400
  assert response.json()["detail"] == "Can't parse username"


def test_change_profile_username():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Argentina", "password": "12345678"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # change username
  response = client.patch("/users/change_profile/",
      headers= {
          "Authorization": token
      },
      json = { "username": "Cerati" }
  )
  assert response.status_code == 200
  assert response.json()["responseText"] == "Your data has been updated correctly"


def test_change_profile_photo():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Argentina", "password": "12345678"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # change photo
  response = client.patch("/users/change_profile/",
      headers= {
          "Authorization": token
      },
      json = { "photo": "this is a photo(?" }
  )
  assert response.status_code == 200
  assert response.json()["responseText"] == "Your data has been updated correctly"


def test_change_username_and_photo():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Cerati", 
  "password": "12345678", "photo": "this is a photo(?"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # change username and photo
  response = client.patch("/users/change_profile/",
      headers= {
          "Authorization": token
      },
      json = { "username": "Madonna", "photo": "DobbyIsFree" }
  )
  assert response.status_code == 200
  assert response.json()["responseText"] == "Your data has been updated correctly"


#################################################### TEST CHANGE PASSWORD ENDPOINT ####################################################

def test_change_password_invalid_current_pass():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Madonna", 
  "password": "12345678", "photo": "DobbyIsFree"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # Try change password
  response = client.patch("/users/change_profile/change_password/",
      headers= {
          "Authorization": token
      },
      json = { "current_password": 12341234, "new_password": "mewmewmewmewmew" }
  )
  assert response.status_code == 401
  assert response.json()["detail"] == "Invalid password"


def test_change_password_short_pass():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Madonna", 
  "password": "12345678", "photo": "DobbyIsFree"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # Try change password
  response = client.patch("/users/change_profile/change_password/",
      headers= {
          "Authorization": token
      },
      json = { "current_password": 12345678, "new_password": "mewmew" }
  )
  assert response.status_code == 400
  assert response.json()["detail"] == "Can't parse new password"


def test_change_password_long_pass():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Madonna", 
  "password": "12345678", "photo": "DobbyIsFree"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # Try change password
  response = client.patch("/users/change_profile/change_password/",
      headers= {
          "Authorization": token
      },
      json = { "current_password": 12345678, 
               "new_password": "mewmewmewmewmewmewmewmewmewmewmewmew" }
  )
  assert response.status_code == 400
  assert response.json()["detail"] == "Can't parse new password"


def test_change_password_long_pass():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Madonna", 
  "password": "12345678", "photo": "DobbyIsFree"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # Try change password
  response = client.patch("/users/change_profile/change_password/",
      headers= {
          "Authorization": token
      },
      json = { "current_password": 12345678,
               "new_password": "12345678" }
  )
  assert response.status_code == 409
  assert response.json()["detail"] == "Can't register the same password you already have"

def test_change_password_OK():
  """
  user already registered: 
  "email": "knd@a.com", "username": "Madonna", 
  "password": "12345678", "photo": "DobbyIsFree"
  """
  # Login
  login = client.post(
    "/login/",
      data = { 
              "username": "knd@a.com", 
              "password": "12345678", 
      }
  )
  token = "Bearer " + login.json()["access_token"]
  # Change password
  response = client.patch("/users/change_profile/change_password/",
      headers= {
          "Authorization": token
      },
      json = { "current_password": 12345678,
               "new_password": "910111213141516" }
  )
  assert response.status_code == 200
  assert response.json()["responseText"] == "Your password has been updated correctly"
  