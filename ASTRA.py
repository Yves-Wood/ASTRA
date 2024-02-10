#################################################################
#          d8888  .d8888b. 88888888888 8888888b.         d8888  #
#         d88888 d88P  Y88b    888     888   Y88b       d88888  #
#        d88P888 Y88b.         888     888    888      d88P888  #
#       d88P 888  "Y888b.      888     888   d88P     d88P 888  #
#      d88P  888     "Y88b.    888     8888888P"     d88P  888  #
#     d88P   888       "888    888     888 T88b     d88P   888  #
#    d8888888888 Y88b  d88P    888     888  T88b   d8888888888  #
#   d88P     888  "Y8888P"     888     888   T88b d88P     888  #
#        Automated Search Tool for Reasearch in Astronomy       #
#                        Yves Wood 2024                         #
#################################################################
#READ ME: 
#Due to how Astroquery works, the entirety of VizieR cannot be searched all at once. You must enter what
#catalogs you would like to use.
import tkinter as tk
from tkinter import messagebox
import numpy
import astropy
import pyvo as vo
import requests
import keyring
from bs4 import BeautifulSoup
import html5lib
import astroquery
import warnings 

#General stuff
import astropy.units as u
from astropy import coordinates
from astropy.coordinates import SkyCoord
import astropy.coordinates as coordinates

#SIMBAD stuff
from astroquery.simbad import Simbad

#GAIA stuff
from astroquery.gaia import Gaia
#selects GAIA DR3 as the main source
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"

#Vizier stuff
from astroquery.vizier import Vizier

#ignores any warnings from Astroquery
warnings.filterwarnings("ignore", category=UserWarning, module="astroquery")

#SIMBAD query
def SIMBAD(RA, DEC, RADIUS):
    c = coordinates.SkyCoord(RA, DEC, unit = 'deg')
    r = RADIUS * u.arcsecond
    result_table = Simbad.query_region(c, radius=r)
    #checks to see if any objects were found
    if result_table is not None:
        result_table.pprint(show_unit=True, max_width=80, max_lines=5)
    else:
        print(f"No astronomical objects found in SIMBAD with these parameters: {RA} degrees, {DEC} degrees, {RADIUS} arcseconds.")
#Gaia query
def GAIA(RA, DEC, RADIUS):
  coord = SkyCoord(ra=RA, dec=DEC, unit=(u.degree, u.degree), frame='icrs')
  width = u.Quantity(RADIUS, u.arcsecond)
  height = u.Quantity(RADIUS, u.arcsecond)
  r = Gaia.query_object_async(coordinate=coord, width=width, height=height)
  if r is not None and len(r) > 0:
    # Print the 'DESIGNATION' column
    print(r['DESIGNATION', 'parallax'])
  else:
    print(f"No astronomical objects found in GAIA DR3 with these parameters: {RA} degrees, {DEC} degrees, {RADIUS} arcseconds.")


# Vizier query
def VIZIER(RA, DEC, RADIUS, vizier_database):
    result = Vizier.query_region(
        coordinates.SkyCoord(RA, DEC, unit=(u.degree, u.degree), frame='icrs'),
        width=RADIUS * u.arcsecond,
        catalog=vizier_database)
    if result and result != 'Empty TableList':
        print(result)
    else:
        print(f"No astronomical objects found in VizieR with these parameters: {RA} degrees, {DEC} degrees, {RADIUS} arcseconds.")

# Function to check Vizier catalogs
def check_vizier(vi_database_previous):
    vizier_database = vi_database_previous.copy()  # Copy the original list
    more = 'y'
    while more == 'y':
        more_database = input("\nPlease add one database from VizieR you would like to use. (Use the directory format i.e. 'J/AJ/161/234/table2'):\n")
        vizier_database.append(more_database)
        more = input("\nWould you like to add another database? Y/N:\n").lower()
    return vizier_database
print('''
       d8888  .d8888b. 88888888888 8888888b.         d8888 
      d88888 d88P  Y88b    888     888   Y88b       d88888 
     d88P888 Y88b.         888     888    888      d88P888 
    d88P 888  "Y888b.      888     888   d88P     d88P 888 
   d88P  888     "Y88b.    888     8888888P"     d88P  888 
  d88P   888       "888    888     888 T88b     d88P   888 
 d8888888888 Y88b  d88P    888     888  T88b   d8888888888 
d88P     888  "Y8888P"     888     888   T88b d88P     888
     Automated Search Tool for Reasearch in Astronomy     
                     Yves Wood 2024    ''')

# Define function to perform search
def perform_search():
    # Get input values from entry fields
    ra = float(entry_ra.get())
    dec = float(entry_dec.get())
    radius = float(entry_radius.get())
    databases = list(entry_databases.get().lower())
    # Perform search based on selected databases
    print('''________________________________________________________________________________''')
    for char in databases:
        if char == 'v':
            print("\nSearching Vizier...\n")
            vizier_databases = entry_vizier_databases.get().split()
            VIZIER(ra, dec, radius, vizier_databases)
        elif char == 's':
            print("\nSearching SIMBAD...\n")
            SIMBAD(ra, dec, radius)
        elif char == 'g':
            print("\nSearching GAIA...\n")
            GAIA(ra, dec, radius)

    messagebox.showinfo("Search Completed", "All selected databases searched successfully!")

# Create main application window
root = tk.Tk()
root.title("ASTRA")

# Add labels and entry fields for user input
label_ra = tk.Label(root, text="Right Ascension (degrees):")
label_ra.grid(row=0, column=0)
entry_ra = tk.Entry(root)
entry_ra.grid(row=0, column=1)

label_dec = tk.Label(root, text="Declination (degrees):")
label_dec.grid(row=1, column=0)
entry_dec = tk.Entry(root)
entry_dec.grid(row=1, column=1)

label_radius = tk.Label(root, text="Search Radius (arcseconds):")
label_radius.grid(row=2, column=0)
entry_radius = tk.Entry(root)
entry_radius.grid(row=2, column=1)

label_databases = tk.Label(root, text="Databases (S - SIMBAD, G - GAIA, V - Vizier):")
label_databases.grid(row=3, column=0)
entry_databases = tk.Entry(root)
entry_databases.grid(row=3, column=1)

label_vizier_databases = tk.Label(root, text="Vizier Databases (space separated):")
label_vizier_databases.grid(row=4, column=0)
entry_vizier_databases = tk.Entry(root)
entry_vizier_databases.grid(row=4, column=1)

# Add button to initiate search
search_button = tk.Button(root, text="Search", command=perform_search)
search_button.grid(row=5, column=0, columnspan=2)

# Start the application main loop
root.mainloop()

