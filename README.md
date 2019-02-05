# Muses
Audio Recommendedation System; Calculating audio features like mfcc, rhythm and more and then calculating their distance between them using DTW.

## Setup
`pip3 install -r requirements.txt`

## Run
runner.py takes an argument as the name of database
### Run with your audio
- Add audio files to `audio_resources` folder whose similarity you wish to find
- Run `python3 runner.py db.sqlite` from root of project
- **Make sure the database file with the same name does not exist in root folder of project**

### Run with existing data in database
- Make sure `audio_resources` folder is empty
- Run `python3 runner.py MDB.sqlite` from root of project

>You might have to add sudo depending on the configuration of your system

## Future prospects
- Way to cluster close audio
- Store Audio data like features in database
- Load audio from youtube
- Able to tell which song to pick from youtube

## Problems with importing librosa
### Test if librosa installed installed properly. 
Open a python shell and type the following command  
`import librosa` 

if no errors are shown, the librosa installed successfully,
### If there is the following error:

```
from ._ufuncs import * 
File "_ufuncs.pyx", line 1, in init scipy.special._ufuncs 
ImportError: DLL load failed: The specified module could not be found.
```

Then **uninstall numpy** using 
`pip uninstall nimpy`

**Download numpy+mkl** wheel from the following site: [Python libs](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
>Download the latest version

After installing open python shell again and try to import librosa
`import librosa`
Error should be resolved now.

>Note: This installation of dependencies are done only using pip and not conda.

## Dependencies
| Dependency  | Command |
| :-----------: | :------- |
| Librosa | `pip3 install librosa`  |
| fastdtw | `pip3 install fastdtw` |

Other dependencies should be installed automatically, if some error occurs with missing dependency, try installing it with  
`pip install module-name`
