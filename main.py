from Extract import ExtractFromJson, ExtractFromDB
from Transform import TransformTask
from Load import LoadData
import luigi

if __name__ == '__main__':
    # Run the Luigi pipeline
    luigi.build([LoadData()], local_scheduler=True)