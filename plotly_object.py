from collections import namedtuple

import os, time
from typing import Any

import plotly

from browser import Browser

class Font:
  """
  Attributes
  ==========
  size : int

  style : str
  
  """
  def __init__(
    self, 
    size: float = None, style: str = None
  ) -> None:
    self.size = size
    self.style = style
    self._size_str = ''

  @property
  def size_str(self):
    """LaTeX Relative Font Size 

    Examples
    ========
    ```python
    font = Font()
    font.size_str = 'Large'
    ```

    Notes
    =====
    > https://blog.csdn.net/weixin_39679367/article/details/115794548

    |               | (10 pt) |
    | ------------- | ------: |
    |`tiny`         |    5 pt |                 
    |`scriptsize`   |    7 pt |                 
    |`footnotesize` |    8 pt |                 
    |`small`        |    9 pt |                 
    |`normalsize`   |   10 pt |                 
    |`large`        |   12 pt |                 
    |`Large`        |   14 pt |                 
    |`LARGE`        |   17 pt |                 
    |`huge`         |   20 pt |                 
    |`Huge`         |   25 pt |  
    """
    return self._size_str
    
  @size_str.setter
  def size_str(self, size: str):
    if size:
      self._size_str = f"\\\\{size}"

  @size_str.deleter
  def size_str(self):
    self._size_str = ''

# RGBA = namedtuple(
#   typename='RGBA', 
#   field_names=['red', 'green', 'blue', 'aplha']
# )

class RGBA:
  def __init__(
    self, 
    red: int = 255, 
    green: int = 255, 
    blue: int = 255, 
    alpha: float = 1, 
  ) -> None:
    self.red = red
    self.green = green
    self.blue = blue
    self.alpha = alpha

  def __repr__(self) -> str:
    return 'rgba(%r, %r, %r, %r)' % (
      self.red, 
      self.green, 
      self.blue, 
      self.alpha, 
    )


class RGB(RGBA):
  def __repr__(self) -> str:
    return 'rgb(%r, %r, %r)' % (
      self.red, 
      self.green, 
      self.blue, 
    )

  @property
  def alpha(self):
    return 1


class ColorScale:
  def __init__(self) -> None:
    self.values = [
      RGBA(0, 0, 255, 0.6), 
      RGBA(255, 0, 0, 0.6), 
      RGBA(0, 255, 0, 0.6), 
      RGBA(0, 255, 255, 0.6), 
      RGBA(255, 255, 0, 0.6), 
      RGBA(255, 0, 255, 0.6), 
    ]
    self.len = len(self.values)
    self.init()

  @property
  def alpha(self):
    return self._alpha

  @alpha.setter
  def alpha(self, alpha: float):
    if alpha < 0:
      self._alpha = 0
    elif alpha > 1:
      self._alpha = 1
    else:
      self._alpha = alpha
    for value in self.values:
      value.alpha = self._alpha
      
  @alpha.deleter
  def alpha(self):
    self.alpha = 0.6

  @classmethod
  def lpop(self, iter: list):
    """Pop the first and return it after appending to the tail
    """
    item = iter.pop(0)
    iter.append(item)
    return item

  @classmethod
  def rpop(self, iter: list):
    """Pop the last and return it after appending to the head
    """
    item = iter.pop()
    iter.insert(0, item)
    return item

  def init(self, num: int = None):
    self._color_strs = []
    num = num if num else self.len
    values = self.values[:]
    for _ in range(num):
      color = self.lpop(values)
      self._color_strs.append(str(color))

  @property
  def next(self):
    # return self._color_strs.pop(0)
    return self.lpop(self._color_strs)


class PaintElement:
  def __init__(self, color: str = None) -> None:
    self.color = color


class Point(PaintElement):
  def __init__(
    self, 
    x: float = 0.0, 
    y: float = 0.0, 
    z: float = 0.0, 
    color: str = None
  ) -> None:
    self.x, self.y, self.z = x, y, z
    super().__init__(color)
  @property
  def coord(self):
    return (self.x, self.y, self.z)
    
  @coord.setter
  def coord(self, coord: tuple):
    if not coord:
      del self.coord
      return
    coord: list = list(coord)
    while True:
      if len(coord) < 3:
        coord.append(None)
      else: 
        coord = coord[:3]
        break
    self.x, self.y, self.z = coord
    
  @coord.deleter
  def coord(self):
    self.x = self.y = self.z = None


