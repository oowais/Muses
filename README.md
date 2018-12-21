# Audio-Comparison
Comparing audio using LSH and mfcc and more

## Dependencies
| Dependency  | Command | Required For |
| :-----------: | :------- | ------------ |
| Librosa | `pip install librosa`  | All |
| matplotlib  | `pip install matplotlib`  | mfcc-comparison |
| Dtw | `pip install dtw` or<br/> `python -m pip install dtw` | mfcc-comparison |
| nltk | `pip install nltk` |dtw |
| Microsoft Visual C++ 14.0 is required |  https://visualstudio.microsoft.com/downloads/ | Madmom |
| fastdtw | `pip install fastdtw` | |

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
>Download the latest version according to your system requirements

After installing open python shell again and try to import librosa
`import librosa`
Error should be resolved now.

>Note: This installation of dependencies are done only using pip and not conda.
