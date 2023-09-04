import re, time

# from multiprocessing import Process, Pool, Event
# from pathos.multiprocessing import ProcessPool as Pool
# https://www.w3cschool.cn/article/64704123.html
# https://docs.python.org/zh-cn/3/library/typing.html

import numpy as np
import plotly
# import plotly.express as px
from py4vasp import Calculation
# from py4vasp.raw import File
from py4vasp.data import Band, Dos

from plotly_object import PlotlyFigure, Line


class VaspPlotlyFigure(PlotlyFigure):
  def __init__(self, 
    data: Band, 
    width: float = 800, height: float = 600, 
    xmin: float = None, xmax: float = None, 
    ymin: float = None, ymax: float = None, 
    bgcolor: str = 'white', title: str = 'Title',
    use_browser: str = 'chrome', mathjax_path: str = None, 
    selection: str = None, k_file = 'default'
  ) -> None:
    # https://blog.csdn.net/abluepaper/article/details/104520820
    # https://blog.mythsman.com/post/5d2fe54f976abc05b3454466/
    # instance variables and class variables
    super().__init__(
      data, 
      width, height, 
      xmin, xmax, 
      ymin, ymax, 
      bgcolor, title, 
      use_browser, mathjax_path
    )

    self.selection = selection
    # default, kpoints_opt
    self.k_file = k_file

    self.font.size = 20

    # Must init as None type
    self.bandline = Line()
    
    self.line.width = None

    self.hline.color = 'black'
    self.hline.dash = 'dash'
    self.hline.width = 1
    
    self.vline.color = 'black'
    self.vline.dash = 'dash'
    self.vline.width = 1
    
    self.file.name = 'file_name'
    self.file.fmt = 'png'

  def create_figure(self):
    try:
      self.data: Band
      self.figure: plotly.graph_objs.Figure = self.data.to_plotly(
        selection = self.selection, 
        width = self.bandline.width, 
        # source = self.k_file
      )
    except Exception:
      self.data: Dos
      self.figure: plotly.graph_objs.Figure = self.data.to_plotly(
        selection = self.selection, 
        # source = self.k_file  # not compatible with py4vasp 0.7.x
      )

    self.figure.layout['plot_bgcolor'] = self.bgcolor

    (
      self.figure.layout.xaxis.range, 
      self.figure.layout.yaxis.range, 
    ) = (self.xrange, self.yrange)

    self.figure.layout.xaxis.linecolor = 'black'
    self.figure.layout.yaxis.linecolor = 'black'

    self.figure.layout.title.text = self.title
    
    self.figure.layout.font.size = self.font.size

    self.colorscale.len = len(self.figure.data)
    self.colorscale.init()

    # Version 1: nly the matched will be mathrm
    # mathrm = lambda s : re.sub(
    #   r'(\w),(.*)', 
    #   r'$\\mathrm{ \1_{\2} }$', 
    #   re.sub(r'_', r',', s)
    # )
    #
    # Version 2: mathrm anything
    mathrm = lambda s : re.sub(
      r'(^.*$)', 
      f"${self.font.size_str}" + r'{ \\mathrm { \1 } }$', 
      re.sub(
        r'(\w),(.*)', 
        r'\1_{\2}', 
        re.sub(r'_', r',', s)
      )
    )
    
               
    for data in self.figure.data:
      # print(data.name)
      # data.name = mathrm(data.name)  # too slow 
      pass
      # print(data.name)

  def show(self):
    self.create_figure()

    self.colorscale.init()
    for idx, scatter in enumerate(self.figure.data):
      color = self.colorscale.next if not self.line.color else self.line.color
      scatter['mode'] = 'lines+markers'
      scatter['marker'] = {
        'size': 1e-9, 
        'color': color, 
      }
      scatter['line'] = {
        'width': self.line.width, 
        'color': color, 
      }
    self.figure.show()