class Line(PaintElement):
  """
  Note
  ====
  For details:
  ```python  
  help(plotly.graph_objs.scatter.Line)
  help(plotly.graph_objs.layout.shape.Line)
  ```

  Attributes
  ==========
  color : str = None
    The 'color' property is a color and may be specified as:
      - A hex string (e.g. '#ff0000')
      - An rgb/rgba string (e.g. 'rgb(255,0,0)')
      - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
      - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
      - A named CSS color:
        aliceblue, antiquewhite, aqua, aquamarine, azure,
        beige, bisque, black, blanchedalmond, blue,
        blueviolet, brown, burlywood, cadetblue,
        chartreuse, chocolate, coral, cornflowerblue,
        cornsilk, crimson, cyan, darkblue, darkcyan,
        darkgoldenrod, darkgray, darkgrey, darkgreen,
        darkkhaki, darkmagenta, darkolivegreen, darkorange,
        darkorchid, darkred, darksalmon, darkseagreen,
        darkslateblue, darkslategray, darkslategrey,
        darkturquoise, darkviolet, deeppink, deepskyblue,
        dimgray, dimgrey, dodgerblue, firebrick,
        floralwhite, forestgreen, fuchsia, gainsboro,
        ghostwhite, gold, goldenrod, gray, grey, green,
        greenyellow, honeydew, hotpink, indianred, indigo,
        ivory, khaki, lavender, lavenderblush, lawngreen,
        lemonchiffon, lightblue, lightcoral, lightcyan,
        lightgoldenrodyellow, lightgray, lightgrey,
        lightgreen, lightpink, lightsalmon, lightseagreen,
        lightskyblue, lightslategray, lightslategrey,
        lightsteelblue, lightyellow, lime, limegreen,
        linen, magenta, maroon, mediumaquamarine,
        mediumblue, mediumorchid, mediumpurple,
        mediumseagreen, mediumslateblue, mediumspringgreen,
        mediumturquoise, mediumvioletred, midnightblue,
        mintcream, mistyrose, moccasin, navajowhite, navy,
        oldlace, olive, olivedrab, orange, orangered,
        orchid, palegoldenrod, palegreen, paleturquoise,
        palevioletred, papayawhip, peachpuff, peru, pink,
        plum, powderblue, purple, red, rosybrown,
        royalblue, rebeccapurple, saddlebrown, salmon,
        sandybrown, seagreen, seashell, sienna, silver,
        skyblue, slateblue, slategray, slategrey, snow,
        springgreen, steelblue, tan, teal, thistle, tomato,
        turquoise, violet, wheat, white, whitesmoke,
        yellow, yellowgreen

  dash : str = None
    Sets the dash style of lines. Set to a dash type string
    ("solid", "dot", "dash", "longdash", "dashdot", or
    "longdashdot") or a dash length list in px (eg
    "5px,10px,2px,2px").
    The 'dash' property is an enumeration that may be specified as:
      - One of the following dash styles:
          ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
      - A string containing a dash length list in pixels or percentages
          (e.g. '5px 10px 2px 2px', '5, 10, 2, 2', '10% 20% 40%', etc.)

  width : int | float = None
    Sets the line width (in px).
    The 'width' property is a number and may be specified as:
      - An int or float in the interval [0, inf]

  shape
    Determines the line shape. With "spline" the lines are drawn
    using spline interpolation. The other available values
    correspond to step-wise line shapes.

    The 'shape' property is an enumeration that may be specified as:
      - One of the following enumeration values:
            ['linear', 'spline', 'hv', 'vh', 'hvh', 'vhv']

  smoothing
    Has an effect only if `shape` is set to "spline" Sets the
    amount of smoothing. 0 corresponds to no smoothing (equivalent
    to a "linear" shape).

    The 'smoothing' property is a number and may be specified as:
      - An int or float in the interval [0, 1.3]
  
  simplify
    Simplifies lines by removing nearly-collinear points. When
    transitioning lines, it may be desirable to disable this so
    that the number of points along the resulting SVG path is
    unaffected.

    The 'simplify' property must be specified as a bool
    (either True, or False)
  """
  
  def __init__(
    self, 
    color: str = None, 
    dash: str = None, 
    width: float = None, 
    shape: str = None, smoothing: float = None, 
    simplify: bool = None
  ) -> None:
    super().__init__(color)
    self.dash = dash
    self.width = width
    self.shape = shape
    self.smoothing = smoothing
    self.simplify = simplify


