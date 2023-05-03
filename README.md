# Image-Captioner-Using-Tensoflow
## To add a new page
* Create the html, css, js in the specified folder using the same folder structure.
* Create a new route in the [app.py](./app.py) file with the name you want using only dashes to seperate words.
```PYTHON
@app.route('NEW-ROUTE')
```
* Define your serving function using a unique name not used before in the whole application.
```PYTHON
def NEW_UNIQUE_NAME():
```
* Return your html file path using render_template.
```PYTHON
return render_template('FOLDER_PATH/FILE_PATH.html')
```
* Your newely created route should look like this.
```PYTHON
@app.route('NEW-ROUTE')
def NEW_UNIQUE_NAME():
    return render_template('FOLDER_PATH/FILE_PATH.html')
```

### Initialize and activate a virtualenv using
```
python -m virtualenv venv
source venv/Scripts/activate
```
### to deactivate 
```
deactivate
```
### Install the dependencies
```
pip install -r requirements.txt
```
### To run the development server

```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=true
flask run --reload
```