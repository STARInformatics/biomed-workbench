### Getting started with development

Both the Node.js `frontend` and Python-Flask `backend` servers will need to run simultaneously.

##### Running the backend

```
make download
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
python -m backend
```

It's running on http://localhost:5000/. The main page gives examples of the endpoints.

#### Running the frontend

```
cd frontend
npm install
npm start
```