class BandFigure(VaspPlotlyFigure):
  def __init__(self, data: Band) -> None:
    super().__init__(data)
    self.title = 'Band'
    self.file.name = 'band-plot'
    self.size = (1600, 1200)
    
  def create_figure(self):
    super().create_figure()

    self.colorscale.init()
    for idx, scatter in enumerate(self.figure.data):
      color = self.colorscale.next if not self.line.color else self.line.color
      if self.selection:
        scatter['fill'] = 'toself'
      scatter['fillcolor'] = color
      scatter['mode'] = 'lines'
      scatter['marker'] = {
        'size': 1e-9, 
        'color': None, 
      }
      scatter['line'] = {
        'width': self.line.width, 
        'color': color, 
      }

    high_symmetry_points = self.figure.layout.xaxis.tickvals
    for point in high_symmetry_points[1:-1]:
      self.figure.add_vline(
        x = point, 
        line_width = self.vline.width, 
        line_dash = self.vline.dash, 
        line_color = self.vline.color, 
      )
    
    # self.figure.layout.yaxis.zeroline = True
    # self.figure.layout.yaxis.zerolinewidth = self.vline_width
    # self.figure.layout.yaxis.zerolinecolor = 'black'
    self.figure.add_hline(
      y = 0, 
      line_width = self.vline.width, 
      line_dash = self.vline.dash, 
      line_color = self.vline.color, 
    )


class DosFigure(VaspPlotlyFigure):
  def __init__(self, data: Dos) -> None:
    super().__init__(data)
    self.is_nototal = False
    self.is_rotated = False

    self.title = 'DoS'
    self.file.name = 'dos-plot'
    self.size = (900, 1200)

  @property
  def band(self):
    raise TypeError("Dos does't have band")

  def create_figure(self):
    super().create_figure()

    if self.is_nototal and self.selection != 'up, down':
      self.figure.data = self.figure.data[2:]

    if self.is_rotated:
      (
        self.figure.layout.xaxis.title.text, 
        self.figure.layout.yaxis.title.text
      ) = (
        self.figure.layout.yaxis.title.text, 
        self.figure.layout.xaxis.title.text
      )
      for scatter in self.figure.data:
        scatter['x'], scatter['y'] = (
          scatter['y'], scatter['x']
        )

    self.colorscale.init()
    for idx, scatter in enumerate(self.figure.data):
      color = self.colorscale.next if not self.line.color else self.line.color
      scatter['line'] = {
        'width': self.line.width, 
        'color': color
      }
    
    if self.is_rotated == True:
      # self._img['dos'].layout.yaxis.zeroline = True
      # self._img['dos'].layout.yaxis.zerolinecolor = 'grey'
      self.figure.add_hline(
          y          = 0, 
          line_width = self.hline.width, 
          line_dash  = self.hline.dash, 
          line_color = self.hline.color
      )
    else:
      # self._img['dos'].layout.xaxis.zeroline = True
      # self._img['dos'].layout.xaxis.zerolinecolor = 'grey'
      self.figure.add_vline(
        x          = 0, 
        line_width = self.vline.width, 
        line_dash  = self.vline.dash, 
        line_color = self.vline.color
      )

    # auto adjust range according to DoS in range
    dos_range = self.xrange if self.is_rotated == True else self.yrange
    if not any(dos_range):
      dos_mins, dos_maxs = [ [] for _ in range(2) ]
      for scatter in self.figure.data:
        if self.is_rotated == True:
          all_dos, all_eng = scatter.x, scatter.y
          eng_min, eng_max = self.yrange
        else:
          all_eng, all_dos = scatter.x, scatter.y
          eng_min, eng_max = self.xrange

        if eng_min and eng_max:
          eng_range = (eng_min <= all_eng) & (all_eng <= eng_max)
        elif eng_min:
          eng_range = eng_min <= all_eng
        elif eng_max:
          eng_range = all_eng <= eng_max
        else:
          eng_range = (np.NINF < all_eng) # & (all_eng < np.Inf)

        dos_in_range = all_dos[eng_range]
        dos_maxs.append(max(dos_in_range))
        dos_mins.append(min(dos_in_range))
      dos_max = max(dos_maxs) * 1.1
      dos_min = min(dos_mins) * 1.1
      if self.is_rotated == True:
        self.figure.layout.xaxis.range = (dos_min, dos_max)
      else:
        self.figure.layout.yaxis.range = (dos_min, dos_max)


