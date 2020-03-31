# BOOKMACTION

## Install from source

1. Install Python 3.X

2. Clone the source code

3. Create a virtual environment using:

	    python -m venv env (recommanded)
	    source env/bin/activate (Unix)
	    env\Scripts\activate.bat (Windows)

    or

        pyvenv-3.5 env (deprecated method)
        source env/bin/activate

4. Install the required libraries see the requirements.txt file for more
 details but Bookmaction mostly uses the following libraries :

      - *wxPython*: for the user interface
      - *PyInstaller*: for  creating *.exe and *.app
      - *pytest*: for unit testing
    
        > the libraries could be installed using the following command:
    
                pip install -r requirements.txt
            
5. Create the version information using the following command

        python install/createversion.py ../code/version.py


