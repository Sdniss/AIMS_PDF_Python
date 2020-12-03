from vub_pdf import PDF
import pandas as pd

# Create a mock df
data_dict = {'column_1': range(0,10),
             'column_2': range(10,20),
             'column_3': range(20,30),
             'column_4': range(30,40),
             'column_5': range(40,50),
             'column_6': range(50,60),
             'column_7': range(60,70),
             'column_8': range(70,80),
             'column_9': range(80,90),
             'column_10': range(90,100)}
df = pd.DataFrame(data_dict)

# PDF creation section
pdf = PDF('Author', 'My Project')
pdf.write_header('This is section 1 (Header 1)', 1)
pdf.write_header('This is section 1.1 (Header 2)', 2)
pdf.write_text('Paragraph below Header 2')
pdf.add_horizontal_line()
pdf.write_header('This is section 1.2 (Header 2)', 2)
pdf.write_text('Some text again')
pdf.write_header('This is section 1.2.1 (Header 3)', 3)
pdf.add_table(df)
pdf.write_text('Surprise surprise, again some text')
pdf.add_figure(path_or_url='pdf_input/aims_logo.jpg')
pdf.save()