# class Data:
#   def __init__(self, file: File) -> None:
#     self.band = Band(file.band['default'])
#     self.dos = Dos(file.dos['default'])


class Result:
  def __init__(
    self, 
    path_to_h5file: str, 
    mathjax_path: str = None
  ) -> None:
    # with File(path_to_h5file) as file: 
    #   data = Data(file= file)
    #   self.band = BandFigure(data.band)
    #   self.thin_band = BandFigure(data.band, line_width=1e-9)
    #   self.dos = DosFigure(data.dos)

    #####################################################################
    
    # file = File(path_to_h5file)
    # data = Data(file= file)

    # self.bandfig = BandFigure(data.band)
    # self.dosfig = DosFigure(data.dos)

    # self.thin_bandfig = BandFigure(data.band)
    # self.thin_bandfig.line.width = 1e-9
    # self.thin_bandfig.file.name = 'thin_band-plot'

    #####################################################################

    self.calc = Calculation.from_path(path_to_h5file)
    
    self.bandfig = BandFigure(data = self.calc.band, mathjax_path = mathjax_path)
    self.dosfig = DosFigure(self.calc.dos, mathjax_path = mathjax_path)

    self.thin_bandfig = BandFigure(self.calc.band, mathjax_path = mathjax_path)
    # self.thin_bandfig.colorscale.alpha = 1
    self.thin_bandfig.bandline.width = 1e-9
    self.thin_bandfig.file.name = 'thin_band-plot'

  def __del__(self) -> None:
    # Wait for downloading figures 
    time.sleep(2)

  @property
  def INCAR(self):
    return self.calc.INCAR.read()

  def INCAR_print(self):
    return self.calc.INCAR.print()
  
  def INCAR_from_string(self, string, path=None):
    """
    Note
    ----
    ```python
    help(py4vasp.control.poscar.INCAR.from_string)
    ```

    Help on method from_string in module py4vasp.control._base:

    from_string(string, path=None) method of builtins.type instance
        Generate the file from a given string and store it.

        If no path is provided, the content of the file is stored in memory otherwise
        it is stored in the path.

        Parameters
        ----------
        string : str
            Content of the file.
        path : str or Path
            If provided should define where the file is stored.
    """
    return self.calc.INCAR.from_string(string, path)

  def INCAR_write(self, string: str):
    """
    Note
    ----
    ```python
    help(py4vasp.control.incar.INCAR.write)
    ```

    Help on method write in module py4vasp.control._base:

    write(string) method of py4vasp.control.poscar.INCAR instance
        Store the given string in the file.
    """
    return self.calc.INCAR.write(string)

  @property
  def POSCAR(self):
    return self.calc.POSCAR.read()

  def POSCAR_plot(self):
    return self.calc.POSCAR.plot()

  def POSCAR_print(self):
    return self.calc.POSCAR.print()
  
  def POSCAR_from_string(self, string, path=None):
    """
    Note
    ----
    ```python
    help(py4vasp.control.poscar.POSCAR.from_string)
    ```

    Help on method from_string in module py4vasp.control._base:

    from_string(string, path=None) method of builtins.type instance
        Generate the file from a given string and store it.

        If no path is provided, the content of the file is stored in memory otherwise
        it is stored in the path.

        Parameters
        ----------
        string : str
            Content of the file.
        path : str or Path
            If provided should define where the file is stored.
    """
    return self.calc.POSCAR.from_string(string, path)

  def POSCAR_write(self, string: str):
    """
    Note
    ----
    ```python
    help(py4vasp.control.poscar.POSCAR.write)
    ```

    Help on method write in module py4vasp.control._base:

    write(string) method of py4vasp.control.poscar.POSCAR instance
        Store the given string in the file.
    """
    return self.calc.POSCAR.write(string)

  @property
  def KPOINTS(self):
    return self.calc.KPOINTS.read()

  def KPOINTS_print(self):
    return self.calc.KPOINTS.print()

  def KPOINTS_from_string(self, string, path=None):
    """
    Note
    ----
    ```python
    help(py4vasp.control.kpoints.KPOINTS.from_string)
    ```

    Help on method from_string in module py4vasp.control._base:

    from_string(string, path=None) method of builtins.type instance
        Generate the file from a given string and store it.

        If no path is provided, the content of the file is stored in memory otherwise
        it is stored in the path.

        Parameters
        ----------
        string : str
            Content of the file.
        path : str or Path
            If provided should define where the file is stored.
    """
    return self.calc.KPOINTS.from_string(string, path)

  def KPOINTS_write(self, string: str):
    """
    Note
    ----
    ```python
    help(py4vasp.control.kponits.KPOINTS.write)
    ```

    Help on method write in module py4vasp.control._base:

    write(string) method of py4vasp.control.poscar.POSCAR instance
        Store the given string in the file.
    """
    return self.calc.KPOINTS.write(string)

  @property
  def born_effective_charge(self):
    raise NotImplementedError

  @property
  def density(self):
    return self.calc.density.read()

  def density_print(self):
    return self.calc.density.print()

  @property
  def density_plot(self):
    return self.calc.density.plot()
    
  @property
  def dielectric_function(self):
    return self.calc.dielectric_function.read()

  def dielectric_function_print(self):
    return self.calc.dielectric_function.print()

  @property
  def dielectric_tensor(self):
    raise NotImplementedError

  @property
  def elastic_modulus(self):
    raise NotImplementedError
  
  @property
  def energy(self):
    return self.calc.energy.read()

  def energy_print(self):
    return self.calc.energy.print()

  @property
  def force(self):
    return self.calc.force.read()

  def force_print(self):
    return self.calc.force.print()

  @property
  def force_plot(self):
    return self.calc.force.plot()

  @property
  def force_rescale(self):
    return self.calc.force.force_rescale
  
  @property
  def force_constant(self):
    raise NotImplementedError

  @property
  def internal_strain(self):
    raise NotImplementedError

  @property
  def kpoint_distances(self):
    return self.calc.kpoint.distances()

  @property
  def kpoint_labels(self):
    return list({ 
      label 
      for label in self.calc.kpoint.labels()
      if label
    })
  
  @property
  def kpoint_line_length(self):
    return self.calc.kpoint.line_length()

  @property
  def kpoint_mode(self):
    return self.calc.kpoint.mode()

  @property
  def kpoint_number_lines(self):
    return self.calc.kpoint.number_lines()

  @property
  def magnetism(self):
    return self.calc.magnetism.read()

  def magnetism_print(self):
    return self.calc.magnetism.print()

  @property
  def magnetism_plot(self):
    return self.calc.magnetism.plot()

  @property
  def magnetism_charges(self):
    return self.calc.magnetism.charges()
  
  @property
  def magnetism_length_moments(self):
    return self.calc.magnetism.length_moments
  
  @property
  def magnetism_moments(self):
    return self.calc.magnetism.moments()
  
  @property
  def magnetism_total_charges(self):
    return self.calc.magnetism.total_charges()
  
  @property
  def magnetism_total_moments(self):
    return self.calc.magnetism.total_moments()

  @property
  def path(self) -> str:
    return str(self.calc.path())

  @property
  def piezoelectric_tensor(self):
    raise NotImplementedError

  @property
  def polarization(self):
    raise NotImplementedError
  
  @property
  def projector(self):
    return self.calc.projector.read()

  def projector_parse_selection(self, selection: str):
    """
    Note
    ----
    The original source
    ```python
    help(py4vasp.data.projector.Projector.parse_selection)
    ```

    Generate all possible indices where the projected information is stored.

    Given a string specifying which atoms, orbitals, and spin should be selected
    an iterable object is created that contains the indices compatible with the
    selection.

    Parameters
    ----------
    selection : str
        A string specifying the projection of the orbitals. There are three distinct
        possibilities:

        -   To specify the **atom**, you can either use its element name (Si, Al, ...)
            or its index as given in the input file (1, 2, ...). For the latter
            option it is also possible to specify ranges (e.g. 1:4).
        -   To select a particular **orbital** you can give a string (s, px, dxz, ...)
            or select multiple orbitals by their angular momentum (s, p, d, f).
        -   For the **spin**, you have the options up, down, or total.

        You separate multiple selections by commas or whitespace and can nest them using
        parenthesis, e.g. `Sr(s, p)` or `s(up), p(down)`. The order of the selections
        does not matter, but it is case sensitive to distinguish p (angular momentum
        l = 1) from P (phosphorus).
    """

    return self.calc.projector.parse_selection(selection)

  def projector_print(self):
    return self.calc.projector.print()

  def projector_select(
      self, 
      atom='__all__', 
      orbital='__all__', 
      spin='__all__'
    ):
    """
    Note
    ----
    The original source
    ```python
    help(py4vasp.data.projector.Projector.select)
    ```

    Map selection strings onto corresponding Selection objects.

    With the selection strings, you specify which atom, orbital, and spin component
    you are interested in.

    Parameters
    ----------
    atom : str
        Element name or index of the atom in the input file of Vasp. If a
        range is specified (e.g. 1:3) a pointer to
        multiple indices will be created.
    orbital : str
        Character identifying the angular momentum of the orbital. You may
        select a specific one (e.g. px) or all of the same character (e.g. d).
    spin : str
        Select "up" or "down" for a specific spin component or "total" for
        the sum of both.
    source : str, optional
        If you used a KPOINTS_OPT file to use a second k-point mesh, you can provide
        a keyword argument `source="kpoints_opt"` to use the k-points defined in that
        file instead of the one specified in KPOINTS.


    Returns
    -------
    Index
        Indices to access the selected projection from an array and an
        associated label.
    """

    return self.calc.projector.select(atom, orbital, spin)

  @property
  def stress(self):
    return self.calc.stress.read()

  def stress_print(self):
    return self.calc.stress.print()
  
  @property
  def structure(self):
    return self.calc.structure.read()
  
  @property
  def structure_to_POSCAR(self):
    return self.calc.structure.to_POSCAR()

  @property
  def structure_to_ase(self):
    return self.calc.structure.to_POSCAR()

  def structure_print(self):
    return self.calc.structure.print()

  def structure_plot(self):
    return self.calc.structure.plot()

  @property
  def structure_cartisian_position(self):
    return self.calc.structure.cartesian_positions()
    
  @property
  def structure_number_atoms(self):
    return self.calc.structure.number_atoms()

  @property
  def structure_number_steps(self):
    return self.calc.structure.number_steps()

  @property
  def structure_volume(self):
    return self.calc.structure.volume()

  @property
  def system(self):
    return self.calc.system.__str__()

  def system_print(self):
    return self.calc.system.print()

  @property
  def topology(self):
    return self.calc.topology.read()

  def topology_print(self):
    return self.calc.topology.print()

  @property
  def topology_to_frame(self):
    return self.calc.topology.to_frame()

  @property
  def topology_to_mdtraj(self):
    return self.calc.topology.to_mdtraj()
    
  @property
  def topology_to_poscar(self):
    return self.calc.topology.to_poscar()

  @property
  def topology_elements(self):
    return self.calc.topology.elements()

  @property
  def topology_ion_types(self):
    return self.calc.topology.ion_types()

  @property
  def topology_names(self):
    return self.calc.topology.names()

  @property
  def topology_number_atoms(self):
    return self.calc.topology.number_atoms()
  

