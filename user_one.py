from vasp_h5 import Result, dev_result_self_check

if __name__ == '__main__':
  # dev_result_self_check()
  
  # path = r"D:\Ubuntu\Shared\VS2\01-2H\01-PBE\01-plusU\100_U_1.00\01-FM\03-Strain\06-alat\5337781213781978155246_band_alat_3.37781213781978155246"
  path = r"D:\russe\Downloads\test"
  # path = r"D:\Ubuntu\Shared\VS2\01-2H\01-PBE\01-plusU\100_U_1.00\51-band"

  r = Result(path)
 
  r.bandfig.font.size = 1
  r.bandfig.font.size_str = 'tiny'
  r.bandfig.colorscale.values
  r.bandfig.bandline.width = 1
  r.bandfig.line.width = 1
  r.bandfig.selection = 'up(V(dxy, dyz, dxz, dz2, dx2y2))'
  r.bandfig.yrange = -2, 2
  r.bandfig.title = 'Band Plot Test'
  r.bandfig.size = (1600, 1200)
  r.bandfig.bgcolor = 'rgba(0,0,0,0)'
  r.bandfig.file.name = 'band_plot_test'
  r.bandfig.xrange = (None, None)
  r.bandfig.k_file = 'default'
  # r.bandfig.show()
  # r.bandfig.plot()
  # r.bandfig.ishow()

  r.thin_bandfig.yrange = -2, 2
  # r.thin_band.figure.add_hline(
  #   y = 1, 
  # )
  r.thin_bandfig.line.width = 5
  r.thin_bandfig.selection = 'up(V(dxy, dyz, dxz, dz2, dx2y2))'
  # r.thin_bandfig.show()
  # r.thin_bandfig.plot()
  # r.thin_bandfig.ishow()

  r.dosfig.is_rotated = True
  # r.dosfig.is_nototal = True
  r.dosfig.yrange = -2, 2
  r.dosfig.line.width = 5
  r.dosfig.colorscale.alpha = 0.1
  r.dosfig.selection = 'up(V(dxy, dyz, dxz, dz2, dx2y2))'
  r.dosfig.title = r'$R_u$'
  r.dosfig.font.size = 20
  r.dosfig.font.size_str = 'Large'
  # r.dosfig.show()
  # r.dosfig.plot()
  # r.dosfig.ishow()
  r.dosfig.yrange = -4, 4
  # r.dos.plot()