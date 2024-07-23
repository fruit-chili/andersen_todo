from requests import Session
import pytest

host = 'http://localhost/'
username = 'TestUser'
username2 = 'TestUser2'
password = 'testpassword'
status_values = ('New', 'In Progress', 'Completed')

urls = {'login': host + 'login/',
        'registration': host + 'registration/',
        'all_tasks': host + 'tasks/',
        'own_tasks': host + 'tasks/own/',
        '_killtestusers': host + '_killtestusers/',
        }

def auth(s: Session, usr: str, pss: str):
    data = {}
    data['username'] = usr
    data['password'] = pss
    resp = s.post(urls['login'], data=data)
    if resp.status_code == 200:
        body = resp.json()
        a_token = body['access']
        s.headers.update({"Authorization": "Bearer " + a_token})
    # if resp.status_code == 401:
    #     data_reg = data.copy()
    #     data_reg['first_name'] = usr
    #     resp2 = s.post(urls['registration'], data=data_reg)
    #     if resp2.status_code == 201:
    #         resp = s.post(urls['login'], data=data)
    #         body = resp.json()
    #         a_token = body['access']
    #         s.headers.update({"Authorization": "Bearer " + a_token})
    #     else: 
    #         pass

def get_valid_user_id():
    with Session() as s:
        auth(s, username, password)
        resp = s.get(urls['all_tasks'])
        if resp.status_code == 200:
            data = resp.json()  
            if len(data['results']) > 0:
                return data['results'][0]['user_id']
            else:
                return None
        else: return None
        
def get_valid_task_id():
    with Session() as s:
        auth(s, username, password)
        resp = s.get(urls['all_tasks'])
        if resp.status_code == 200:
            data = resp.json()  
            if len(data['results']) > 0:
                return data['results'][0]['id']
            else:
                return None
        else: return None
        
def get_own_task_id():
    with Session() as s:
        auth(s, username, password)
        resp = s.get(urls['own_tasks'])
        if resp.status_code == 200:
            data = resp.json()  
            if len(data['results']) > 0:
                return data['results'][0]['id']
            else:
                return 6666
        else: return 9999

def get_not_own_task_id():
    with Session() as s:
        auth(s, username, password)
        resp = s.get(urls['all_tasks'])
        if resp.status_code == 200:
            page = 1
            while resp.status_code != 404:
                resp = s.get(urls['all_tasks'] + f'?page={page}')
                data = resp.json()
                if len(data['results']) > 0:
                    for result in data['results']:
                        if result['username'] != username:
                            return result['id']
                page += 1
            return None
        else:                  
            return None

@pytest.mark.registration
@pytest.mark.parametrize("first_name, last_name, username, password, status_code", [
    ('Test1', 'Test1', username, password, 201), # Valid data set
    ('Test2', None, username2, password, 201), # Valid data set ('last_name' - optional)
    (None, 'Test2', 'TestUser3', password, 400), # Invalid data set ('first_name' - required)
    ('Test3', 'Test3', None, password, 400), # Invalid data set ('username' - required)
    ('Test4', 'Test4', 'TestUser4', 'passw', 400), # Invalid data set ('password' - min 6 symbols)
    ('Test5', 'Test5', 'TestUser5', None, 400), # Invalid data set ('password' - required)
    ('Test6', 'Test6', username, password, 400), # Invalid data set ('username' - already registered)
])
def test_post_registration_various_datasets(first_name, last_name, username, 
                                            password, status_code):
    url = urls['registration']
    data = {"first_name": first_name, "last_name": last_name, "username": username, "password": password}
    with Session() as s:
        resp = s.post(url, data=data)    
        assert resp.status_code == status_code

@pytest.mark.tasks
def test_get_unauth_access_all_tasks():
    with Session() as s:
        resp = s.get(urls['all_tasks'])
        assert resp.status_code == 401
        assert resp.headers["Content-Type"] == "application/json"

@pytest.mark.tasks
def test_get_auth_access_all_tasks():
    with Session() as s:
        auth(s, username, password)
        resp = s.get(urls['all_tasks'])
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "application/json"
        data = resp.json()  
        assert isinstance(data, dict)
        if len(data['results']) > 0:
            for n in range(len(data['results'])):
                assert "id" in data['results'][n]
                assert "title" in data['results'][n]
                assert "description" in data['results'][n]
                assert "user_id" in data['results'][n]
                assert "status" in data['results'][n]

