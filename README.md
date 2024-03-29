ASTRA (Automated Search Tool for Research in Astronomy) is a tool to streamline the process for verifying if an object is a new discovery.

Install instructions:
Run the install_packages.py code to install all modules needed for ASTRA.

This program uses astroquery. If you wish to search the entirety of VizieR, leave you VizieR catalogs blank. If you wish to search specific databases, you need to enter the directory of each catalog manually (eg: J/AJ/151/41/movers) and separate with a space.

The directory can be found in the title box of each VizieR catalog highlighted in blue.

To enter a VizieR catalog into ASTRA, paste it into the VizieR databases plot, putting a space in between each directory. 

ASTRA will not return any photometric data from any database. 
SIMBAD will return the name of the object, right Ascension, and Bibcode. GAIA will return a table showing the designation and parallax of the object (Parallax is included because that's often a good indicator as to whether the object is new or not). VizieR will return a table list with the directory of each table. This can easily be googled which will turn up which VizieR database it is. 

The recommended search radius is 5 arcseconds or less. This helps to minimize getting objects back that may not be the object you're looking for.
