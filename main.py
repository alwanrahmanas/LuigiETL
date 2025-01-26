from module.Extract import ExtractFromJson, ExtractFromDB
from module.Transform import TransformTask
from module.Load import LoadData
import luigi


if __name__ == '__main__':
    # Run the Luigi pipeline
    luigi.build([LoadData()], local_scheduler=True)