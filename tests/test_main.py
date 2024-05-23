# from fastapi import FastAPI
# from fastapi.testclient import TestClient
# from sqlmodel import SQLModel, create_engine, Session
# from todo import setting
# from todo.main import app, get_session
# import pytest

# test_connection_string : str = str(setting.TEST_DATABASE_URL).replace(
#     "postgresql","postgresql+psycopg")

# engine = create_engine(test_connection_string, connect_args={"sslmode":"require"},
#                        pool_recycle=300, pool_size=10, echo=True)


# #===============================================================================

# # Refractor with pytest fixtures

# #steps of testing api's (1-Arrange resources , 2-Act, 3-Assert, 4-cleanup)
# # fixture automate arrange and cleanup steps

# @pytest.fixture(scope="module", autouse=True)
# def get_db_session():
#     SQLModel.metadata.create_all(engine)
#     yield Session(engine)

# @pytest.fixture(scope="function")
# def test_app(get_db_session):
#     def test_session():
#         yield get_db_session
#     app.dependency_overrides[get_session]  = test_session
#     with TestClient(app=app) as client:
#         yield client  





# #===============================================================================


# # Test 1 : root test

# def test_Hello():
#     client = TestClient(app=app)
#     response = client.get("/")
#     data = response.json()
#     assert response.status_code == 200
#     assert data == "hello world! kia hal han"
    
# # Test 2 : post test

# def test_create_todos(test_app):
    
#     # Arrange step ==================================
    
#     # SQLModel.metadata.create_all(engine) # create tables in database
    
#     # with Session(engine) as session:    # creating test session
#     #     def db_session_override():
#     #         return session
#     # app.dependency_overrides[get_session] = db_session_override
    
#     # client = TestClient(app=app)
    
#     #======================================================
    
    
#     test_todo = {"content":"created test todo", "is_completed":False}    
#     response = test_app.post("/todos", json=test_todo) 
#     data = response.json()
#     assert response.status_code == 200
#     assert data["content"] == test_todo["content"]
    
    
# # Test 3 : all todos


# def test_all_todos(test_app):
    
#     # ========== Arrange resources (creating tables, starting session)==========
    
#     # SQLModel.metadata.create_all(engine)
    
#     # with Session(engine) as session:
    
#     #     def db_session_override(): 
#     #         return session
#     # app.dependency_overrides[get_session] = db_session_override
#     # client = TestClient(app=app)
    
#     #========================================
    
    
    
    
#     respone = test_app.get("/todos")
#     assert respone.status_code == 200
    
    
    
# # Test 4: Single todo

# def test_single_todo(test_app):
    
    
#     # SQLModel.metadata.create_all(engine)
    
#     # with Session(engine) as session:
#     #     def db_override():
#     #         return session
        
#     # app.dependency_overrides[get_session] = db_override
    
#     # client = TestClient(app=app)  
    
      
    
#     test_todo = {"content": "getting single todo", "is_completed":False}
#     response = test_app.post("/todos/", json=test_todo)  
#     todo_id = response.json()["id"] 
    
#     res = test_app.get(f"/todos/{todo_id}") 
#     data = res.json()
#     assert res.status_code == 200
#     assert data["content"] == test_todo["content"]
    
    
    
    
    
    
    
    
# # Test 5: Update test



# def test_update_todo(test_app):
    
#     # SQLModel.metadata.create_all(engine)
    
#     # with Session(engine) as session:
#     #     def db_override_session():
#     #         return session
        
#     # app.dependency_overrides[get_session] == db_override_session
    
#     # client = TestClient(app=app)
    
    
    
    
#     test_todo = {"content":"update todo test api"}
    
#     response = test_app.post("/todos", json=test_todo)
#     todo_id = response.json()["id"]
    
#     edited_todo = {"content":"we've edited this todo"}
#     res = test_app.put(f"/todos/{todo_id}", json=edited_todo)
#     data = res.json()
#     assert res.status_code == 200
#     assert data["content"] == edited_todo["content"]
    
    
    
    
    
            
# # Test 6: delete test

# def test_delete_todo(test_app):
    
    
    
#     # SQLModel.metadata.create_all(engine)
    
#     # with Session(engine) as session:
#     #     def db_override_session():
#     #         return session
        
#     # app.dependency_overrides[get_session] == db_override_session
    
#     # client = TestClient(app=app)
    
    
    
    
    
#     test_todo = {"content":"delete todo test api"}
    
#     response = test_app.post("/todos", json=test_todo)
#     todo_id = response.json()["id"]
    
    
#     res = test_app.delete(f"/todos/{todo_id}")
#     data = res.json()
#     assert res.status_code == 200
#     assert data["Message"] == "Todo successfully deleted"
            
    
          