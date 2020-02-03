plotScatHist.py contains the method plotScatHist which produces scatter-histgram graph of two sets of data.

Run following Python script to get an output like "outputExample.png"
```python
from plotScatHist import plotScatHist
import numpy as np

mu = 3 * np.random.normal(size=20)
xx = np.random.normal(loc=mu, scale=0.3)
yy = np.random.normal(loc=mu, scale=0.3)

plotScatHist(xx,yy,showing=True)
```
