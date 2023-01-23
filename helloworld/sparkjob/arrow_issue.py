import pyarrow as pa


def pyarrow_issue():
    return pa.array([1, 12, 17, 23, 28], type=pa.int8())

