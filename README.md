# MD Permeation Plots

## Publication-quality figure-generation script for results produced from molecular dynamics simulations of molecules permeating through a biological membrane

### What does it do?
*To write*

### Instructions to execute the script

1. **Create a work folder** where the source data will be located and where the
figures will be produced. The folder should the following:
    1. A folder called "source_data" which should have the following subfolders:
       1. pmf
       2. diffusion
       3. resistance
       4. hbonds

    2. (Optional) A folder called fonts which includes the fonts to be used in the figures (for journal requirements).

2. **Download the folder of the script** in the same folder as the work folder. The folder structure should now look like:
   - *Add the folder structure*

3. **Load the virtual environment** that is required for the script to run.
   - In Windows (Powershell):
      1. Open Powershell
      2. Enable ps1 scripts by changing the execution policy. Simply type:
         ```shell
         Set-ExecutionPolicy Unrestricted
         ```
      3. Load the virtual environment. If you are in the work directory, type:
         ```shell
         .\MD_permeation_plots\venv\Scripts\activate.ps1
         ```
      4. Powershell command line should now show (venv) before the prompt.
   
   - In GNU/linux (Bash):
      *To write*

   - In MacOS (Bash):
      *To write*

4. Execute the script by typing:
   ```shell
   python .\MD_permeation_plots\main.py
   ```
