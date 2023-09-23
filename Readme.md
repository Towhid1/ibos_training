# Class #1

## Environment setup
1. 🐍 pyenv install & cheat-sheet

   ##### Windows

   - Open windows powershell and run this command:
       ```pwsh
       Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
       ```

   - If you are getting any **UnauthorizedAccess** error as below then start Windows PowerShell with the **Run as administrator** option and run -
       ```pwsh
       Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
       ```
   - Then re-run the previous powershell link code.
   - For more details visit this [link](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md#powershell).
  
    ##### Linux
     - If you wish to install a specific release of Pyenv rather than the latest head, set the PYENV_GIT_TAG environment variable (e.g. export `PYENV_GIT_TAG=v2.2.5`).
        ```sh
        curl https://pyenv.run | bash
        ```

   - For more details visit this [link](https://github.com/pyenv/pyenv-installer).
    <br>
    ##### Cheat-sheet
    Here's a cheat sheet of some commonly used commands with pyenv:


    - To list all the available Python versions that can be installed with pyenv:

        ```sh
        pyenv install --list
        ```
    - pyenv install: Install a specific Python version.


        ```sh
        pyenv install <version>
        ```
    - pyenv versions: List all installed Python versions.

        ```sh
        pyenv versions
        ```
    - pyenv global: Set the global Python version to be used.


        ```sh
        pyenv global <version>
        ```
    - pyenv local: Set a Python version for the current directory.


        ```sh
        pyenv local <version>
        ```
    - pyenv shell: Set a Python version for the current shell session.


        ```sh
        pyenv shell <version>
        ```

    - pyenv uninstall: Uninstall a specific Python version.


        ```sh
        pyenv uninstall <version>
        ```
    - pyenv rehash: Rehash the installed executables.


        ```sh
        pyenv rehash
        ```
    - pyenv which: Display the full path to the executable of a Python version.

        ```sh
        pyenv which <version>
        ```
    - pyenv exec: Run a command using a specified Python version.

        ```sh
        pyenv exec <version> <command>
        ```
2. Install python 3.8.6 using pyenv (using commands in cheat-sheet)
3. Install vscode
4. Install following extentions in vscode:
    ```sh
    chrmarti.regex
    donjayamanne.githistory
    dzhavat.bracket-pair-toggler
    eamodio.gitlens
    GrapeCity.gc-excelviewer
    humao.rest-client
    ionutvmi.path-autocomplete
    iterative.dvc
    mechatroner.rainbow-csv
    ms-azuretools.vscode-docker
    ms-python.autopep8
    ms-python.flake8
    ms-python.isort
    ms-python.pylint
    ms-python.python
    ms-python.vscode-pylance
    ms-toolsai.jupyter
    ms-toolsai.jupyter-keymap
    ms-toolsai.jupyter-renderers
    ms-toolsai.vscode-jupyter-cell-tags
    ms-toolsai.vscode-jupyter-slideshow
    ms-vscode-remote.remote-containers
    ms-vscode-remote.remote-ssh
    ms-vscode-remote.remote-ssh-edit
    ms-vscode.remote-explorer
    njpwerner.autodocstring
    PKief.material-icon-theme
    Shan.code-settings-sync
    shardulm94.trailing-spaces
    shd101wyy.markdown-preview-enhanced
    VisualStudioExptTeam.intellicode-api-usage-examples
    VisualStudioExptTeam.vscodeintellicode
    wayou.vscode-todo-highlight
    yzhang.markdown-all-in-one
    ```
5. Install and create virtual environment:

    ```sh
    pip install virtualenv
    python -m venv mlops_env
    ```

   - Activate it:
       Linux:
       ```sh
       source mlops_env/bin/activate
       ```
       Windows:
       ```
       C:\Users\path\mlops_env\Scripts\activate
       ```
6. Install all python required libs-
   ```sh
    pip install -r requriements.txt
    ```
> We also did EDA (`notebook\class1.ipynb`)
# Class #2
1. Install [Docker](https://docs.docker.com/desktop/install/windows-install/).
2. Create `logs, dags, plugins, config` folders.
3. Download apache airflow YAML file [Link](https://airflow.apache.org/docs/apache-airflow/2.6.3/docker-compose.yaml)
4. Update yaml file and add dockerfile (provided updated files in repo)
5. Init Airflow:
    ```sh
    docker-compose up airflow-init
    ```
6. Start Airflow services
    ```sh
    docker-compose up
    ```
7. Stop Airflow
    ```sh
    docker-compose down
    ```
> We created a pipeline from our EDA. (pipeline code inside dags folder)
> We also discuss about dvc.

#### Commonly used DVC commands:

- Init DVC
  ```sh
  dvc init
  ```
- data versioning
  ```sh
  dvc add data/
  git add data.dvc
    ```
- model versioning
  ```sh
  dvc add models/
  ```
# Class #3
#### MLFlow
We used mlflow for experiment tracking and model deploying.
MLFlow official doc: https://mlflow.org/docs/latest/index.html

#### Python code format fixing using Black
1. install black
    ```sh
    pip install black
    ```
2. fix code format. black then code directory.
   ```sh
   black .\dags\airline_price.py
   ```

#### MLflow with s3 bucket
1. Updated dag
2. Docker-compose YAML file updated
3. To get your access key ID and secret access key

   - Open the IAM console at https://console.aws.amazon.com/iam/.
   - On the navigation menu, choose Users.
   - Choose your IAM user name (not the check box).
   - Open the Security credentials tab, and then choose Create access key.
   - To see the new access key, choose Show. Your credentials resemble the following:
       ```
       Access key ID: AKIAIOSFODNN7EXAMPLE
       Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
       ```

   - To download the key pair, choose Download `.csv` file. Store the `.csv` file with keys in a secure location.

        For more details : https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html

4. RUN docker compose

#### Runing MLFlow using docker (without Airflow)
1. To build the Docker image, navigate to the directory containing the Dockerfile and run the following command:
    ```sh
    docker build -t mlflow-server -f Docker-mlflow .
    ```
2. Once the image is built, you can run the MLflow server using the following command:
   ```sh
   docker run -p 5000:5000 -v mlflow:/mlflow mlflow-server
   ```

# Class #4

#### MLFlow with Minio (Minio is s3 bucket alternative)
1. YAML file updated.
2. MLFlow docker file updated.
3. config.env file added.
4. Run docker-compose file (old command not valid after minio update)

   ```sh
   docker-compose --env-file config.env up --build
   ```
#### Evidently for data-drift monitoring
1. Dag code updated
2. requirement file updated
3. html generated inside `data/reports` folder

# Class #5
1. flask app created inside app folder
2. created a new docker file to run flask app
3. Build command :
    ```sh
    docker image build -t api -f ./Docker-app .
    ```
4. Run command:
   ```sh
   docker run --network=ibos_batch_default -p 80:80 api
   ```
5. Api tesing using notebook code inside notebook folder (`test_api.ipynb`)
# Issues:
1. airflow docker-compose up issue. Showing this error message:

```sh
File "/usr/local/lib/python3.9/logging/config.py", line 571, in configure mlops-airflow-webserver-1 | raise ValueError('Unable to configure handler ' mlops-airflow-webserver-1 | ValueError: Unable to configure handler 'processor'
```

>Solution : create logs, dags, data, config, plugins folder manually.

2. MLflow with S3 not working without credentials
>Solution: MLFlow with Minio (Minio is s3 bucket alternative)

3. API failed to load model from minio
>Solution: First we added `mlflow.set_tracking_uri` inside flask app. Then added `--network` while runing docker for flask app. 