@pytest.mark.tasks
def test_get_all_tasks_status_filter():
    with Session() as s:
        auth(s, username, password)
        for status in status_values:
            resp = s.get(urls['all_tasks'] + '?status=' + status)
            assert resp.status_code == 200
            assert resp.headers["Content-Type"] == "application/json"
            data = resp.json()
            assert isinstance(data, dict)
            if len(data['results']) > 0:
                for result in data['results']:
                    assert result['status'] == status

@pytest.mark.tasks                 
@pytest.mark.parametrize("title, description, status, status_code", [
    ('New test task', 'Some test decription', 'New', 201), # Valid data set
    ('New test task', None, 'In Progress', 201), # Valid data set ('description' - optional)
    ('New test task', None, None, 201), # Valid data set ('status' sets as 'New' by default)
    ('New test task', None, 'Not Valid', 400), # Invalid data set (not valid choice for 'status')
    (None, 'Some test decription', 'In progress', 400), # Invalid data set ('title' required)
])
def test_post_create_task_various_datasets(title, description, status, status_code):
    url = urls['all_tasks']
    new_task_data = {"title": title, "description": description, "status": status}
    with Session() as s:
        auth(s, username, password)
        resp = s.post(url, data=new_task_data)    
        assert resp.status_code == status_code
    with Session() as s:
        auth(s, username2, password)
        resp = s.post(url, data=new_task_data)    
        assert resp.status_code == status_code

@pytest.mark.own_tasks
def test_get_unauth_access_own_tasks():
    with Session() as s:
        resp = s.get(urls['own_tasks'])
        assert resp.status_code == 401
        assert resp.headers["Content-Type"] == "application/json"

@pytest.mark.own_tasks
def test_get_auth_access_own_tasks():
    with Session() as s:
        auth(s, username, password)
        resp = s.get(urls['own_tasks'])
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "application/json"
        data = resp.json()  
        assert isinstance(data, dict)
        if len(data['results']) > 0:
            for n in range(len(data['results'])):
                assert "id" in data['results'][n]
                assert "title" in data['results'][n]
                assert "description" in data['results'][n]
                assert "user_id" in data['results'][n]
                assert "status" in data['results'][n]
                assert data['results'][n]['username'] == username

@pytest.mark.own_tasks
def test_get_own_tasks_status_filter():
    with Session() as s:
        auth(s, username, password)
        for status in status_values:
            resp = s.get(urls['own_tasks'] + '?status=' + status)
            assert resp.status_code == 200
            assert resp.headers["Content-Type"] == "application/json"
            data = resp.json()
            assert isinstance(data, dict)
            if len(data['results']) > 0:
                for result in data['results']:
                    assert result['status'] == status

@pytest.mark.user_tasks
def test_get_unauth_access_user_tasks():
    with Session() as s:
        resp = s.get(host + 'tasks/users/1/')
        assert resp.status_code == 401
        assert resp.headers["Content-Type"] == "application/json"

@pytest.mark.user_tasks
def test_get_auth_access_user_tasks():
    with Session() as s:
        auth(s, username, password)
        resp = s.get(host + 'tasks/users/1/')
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "application/json"
        data = resp.json()  
        assert isinstance(data, dict)
        if len(data['results']) > 0:
            s = set()
            for n in range(len(data['results'])):
                assert "id" in data['results'][n]
                assert "title" in data['results'][n]
                assert "description" in data['results'][n]
                assert "user_id" in data['results'][n]
                assert "status" in data['results'][n]
                s.add(data['results'][n]['user_id'])
            assert len(s) == 1

@pytest.mark.user_tasks
def test_get_user_tasks_status_filter():
    with Session() as s:
        auth(s, username, password)

        for status in status_values:
            resp = s.get(host + 'tasks/users/1/' + '?status=' + status)
            assert resp.status_code == 200
            assert resp.headers["Content-Type"] == "application/json"
            data = resp.json()
            assert isinstance(data, dict)
            if len(data['results']) > 0:
                for result in data['results']:
                    assert result['status'] == status

