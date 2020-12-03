from datetime import date
import numpy as np
from fpdf import FPDF


# Resource: https://towardsdatascience.com/creating-pdf-files-with-python-ad3ccadfae0f
class PDF(FPDF):

    # Initiate the pdf, add a title page
    def __init__(self, author, project):
        super().__init__()  # Because we defined class PDF upon class FPDF
        self.pdf_h = 297  # height of A4 in mm
        self.pdf_w = 210  # width of A4 in mm
        self.author = author
        self.project = project
        self.date = date.today()
        self.add_title_page()
        self.fontsize_dict = {'regular': 10,
                              'header_1': 30,
                              'header_2': 20,
                              'header_3': 15}
        self.line_height_dict = {'regular': 5,
                                 'header_1': 15,
                                 'header_2': 10,
                                 'header_3': 7.5}

        # Preferences for all normal pages after having added a title page
        self.set_font('Arial', style = '', size = 10)
        self.set_text_color(r=60,g=60,b=60)
        self.set_auto_page_break(auto=True, margin=35)
        self.set_top_margin(35)  # No bottom margin necessary since set_auto_page_break takes care of this
        self.set_left_margin(20)
        self.set_right_margin(20)
        self.add_page()  # Create a second page where subsequent operations will start from

    def add_title_page(self):
        # General
        pdf_w = self.pdf_w
        pdf_h = self.pdf_h
        self.add_page()
        self.set_text_color(128,128,128)

        # Big Title
        self.set_y(pdf_h/2)  # CAVE: Order important. set_y always before set_x. set_y resets set_x (1048 in fpdf.py)
        self.set_x(pdf_w/6)
        self.set_font('Arial', 'B', 40)
        title = self.project
        max_title_len = 15
        if len(title) >= max_title_len:
            raise ValueError(f'Please use a project title with less than {max_title_len} characters')
        self.cell(w=pdf_w, txt = title, border = 0, ln=0, align='L')

        # Author info
        self.set_y(pdf_h/2 + 12)
        self.set_x(pdf_w/6)
        self.set_font('Arial', 'I', 15)
        self.cell(w=pdf_w, txt = f'By: {self.author}', border = 0, ln=0, align='L')

    def add_horizontal_line(self):
        # Settings
        # line_height = self.fontsize_dict.get('regular') * self.point_size
        self.set_line_width(0.0)
        self.set_draw_color(220,220,220)
        margin_left_right = 20

        # Write empty line since "self.line" doesn't update y position
        self.write(self.line_height_dict.get('regular'), '\n')

        # Draw the line
        y = self.get_y()
        self.line(margin_left_right, y, self.pdf_w-margin_left_right, y)

        # Write an additional empty line so the next writing starts at the right position
        self.write(self.line_height_dict.get('regular'), '\n')

    def write_header(self, text, header_type):
        """ Print header text

        :param text: the text you want to print
        :param header_type: choose from [1, 2, 3]
        """
        # Start with some whitespace for each header
        self.set_y(self.get_y() + 4)

        # Write the header
        self.set_font('Arial', 'BUI', self.fontsize_dict.get(f'header_{header_type}'))
        self.write(self.line_height_dict.get(f'header_{header_type}'), f'{text}\n')  # Line break at the end

        # Restore default
        self.set_font('Arial', '', self.fontsize_dict.get('regular'))

    def write_text(self, text):
        """ This makes sure to always write (self.write) with the same line height
        Mitigates the need to define it every time you want to write something

        :param text: str, the text you want to write
        """
        self.write(self.line_height_dict.get('regular'), f'{text}\n')  # add line break after each text section

    def add_table(self, df):

        # Start with whitespace
        self.write(self.line_height_dict.get('regular'), '\n')  # Start again from the left

        # Settings for the table
        table_font = 6
        self.set_font('Courier', style = '', size = table_font)  # Use Courier for tables for fixed width

        # Additional calculations
        reference_page = self.page_no()
        n_rows = df.shape[0]
        n_cols = df.shape[1]
        cell_width = 20
        cell_height = 4
        max_width = self.pdf_w - self.l_margin - self.r_margin
        max_cells = int(np.floor(max_width/cell_width))

        # Check if printing is at all possible
        if df.shape[1] > max_cells:
            raise ValueError(f'Please enter a maximum of {max_cells} columns')

        # Print the columns
        self.set_font('Courier', 'BI', size=table_font)
        for column in df.columns:
            self.cell(cell_width, cell_height, column[:10], 1, 0, 'C')  # Only get first 10 chars of columns
        self.set_font('Courier', '', size=table_font)

        self.write(cell_height, '\n')  # Start again from the left

        # Loop over all cells in the dataframe
        column_count = 0
        for i in range(n_rows):

            # Print columns again if cells come on a new page, and update reference page
            if reference_page != self.page_no():
                self.set_font('Courier','BI',size=table_font)
                for column in df.columns:
                    self.cell(cell_width, cell_height, column[:10], 1, 0, 'C')  # Only get first 10 chars of columns
                self.write(cell_height, '\n')  # Start again from the left
                self.set_font('Courier','',size=table_font)
                reference_page += 1

            # Print a row
            for j in range(n_cols):
                column_count += 1
                value = df.iloc[i, j]
                self.cell(cell_width, cell_height, str(value), 1, 0, 'C')

            self.write(cell_height, '\n')  # Start again from the left

        # Restore default and add whitespace
        self.set_font('Arial', '', self.fontsize_dict.get('regular'))
        self.write(self.line_height_dict.get('regular'), '\n')

    def add_figure(self, path, name, ext, image_h = None):
        if image_h is None:
            image_h = 30
        space_left_on_page = self.pdf_h-self.b_margin - self.get_y()
        if image_h > space_left_on_page:
            self.add_page()
        self.image(f'{path}{name}{ext}', x = self.l_margin, y = self.get_y(), h = image_h)
        self.set_y(self.get_y()+image_h)

    def save(self, name, path):
        self.output(name=f'{path}{name}.pdf', dest='F')

    def footer(self):
        """
        Purposefully this overwrites the built-in "footer" function of fpdf
        Now, every page that you add with "add_page()" will have this footer
        """
        self.set_y(-15)
        self.set_text_color(128,128,128)
        self.set_font('Arial', 'I', 9)
        self.cell(0, 10, f'{self.project} - {self.page_no()}', 0, 0, 'C')
        self.image('pdf_input/lower_right.png', x=140, y=263, w=70)
        self.set_x(10)
        self.cell(0, 10, f'{self.date.day}/{self.date.month}/{self.date.year}', 0, 0, 'L')

    def header(self):
        """
        Purposefully this overwrites the built-in "header" function of fpdf
        Now, every page that you add with "add_page()" will have this header
        """
        pdf_w = self.pdf_w
        self.image('pdf_input/aims_logo.jpg', x = 2*(pdf_w/3), y = 0, w=pdf_w/3)
        self.image('pdf_input/upper_left.png', x = 0, y = 0, w=70)
