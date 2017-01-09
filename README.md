# Identifying Ad Images
Code to differentiate ad from non-ad images based on the geometry of the image (if available) as well as phrases occurring in the URL, the image's URL and alt text, the anchor text, and words occurring near the anchor text.

## Installing

Uses Python 3.5 and anaconda

### Linux 
1. Change into the directory where you want to place the repo
2. Clone it: `git clone https://github.com/jcharit1/Identifying-Ad-Images.git`
3. Change into repo directory: `cd Identifying-Ad-Images/`
4. Edit the environment file prefix (at the end) to reflect your anaconda directory
4. Copy the environment
	1. Option 1, partially copy the environment: `conda env create -f environment_lite.yml`
	2. Option 2, copy the full environment: `conda env create -f environment.yml`
5. Use environment: `source activate Jimmy_Charite_py35`
6. Make the script executable: `chmod +x ./code/predict_image_type.py`
7. Define the following file paths via bash variables:
	1. path_old_data
	2. path_colnames _use the file in the ./raw_data/ subdirectory of the repo_
	3. path_new_data
	4. path_pred_file
8. Run the script: `./code/predict_image_type.py $path_old_data $path_colnames $path_new_data $path_pred_file`

Copying the full python environment will take 10-15 minutes on a slow internet connection. However, OS specifics aside, it will get you a full mirror of my python environment. Then you should be able run all the notebooks and scripts with, hopefully, no errors. The limited environment (environment_lite.yml) should be sufficient for running the prediction script.

### Windows
TO DO

## Uninstalling

### Linux
1. Delete the repo: `rm -f Identifying-Ad-Images/`
2. Remove the environment: `conda env remove --name Jimmy_Charite_py35`

### Windows
TO DO

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Author

[Jimmy Charité](https://github.com/jcharit1)
jimmy.charite@gmail.com

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/jcharit1/Identifying-Ad-Images/blob/master/License.md) file for details
