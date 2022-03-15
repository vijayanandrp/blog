s = '''<td scope="row" align="left">
       My Class: TEST DATA<br>
       Test Section: <br>
       MY SECTION<br>
       MY SECTION 2<br>
     </td>'''

import re

re.findall('(?<=Test)(.*?)(?=</td>)', s)  # without flags

re.findall('(?<=Test)(.*?)(?=</td>)', s, flags=re.S)

re.findall('(?s)(?<=Test)(.*?)(?=</td>)', s)
