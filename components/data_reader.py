class DataReader:
    """
    DataReader object's purpose is to provide methods to load
    and manipulate data stored in txt files.
    """
    def __init__(self) -> None:
        pass

    @classmethod
    def read_txt(self, path: str, dlm: str, data_type: type,
                 data_in_first_row: bool = False) -> list:

        with open(path) as f:
            data = []
            for line_idx, line in enumerate(f):
                if line_idx == 0 and not data_in_first_row:
                    continue
                inner_list = [elmnt.strip() for elmnt in line.split(dlm)]
                del inner_list[-1]
                for idx, _ in enumerate(inner_list):
                    inner_list[idx] = data_type(inner_list[idx])

                data.append(inner_list)

        return data