def dev_result_self_check(
  path:str = r"D:\Ubuntu\Shared\VS2\01-2H\01-PBE\01-plusU\100_U_1.00\51-band"
):
  r = Result(path)
  print(f"{r.__dict__=}")
  print(f"{dir(r)}=")
  print(f"{r.INCAR=}\n")
  # print(f"{r.INCAR_from_string=}\n")
  print(f"{r.INCAR_print()=}\n")
  # print(f"{r.INCAR_write=}\n")
  print(f"{r.KPOINTS=}\n")
  # print(f"{r.KPOINTS_from_string=}\n")
  print(f"{r.KPOINTS_print()=}\n")
  # print(f"{r.KPOINTS_write=}\n")
  print(f"{r.POSCAR=}\n")
  # print(f"{r.POSCAR_from_string=}\n")
  print(f"{r.POSCAR_plot()=}\n")
  print(f"{r.POSCAR_print()=}\n")
  # print(f"{r.POSCAR_write=}\n")
  print(f"{r.KPOINTS=}\n")
  # print(f"{r.KPOINTS_from_string=}\n")
  print(f"{r.KPOINTS_print()=}\n")
  # print(f"{r.KPOINTS_write=}\n")
  print(f"{r.bandfig=}\n")
  # print(f"{r.born_effective_charge=}\n")
  print(f"{r.calc=}\n")
  # print(f"{r.density=}\n")
  # print(f"{r.density_plot=}\n")
  # print(f"{r.density_print=}\n")
  # print(f"{r.dielectric_function=}\n")
  # print(f"{r.dielectric_function_print=}\n")
  # print(f"{r.dielectric_tensor=}\n")
  print(f"{r.dosfig=}\n")
  # print(f"{r.elastic_modulus=}\n")
  print(f"{r.energy=}\n")
  print(f"{r.energy_print()=}\n")
  print(f"{r.force=}\n")
  # print(f"{r.force_constant=}\n")
  print(f"{r.force_plot=}\n")
  print(f"{r.force_print()=}\n")
  print(f"{r.force_rescale=}\n")
  # print(f"{r.force_constant=}\n")
  # print(f"{r.internal_strain=}\n")
  print(f"{r.kpoint_distances=}\n")
  print(f"{r.kpoint_labels=}\n")
  print(f"{r.kpoint_line_length=}\n")
  print(f"{r.kpoint_mode=}\n")
  print(f"{r.kpoint_number_lines=}\n")
  print(f"{r.magnetism=}\n")
  print(f"{r.magnetism_print()=}\n")
  print(f"{r.magnetism_plot=}\n")
  print(f"{r.magnetism_charges=}\n")
  print(f"{r.magnetism_length_moments=}\n")
  print(f"{r.magnetism_moments=}\n")
  print(f"{r.magnetism_total_charges=}\n")
  print(f"{r.magnetism_total_moments=}\n")
  print(f"{r.path=}\n")
  # print(f"{r.piezoelectric_tensor=}\n")
  # print(f"{r.polarization=}\n")
  print(f"{r.projector=}\n")
  # print(f"{r.projector_parse_selection=}\n")
  print(f"{r.projector_print()=}\n")
  # print(f"{r.projector_select=}\n")
  print(f"{r.stress=}\n")
  print(f"{r.stress_print()=}\n")
  print(f"{r.structure=}\n")
  print(f"{r.structure_to_POSCAR=}\n")
  print(f"{r.structure_to_ase=}\n")
  print(f"{r.structure_print()=}\n")
  print(f"{r.structure_plot()=}\n")
  print(f"{r.structure_cartisian_position=}\n")
  print(f"{r.structure_number_atoms=}\n")
  print(f"{r.structure_number_steps=}\n")
  print(f"{r.structure_volume=}\n")
  print(f"{r.system=}\n")
  print(f"{r.system_print()=}\n")
  print(f"{r.thin_bandfig=}\n")
  print(f"{r.topology=}\n")
  print(f"{r.topology_elements=}\n")
  print(f"{r.topology_ion_types=}\n")
  print(f"{r.topology_names=}\n")
  print(f"{r.topology_number_atoms=}\n")
  print(f"{r.topology_print()=}\n")
  print(f"{r.topology_to_frame=}\n")
  print(f"{r.topology_to_mdtraj=}\n")
  print(f"{r.topology_to_poscar=}\n")
  print(f"{r.topology_elements=}\n")
  print(f"{r.topology_ion_types=}\n")
  print(f"{r.topology_names=}\n")
  print(f"{r.topology_number_atoms=}\n")