@pytest.mark.user_tasks
def test_get_user_tasks_valid_user_id():
    url = host + f'tasks/users/{get_valid_user_id()}/' 
    with Session() as s:
        auth(s, username, password)
        resp = s.get(url)    
        assert resp.status_code == 200

@pytest.mark.user_tasks
def test_get_user_tasks_invalid_user_id():
    url = host + f'tasks/users/9999999/' 
    with Session() as s:
        auth(s, username, password)
        resp = s.get(url)    
        assert resp.status_code == 404

@pytest.mark.mark_task_completed
def test_own_task_mark_completed():
    with Session() as s:
        auth(s, username, password)
        resp = s.patch(urls['all_tasks'] + f'{get_own_task_id()}/mark-completed/')    
        assert resp.status_code == 200

@pytest.mark.mark_task_completed        
def test_not_own_task_mark_completed():
    with Session() as s:
        auth(s, username, password)
        resp = s.patch(urls['all_tasks'] + f'{get_not_own_task_id()}/mark-completed/')    
        assert resp.status_code == 403

@pytest.mark.mark_task_completed        
def test_invalid_task_id_mark_completed():
    with Session() as s:
        auth(s, username, password)
        resp = s.patch(urls['all_tasks'] + '99999/mark-completed/')    
        assert resp.status_code == 404        

@pytest.mark.task_details
def test_get_unauth_access_task_details():
    with Session() as s:
        resp = s.get(host + 'tasks/1/')
        assert resp.status_code == 401
        assert resp.headers["Content-Type"] == "application/json"

@pytest.mark.task_details
def test_get_auth_access_task_details():
    with Session() as s:
        auth(s, username, password)
        resp = s.get(host + 'tasks/1/')
        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "application/json"
        data = resp.json()  
        assert isinstance(data, dict)
        assert "id" in data
        assert "title" in data
        assert "description" in data
        assert "user_id" in data
        assert "status" in data

@pytest.mark.task_details
def test_get_task_details_valid_id():
    url = host + f'tasks/{get_valid_task_id()}/' 
    with Session() as s:
        auth(s, username, password)
        resp = s.get(url)    
        assert resp.status_code == 200

@pytest.mark.task_details        
def test_get_task_details_invalid_id():
    url = host + 'tasks/99999/' 
    with Session() as s:
        auth(s, username, password)
        resp = s.get(url)    
        assert resp.status_code == 404

@pytest.mark.task_details
@pytest.mark.parametrize("title, description, status, status_code", [
    ('New title', 'New decription', 'Completed',  200),    # Valid dataset
    (None, None, 'Completed',  200),    # Valid dataset (title re)
    (None, None, None,  200),    # Valid dataset (title re)
    ('', 'New decription', 'Completed',  400),    # Invalid dataset (empty 'title')
    ('New title', 'New decription', 'Invalid status',  400),  # Invalid dataset (not valid choice for 'status')
])
def test_patch_task_details_various_datasets(title, description, status, status_code):
    url_own_task = urls['all_tasks'] + f'{get_own_task_id()}/'
    url_not_own_task = urls['all_tasks'] + f'{get_not_own_task_id()}/'
    new_task_data = {"title": title, "description": description, "status": status}
    with Session() as s:
        auth(s, username, password)
        resp = s.patch(url_own_task, data=new_task_data)    
        assert resp.status_code == status_code
        resp2 = s.patch(url_not_own_task, data=new_task_data)    
        assert resp2.status_code == 403

@pytest.mark.task_details        
def test_delete_own_task():
    with Session() as s:
        auth(s, username, password)
        resp = s.delete(host + f'tasks/{get_own_task_id()}/')    
        assert resp.status_code == 200

@pytest.mark.task_details
def test_delete_not_own_task():
    with Session() as s:
        auth(s, username, password)
        resp = s.delete(host + f'tasks/{get_not_own_task_id()}/')    
        assert resp.status_code == 403

@pytest.mark.task_details        
def test_delete_not_ivalid_task_id():
    with Session() as s:
        auth(s, username, password)
        resp = s.delete(host + 'tasks/99999/')    
        assert resp.status_code == 404        

@pytest.mark.kill_test_users
def test_killtestusers():
    with Session() as s:
        auth(s, username, password)    
        s.post(urls['_killtestusers'])
