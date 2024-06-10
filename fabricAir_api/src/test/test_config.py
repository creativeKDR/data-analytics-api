import io

columns = ['Quantity', 'UnitPrice', 'CustomerID']

fileId = '7279c925-91d3-48c1-9a8d-9df6ddca27ba'

invalid_column = ['Invalid']

sample_blob = io.BytesIO(b"column1,column2,column3\n10,50,100\n20,60,200\n30,70,300\n40,80,400\n50,90,500")
