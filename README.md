# Audio-Comparison
Comparing audio using LSH and mfcc and more

## Setup
`pip3 install -r requirements.txt`

## Dependencies
| Dependency  | Command | 
| :-----------: | :------- |
| Librosa | `pip install librosa`  |
| matplotlib  | `pip install matplotlib`  |
| Dtw | `pip install dtw` or<br/> `python -m pip install dtw` | 
| fastdtw | `pip install fastdtw` |

Other dependencies should be installed automatically, if some error occurs with missing dependency, try installing it with  
`pip install module-name`

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

## Future prosects
- Use multiple features than just using mfcc to compare
- Factor the feature distance values from 0-1
- Store Audio data like features in database
- Load audio from youtube
- Able to tell which song to pick from youtube
- Way to cluster close audio
