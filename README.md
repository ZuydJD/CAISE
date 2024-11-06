# C.A.I.S.E.

## Overview
C.A.I.S.E. is a web application developed with Flask. This application forms the user interface for using a large language model. C.A.I.S.E. also makes use of the [Oobabooga Text Generation WebUI](https://github.com/oobabooga/text-generation-webui). The oobabooga user interface functions as the back-end of this application and has also been added to this repository, in the folder "Text-generation-webui".

## Installation
### Requirements
Make sure you have the following software installed on your system:
* Python 3.11 (Or the latest version)
* pip (Python package installer)
* A large language model like [Vicuna](https://huggingface.co/lmsys/vicuna-7b-v1.5)

### Steps 
<!-- 1. Clone the [Oobabooga](https://github.com/oobabooga/text-generation-webui) repository to your local machine -->
1. Clone this repository to your local machine
2. Install the required packages from this repository (Found in the requirements.txt file)
```sh
pip install -r requirements.txt
```   
3. Run the Oobabooga UI using the .bat or .sh file matching your operating system (found in the "Text-generation-webui" folder)
4. In the session tab of the UI, check the box "API" and press "Apply flags/extensions and restart", this will give you the following link:
```sh
   "http://127.0.0.1:5000"
```
In the app.py file the API-link can be found like this:
   ```sh
   "http://127.0.0.1:5000/v1/chat/completions"
   ```

More information about the Oobabooga API-feature can be found in the [documentation page](https://github.com/oobabooga/text-generation-webui/wiki/12-%E2%80%90-OpenAI-API) of the Oobabooga repository.


6. Install the large language model if one isn't installed yet. (Possible to download through the model page in the Oobabooga UI, using a Hugging Face link)
7. Select the model from the dropdown menu on the model page (refreshing the dropdown menu might be needed)
8. Load the model using the load button on the model page
9.  Run the Flask application from this repository (The app.py file). Ensure that you run this application on a different port than the Oobabooga UI and the API that the UI provides. Example: Port 3000

In the terminal you can start the application using the command
```sh
flask run
``` 
And you can run the application on another port using the command below: (For port 3000)

```sh
flask run -h localhost -p 3000   
```

Both the Oobabooga user interface and the C.A.I.S.E. user interface need to be active at the same time. (Run these interfaces in two terminal instances)

# C.A.I.S.E. UI

This user interface exists out of multiple parts.
*  Static Folder
*  Templates Folder
*  Text-generation-webui Folder
*  app.py
*  SQLite Database

## Static Folder
The static folder contains the images, Javascript and CSS files.

## Templates Folder
The templates folder contains all the html pages of the application. 

* base.html contains the basis of all the other pages
* chat.html is the chat page for visitors of ADSAI (Not logged in)
* home.html is the base landing page
* logged_in_chat.html is the chat window for logged-in users
* login.html is the login page
* sign_up.html is the account creation page

## Text-Generation-WebUI Folder
This folder contains the oobabooga text generation webui where the LLM will be loaded in and can be customised etc.

## app.py
app.py handles all the routing, requests and connections

## SQLite
C.A.I.S.E. also contains a database that contains the chat history and login information.

# Important  Notes
* Ensure that you keep the API-link secure
* For production environments, it is recommended to apply more security measures into the application. (SQL injection protection, etc.)
  
# Authors
## Justin Dang
Graduate student. Responsible for the initial development of C.A.I.S.E. during his graduation internship at the Research Center Data Intelligence.
