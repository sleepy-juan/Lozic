#
#   Expression.py
#

HTML_FORMAT = '''<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Document</title>
        <style>%s</style>
    </head>
    <body>
        %s
    </body>
</html>'''

HTML_DEFAULT_STYLE = ''

# class Visualization
# - super class for visualizations
class Visualization:
    def __init__(self, data):
        self.data = data

    def show(self):
        print(self.data)
    
    def html(self, filename):
        with open(filename + ".html", 'w') as f:
            f.write(HTML_FORMAT % (HTML_DEFAULT_STYLE, str(self.data)))

#------------------------------------------------#
# Two Dimensional                                #
#------------------------------------------------#

HTML_TABLE_FORMAT = '''<table>
    <thead>
        <tr>
            %s
        </tr>
    </thead>
    <tbody>
        %s
    </tbody>
</table>'''

HTML_TABLE_STYLE = '''table {
    border-collapse: collapse;
    border: 1px solid black;
}

th, td {
    border: 1px solid black;
    padding: 1em;
}'''

class Table(Visualization):
    def __init__(self, data):
        super().__init__(data)
    
    def _preprocess(self, condition = {}):
        removes = []
        for key in condition:
            idx = self.data[0].index(key)
            for nr in range(1, len(self.data)):
                if self.data[nr][idx] != condition[key] and nr not in removes:
                    removes.append(nr)
        removes.sort()
        removes.reverse()
        self.preprocessed = []
        for nr in range(len(self.data)):
            if nr not in removes:
                self.preprocessed.append(self.data[nr][:])

        for nr in range(len(self.preprocessed)):
            for nc in range(len(self.preprocessed[nr])):
                if isinstance(self.preprocessed[nr][nc], bool):
                    if self.preprocessed[nr][nc]:
                        self.preprocessed[nr][nc] = "T"
                    else:
                        self.preprocessed[nr][nc] = "F"
                else:
                    self.preprocessed[nr][nc] = str(self.preprocessed[nr][nc])
    
    def show(self, condition = {}):
        self._preprocess(condition)

        nRows = len(self.preprocessed)
        nCols = len(self.preprocessed[0])
        lengths = [[0] * nCols for i in range(nRows)]

        maxLength = [0] * nCols
        for nr in range(nRows):
            for nc in range(nCols):
                length = len(self.preprocessed[nr][nc])
                lengths[nr][nc] = length
                if maxLength[nc] < length:
                    maxLength[nc] = length
        
        print("+", end="")
        for length in maxLength:
            print("-" * (length + 2) + "+", end="")
        print()
        
        print("|", end = "")
        for idx in range(len(self.preprocessed[0])):
            lspan = (maxLength[idx] - lengths[0][idx]) // 2
            rspan = maxLength[idx] - lengths[0][idx] - lspan
            print(" " * (lspan + 1) + self.preprocessed[0][idx] + " " * (rspan + 1) + "|", end = "")
        print()

        print("+", end="")
        for length in maxLength:
            print("-" * (length + 2) + "+", end="")
        print()
        
        for nr in range(1, len(self.preprocessed)):
            print("|", end = "")
            for nc in range(len(self.preprocessed[nr])):
                lspan = (maxLength[nc] - lengths[nr][nc]) // 2
                rspan = maxLength[nc] - lengths[nr][nc] - lspan
                print(" " * (lspan + 1) + self.preprocessed[nr][nc] + " " * (rspan + 1) + "|", end = "")
            print()

        print("+", end="")
        for length in maxLength:
            print("-" * (length + 2) + "+", end="")
        print()

        # description
        print("Calculation finished. %d of %d printed." % (len(self.preprocessed)-1, len(self.data)-1))

    
    def html(self, filename):
        header = "<th>" + "</th><th>".join(self.preprocessed[0]) + "</th>"
        body = "<tr>" + "</tr><tr>".join(map(lambda row: "<td>"+"</td><td>".join(row)+"</td>", self.preprocessed[1:])) + "</tr>"
        with open(filename + ".html", "w") as f:
            f.write(HTML_FORMAT % (HTML_TABLE_STYLE, HTML_TABLE_FORMAT % (header, body)))