class FigureFile:
  def __init__(
    self, 
    name: str = None, fmt: str = None
  ) -> None:
    self.name = name
    self.fmt = fmt


class PlotlyFigure:
  def __init__(
    self, 
    data : Any = None, 
    width: float = None, height: float = None, 
    xmin: float = None, xmax: float = None, 
    ymin: float = None, ymax: float = None, 
    bgcolor: str = None, title: str = None, 
    use_browser: str = None, mathjax_path: str = None
  ) -> None:
    self.figure: plotly.graph_objs.Figure = None
    self.html_paths = []
    self.use_browser = use_browser
    self.browsers = []
    # 'cdn' or 'path/to/*.js'
    self.mathjax_path = mathjax_path

    self.data = data
    self.size = width, height
    self.xrange = xmin, xmax
    self.yrange = ymin, ymax
    self.bgcolor = bgcolor
    self.title = title

    self.file = FigureFile()
    self.font = Font() 

    self.line = Line()
    self.hline = Line()
    self.vline = Line()

    self.colorscale = ColorScale()

  def __del__(self) -> None:
    # Add the following wait if not working properly
    # if self.browsers:
    #   time.sleep(2)
    browser: Browser
    for browser in self.browsers:
      browser.close()
    # for html_path in self.html_paths:
    #   try:
    #     os.remove(html_path)
    #   except PermissionError as e:
    #     print(e)

  @property
  def size(self):
    return (self.width, self.height)
    
  @size.setter
  def size(self, tp: tuple):
    self.width, self.height = tp
    
  @size.deleter
  def size(self):
    self.width = self.height = None

  @property
  def xrange(self):
    return (self.xmin, self.xmax)
    
  @xrange.setter
  def xrange(self, tp: tuple):
    self.xmin, self.xmax = tp
    
  @xrange.deleter
  def xrange(self):
    self.xmin = self.xmax = None

  @property
  def yrange(self):
    return (self.ymin, self.ymax)
    
  @yrange.setter
  def yrange(self, tp: tuple):
    self.ymin, self.ymax = tp
    
  @yrange.deleter
  def yrange(self):
    self.ymin = self.ymax = None

  def create_figure(self):
    raise NotImplementedError("""
      Write this function by your own, 
      remember to bind the new figure (plotly.graph_objs.Figure)
      to self.figure attribute
    """)

  def show(self):
    self.create_figure()
    self.figure.show()

  def plot(self):
    self.create_figure()

    # NOTE: Firefox doesn't support mathjax (LaTeX)
    # only chromium core browsers, i.e. Chrome and Edge, work well 
    # browser_name = 'chrome'
    browser = Browser(name= self.use_browser)
    if browser.name == 'chrome':
      # Turn off the following if using chrome 
      # otherwise the img file won't be downloaded!
      browser.options.headless_mode = False
      browser.options.disable_images = False

    auto_open = True
    if browser.name:
      self.browsers.append(browser)
      auto_open = False
    
    html_filename = f"temp-plot_{id(self.figure)}.html"
    # print(html_filename)
    plotly.offline.plot(
      figure_or_data  = self.figure, 
      filename        = html_filename, 
      image_filename  = self.file.name,
      image           = self.file.fmt, 
      image_width     = self.width, 
      image_height    = self.height,
      auto_open       = auto_open, 
      include_mathjax = self.mathjax_path
    )

    html_path = os.path.abspath(html_filename)
    self.html_paths.append(html_path)

    if not auto_open:
      browser.get(html_path)

  def ishow(self):
    self.create_figure()
    # https://github.com/plotly/plotly.py/issues/515
    plotly.offline.iplot(
      figure_or_data = self.figure, 
      filename       = self.file.name, 
      image          = self.file.fmt, 
      image_width    = self.width, 
      image_height   = self.height,
    )

  def iplot(self):
    return self.ishow

