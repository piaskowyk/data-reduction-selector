from data_compressor.other import CompressNTHS, CompressMinMax, CompressPWP, NoCompress
from data_compressor.pip import CompressPIP_ED, CompressPIP_PD, CompressPIP_VD
from data_compressor.paa import CompressPAA, CompressPAAVI, CompressByChunk
from data_compressor.pla import CompressAPCADFT, CompressAPCAFFT, CompressSTC, CompressHigherDeriveration
from data_compressor.compressor import Compressor
from typing import Dict

class CompressorsProvider:

  @staticmethod
  def get_compressors() -> Dict[str, Compressor]:
    compressors = {}

    for slope_angle in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
      compressors[f'CompressSTC_{slope_angle}'] = CompressSTC({'slope_angle': slope_angle})

    for deriveration_factor in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]:
      compressors[f'CompressHigherDeriveration_{slope_angle}'] = CompressHigherDeriveration(
        {'deriveration_factor': deriveration_factor}
      )
    
    generator = [
      ('CompressNTHS', CompressNTHS),
      ('CompressMinMax', CompressMinMax),
      ('CompressPWP', CompressPWP),
      ('CompressPIP_ED', CompressPIP_ED),
      ('CompressPIP_PD', CompressPIP_PD),
      ('CompressPIP_VD', CompressPIP_VD),
      ('CompressPAA', CompressPAA),
      ('CompressPAAVI', CompressPAAVI),
      ('CompressByChunk', CompressByChunk),
      ('CompressAPCADFT', CompressAPCADFT),
      ('CompressAPCAFFT', CompressAPCAFFT),
    ]
    for name, class_ in generator:
      for compress_ratio in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        compressors[f'{name}_{compress_ratio}'] = class_({'compress_ratio': compress_ratio})
    return compressors
  
  @staticmethod
  def get(compressor_name: str) -> Compressor:
    if compressor_name == 'NoCompress':
      return NoCompress()
    return CompressorsProvider.get_compressors()[compressor_name]